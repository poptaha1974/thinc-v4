# -*- coding: utf-8 -*-
"""The Auto-Updater: one supervised cycle from papers to reviewable proposals.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

Cycle: build queries from the active theories → fetch → filter → grade → dedupe →
propose. **Nothing is applied.** Every proposal waits for Dr. Ehab Taha's review,
and the run record reports what was fetched, filtered out, stored, and which
queries failed — a failed source is visible instead of looking like "no results".

CLI: `thinc-v4-research run | pending | approve <id> | reject <id> | stats`
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Sequence

from .evidence import grade_and_annotate
from .ingestion import JsonFetcher, ResearchIngestor
from .models import ResearchPaper, UpdateRun, utc_now
from .proposals import ProposalGenerator, ProposalStore
from .registry import PapersStore, TheoryRegistry, resolve_research_dir
from .semantic_filter import SemanticFilter

#: Upper bound on queries per cycle, to stay well inside the free rate limits.
MAX_QUERIES_PER_RUN = 35
#: Pause between requests, for the same reason.
REQUEST_SPACING_SECONDS = 0.5
#: Queries used when the registry has no active theory yet.
FALLBACK_QUERIES: tuple[str, ...] = (
    "consumer behavior meta-analysis",
    "marketing science behavioral economics",
    "purchase decision heuristic",
)
#: Context suffixes appended to each theory name. The quoted theory name is what
#: stopped the ingestor from matching any paper containing "loss" or "social".
QUERY_CONTEXTS: tuple[str, ...] = ("consumer behavior", "marketing", "purchase decision")


class AutoUpdater:
    """Coordinates one update cycle. Human-in-the-Loop by construction."""

    RUNS_FILENAME = "update_runs.json"

    def __init__(
        self,
        research_dir: Path | None = None,
        *,
        fetcher: JsonFetcher | None = None,
        registry: TheoryRegistry | None = None,
        papers: PapersStore | None = None,
        generator: ProposalGenerator | None = None,
        semantic_filter: SemanticFilter | None = None,
        ingestor: ResearchIngestor | None = None,
        weights_path: Path | None = None,
        request_spacing: float = REQUEST_SPACING_SECONDS,
    ) -> None:
        base = resolve_research_dir(research_dir)
        self.base_dir = base
        self.registry = registry if registry is not None else TheoryRegistry(base / TheoryRegistry.FILENAME)
        self.papers = papers if papers is not None else PapersStore(base / PapersStore.FILENAME)
        self.generator = (
            generator
            if generator is not None
            else ProposalGenerator(
                self.registry, ProposalStore(base / ProposalStore.FILENAME), weights_path
            )
        )
        self.semantic_filter = (
            semantic_filter
            if semantic_filter is not None
            else SemanticFilter(base / "rejection_log.json")
        )
        self.ingestor = (
            ingestor
            if ingestor is not None
            else ResearchIngestor(fetcher, cache_dir=base / "cache")
        )
        self.runs_path = base / self.RUNS_FILENAME
        self.request_spacing = request_spacing

    # ── queries ───────────────────────────────────────────────────────────────

    def build_queries(self) -> List[str]:
        """One quoted-name query per context, per active theory."""

        active = self.registry.active()
        if not active:
            return list(FALLBACK_QUERIES)
        queries: List[str] = []
        for theory in active:
            for context in QUERY_CONTEXTS:
                queries.append(f'"{theory.name_en}" {context}')
        return queries[:MAX_QUERIES_PER_RUN]

    # ── the cycle ─────────────────────────────────────────────────────────────

    def run_cycle(self, triggered_by: str = "manual", *, max_queries: int | None = None) -> UpdateRun:
        run = UpdateRun(
            triggered_by=triggered_by, sources_queried=["openalex", "semantic_scholar"]
        )
        queries = self.build_queries()
        if max_queries is not None:
            queries = queries[:max_queries]

        fetched: List[ResearchPaper] = []
        for index, query in enumerate(queries):
            outcome = self.ingestor.search_openalex(query)
            if outcome.failed:
                run.queries_failed.append(query)
            fetched.extend(outcome.papers)

            # Semantic Scholar is a fallback for thin OpenAlex results only
            if not outcome.failed and len(outcome.papers) < 3:
                secondary = self.ingestor.search_semantic_scholar(query)
                if secondary.failed:
                    run.queries_failed.append(query)
                fetched.extend(secondary.papers)

            if self.request_spacing and index < len(queries) - 1:
                time.sleep(self.request_spacing)

        run.papers_fetched = len(fetched)
        accepted = self.semantic_filter.filter_papers(fetched)
        run.papers_filtered_out = len(fetched) - len(accepted)

        grade_and_annotate(accepted)
        new_papers = self.papers.add_many(accepted)
        run.papers_new = len(new_papers)

        proposals = self.generator.analyze_papers(new_papers)
        run.proposals_generated = len(proposals)

        run.completed_at = utc_now()
        run.status = "completed"
        self._append_run(run)
        return run

    def _append_run(self, run: UpdateRun) -> None:
        runs: List[Dict[str, Any]] = []
        if self.runs_path.exists():
            try:
                with self.runs_path.open(encoding="utf-8") as handle:
                    loaded = json.load(handle)
                if isinstance(loaded, list):
                    runs = [entry for entry in loaded if isinstance(entry, dict)]
            except (OSError, json.JSONDecodeError):
                runs = []
        runs.append(run.model_dump(mode="json"))
        self.runs_path.parent.mkdir(parents=True, exist_ok=True)
        with self.runs_path.open("w", encoding="utf-8") as handle:
            json.dump(runs, handle, ensure_ascii=False, indent=2, default=str)
            handle.write("\n")

    # ── review passthrough ────────────────────────────────────────────────────

    def pending(self) -> List[Any]:
        return self.generator.pending()

    def approve(self, proposal_id: str, notes: str = "") -> bool:
        return self.generator.approve(proposal_id, notes)

    def reject(self, proposal_id: str, notes: str = "") -> bool:
        return self.generator.reject(proposal_id, notes)

    def stats(self) -> Dict[str, Any]:
        return {
            "research_dir": str(self.base_dir),
            "theories_active": len(self.registry.active()),
            "theories_total": len(self.registry.theories),
            "papers_stored": len(self.papers.papers),
            "proposals_pending": len(self.generator.pending()),
            "rejections": self.semantic_filter.stats()["total_rejections"],
        }


def _print_pending(updater: AutoUpdater) -> None:
    pending = updater.pending()
    if not pending:
        print("لا اقتراحات معلّقة.")
        return
    print(f"اقتراحات معلّقة: {len(pending)}\n")
    for proposal in pending:
        print(f"• {proposal.proposal_id}")
        print(f"  النوع: {proposal.proposal_type.value} | الهدف: {proposal.target}")
        print(f"  الحالي: {proposal.current_value} → المقترح: {proposal.proposed_value}")
        print(f"  الثقة: {proposal.confidence}")
        print(f"  المبرر: {proposal.justification[:200]}\n")


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="THINC research Auto-Updater (Human-in-the-Loop: nothing is auto-applied)."
    )
    parser.add_argument(
        "command", choices=["run", "pending", "approve", "reject", "stats"], help="action"
    )
    parser.add_argument("proposal_id", nargs="?", help="proposal id for approve/reject")
    parser.add_argument("--notes", default="", help="reviewer notes")
    parser.add_argument("--dir", type=Path, default=None, help="research state directory")
    parser.add_argument("--max-queries", type=int, default=None, help="limit queries this run")
    parser.add_argument(
        "--triggered-by", default="manual", help="who started this run (manual/cron/api)"
    )
    args = parser.parse_args(argv)

    updater = AutoUpdater(args.dir)

    if args.command == "run":
        run = updater.run_cycle(args.triggered_by, max_queries=args.max_queries)
        print(f"أوراق مسحوبة: {run.papers_fetched}")
        print(f"مرفوضة بالفلتر: {run.papers_filtered_out}")
        print(f"جديدة مخزّنة: {run.papers_new}")
        print(f"اقتراحات مولّدة: {run.proposals_generated} (كلها معلّقة للمراجعة)")
        if run.queries_failed:
            print(f"⚠️ استعلامات فشلت: {len(run.queries_failed)}")
    elif args.command == "pending":
        _print_pending(updater)
    elif args.command == "approve":
        if not args.proposal_id:
            raise SystemExit("approve requires a proposal id")
        print("✅ اعتُمد وطُبِّق" if updater.approve(args.proposal_id, args.notes) else "❌ غير موجود أو مُراجَع")
    elif args.command == "reject":
        if not args.proposal_id:
            raise SystemExit("reject requires a proposal id")
        print("✅ رُفض" if updater.reject(args.proposal_id, args.notes) else "❌ غير موجود أو مُراجَع")
    else:
        for key, value in updater.stats().items():
            print(f"{key}: {value}")


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
