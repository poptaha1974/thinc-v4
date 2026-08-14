# -*- coding: utf-8 -*-
"""Theory registry and paper store for the THINC research line.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

Storage follows the lesson learned from the calibrated weights: an installed
package lives in a read-only `site-packages`, so shipped data is **seed data** and
the working state goes to a writable path chosen by the operator
(`THINC_RESEARCH_DIR`, defaulting to `~/.thinc/research`).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from .models import ResearchPaper, Theory, TheoryStatus, utc_now

#: Read-only reference data shipped with the package.
PACKAGED_DATA_DIR = Path(__file__).resolve().parent / "data"
#: Seed of the ten founding theories curated by Dr. Ehab Taha.
THEORIES_SEED_PATH = PACKAGED_DATA_DIR / "theories_seed.json"
#: Environment variable pointing at a writable directory for working state.
RESEARCH_DIR_ENV = "THINC_RESEARCH_DIR"


class ResearchStoreError(RuntimeError):
    """Raised when research state cannot be read or written."""


def resolve_research_dir(path: Path | None = None) -> Path:
    """Resolve the working directory: explicit path > env var > `~/.thinc/research`."""

    if path is not None:
        return path
    override = os.environ.get(RESEARCH_DIR_ENV, "").strip()
    if override:
        return Path(override).expanduser()
    return Path.home() / ".thinc" / "research"


def load_seed_theories() -> Dict[str, Theory]:
    """Load the shipped theory seed. Never written to."""

    with THEORIES_SEED_PATH.open(encoding="utf-8") as handle:
        payload: Dict[str, Any] = json.load(handle)
    return {theory_id: Theory(**data) for theory_id, data in payload.items()}


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        handle = path.open("w", encoding="utf-8")
    except OSError as exc:
        raise ResearchStoreError(
            f"Cannot write research state to {path}. "
            f"Set {RESEARCH_DIR_ENV} to a writable directory "
            "(installed packages are read-only)."
        ) from exc
    with handle as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2, default=str)
        fh.write("\n")


class TheoryRegistry:
    """The registry of behavioural theories, their status and confidence.

    On first use the registry is seeded from the packaged reference data, so a fresh
    install starts with the ten founding theories instead of an empty file.
    """

    FILENAME = "theory_registry.json"

    def __init__(self, path: Path | None = None, *, seed_if_missing: bool = True) -> None:
        self.path = path if path is not None else resolve_research_dir() / self.FILENAME
        self.theories: Dict[str, Theory] = self._load(seed_if_missing=seed_if_missing)

    def _load(self, *, seed_if_missing: bool) -> Dict[str, Theory]:
        if not self.path.exists():
            return load_seed_theories() if seed_if_missing else {}
        try:
            with self.path.open(encoding="utf-8") as handle:
                payload: Dict[str, Any] = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            raise ResearchStoreError(
                f"Theory registry at {self.path} is unreadable: {exc}. "
                "Fix or remove the file; refusing to continue with an empty registry "
                "because that would silently drop every tracked theory."
            ) from exc
        return {theory_id: Theory(**data) for theory_id, data in payload.items()}

    def save(self) -> None:
        _write_json(
            self.path,
            {tid: theory.model_dump(mode="json") for tid, theory in self.theories.items()},
        )

    def add_theory(self, theory: Theory) -> None:
        self.theories[theory.theory_id] = theory
        self.save()

    def get(self, theory_id: str) -> Theory | None:
        return self.theories.get(theory_id)

    def update_theory(self, theory_id: str, **changes: Any) -> bool:
        theory = self.theories.get(theory_id)
        if theory is None:
            return False
        for key, value in changes.items():
            if not hasattr(theory, key):
                raise ResearchStoreError(f"Theory has no field {key!r}")
            setattr(theory, key, value)
        theory.last_updated = utc_now()
        self.save()
        return True

    def deprecate_theory(self, theory_id: str, reason: str) -> bool:
        return self.update_theory(
            theory_id,
            status=TheoryStatus.DEPRECATED,
            description_ar=f"دُحضت: {reason}",
        )

    def active(self) -> List[Theory]:
        return [t for t in self.theories.values() if t.status == TheoryStatus.ACTIVE]

    def link_paper(self, theory_id: str, paper_id: str, *, supports: bool = True) -> bool:
        """Link evidence to a theory and recompute its confidence from the ratio.

        Note: this recomputes confidence from `net_evidence()`. Approving an
        `evidence_update` proposal deliberately does **not** go through here — it
        applies the reviewed value, because recomputing from a ratio with no
        contradicting papers jumps straight to 1.0.
        """

        theory = self.theories.get(theory_id)
        if theory is None:
            return False
        target = theory.supporting_papers if supports else theory.contradicting_papers
        if paper_id not in target:
            target.append(paper_id)
        theory.confidence_score = theory.net_evidence()
        theory.last_updated = utc_now()
        self.save()
        return True

    def find_by_keyword(self, keyword: str) -> Theory | None:
        needle = keyword.lower()
        for theory in self.theories.values():
            if (
                needle in theory.theory_id
                or needle in theory.name_en.lower()
                or needle in theory.name_ar
            ):
                return theory
            if any(needle in tag.lower() for tag in theory.tags):
                return theory
        return None

    def related_to(self, text: str) -> List[Theory]:
        """Active theories mentioned in `text` (already lowercased)."""

        return [theory for theory in self.active() if theory.matches(text)]


class PapersStore:
    """Deduplicated store of fetched papers."""

    FILENAME = "papers.json"

    def __init__(self, path: Path | None = None) -> None:
        self.path = path if path is not None else resolve_research_dir() / self.FILENAME
        self.papers: Dict[str, ResearchPaper] = self._load()

    def _load(self) -> Dict[str, ResearchPaper]:
        if not self.path.exists():
            return {}
        try:
            with self.path.open(encoding="utf-8") as handle:
                payload: Dict[str, Any] = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            raise ResearchStoreError(f"Papers store at {self.path} is unreadable: {exc}") from exc
        return {pid: ResearchPaper(**data) for pid, data in payload.items()}

    def save(self) -> None:
        _write_json(
            self.path,
            {pid: paper.model_dump(mode="json") for pid, paper in self.papers.items()},
        )

    def add_or_update(self, paper: ResearchPaper) -> bool:
        """Store `paper`; return `True` only when it is new.

        A duplicate refreshes the citation count (monotonically) instead of creating
        a second row for the same DOI.
        """

        key = paper.dedupe_key()
        for existing in self.papers.values():
            if existing.dedupe_key() == key:
                existing.cited_by_count = max(existing.cited_by_count, paper.cited_by_count)
                self.save()
                return False
        self.papers[paper.paper_id] = paper
        self.save()
        return True

    def add_many(self, papers: Iterable[ResearchPaper]) -> List[ResearchPaper]:
        """Store several papers, returning only the newly added ones."""

        return [paper for paper in papers if self.add_or_update(paper)]
