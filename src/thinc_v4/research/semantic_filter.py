# -*- coding: utf-8 -*-
"""Semantic filtering of candidate papers before they enter the research base.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

This layer exists because of a documented failure: the first unfiltered run had the
ingestor accept any paper whose text contained "social" or "loss", so papers about
athlete concussion and coronary disease were proposed as evidence for Social Proof
— six of ten proposals were unusable. The filter fixed that by combining a hard
keyword blacklist, journal lists, and a required-keyword gate, with every rejection
logged with its reason.

The decision is a pure function (`evaluate`); only `filter_papers` touches storage.
"""
from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

from .models import ResearchPaper

#: Any of these in the title or abstract rejects the paper outright.
HARD_BLACKLIST_KEYWORDS: Tuple[str, ...] = (
    # clinical / medical
    "clinical trial", "clinicians", "clinician", "patient outcomes", "patient care",
    "healthcare", "health care", "medical", "medicine",
    "disease", "diagnosis", "treatment", "therapy", "therapeutic",
    "cardiac", "coronary", "cardiovascular", "cardiology",
    "cancer", "tumor", "oncology", "neurology",
    "dementia", "alzheimer", "parkinson",
    "concussion", "injury", "surgery", "surgical",
    "eating disorder", "anorexia", "bulimia",
    "psychiatric", "schizophrenia", "depression treatment",
    "pharmaceutical", "drug", "medication", "vaccine",
    "epidemic", "pandemic", "covid-19 treatment",
    "clinical guideline", "medical guideline",
    # pure natural science
    "climate change", "ipcc", "biodiversity",
    "quantum", "particle physics", "astronomy",
    # engineering / networks
    "iot", "internet of things", "wireless sensor",
    "5g network", "blockchain protocol", "cryptocurrency mining",
    # purely technical AI (not behavioural)
    "gpt-4 technical", "large language model architecture",
    "transformer architecture", "neural network architecture",
    # sports
    "sport", "athlete", "football player", "olympic",
)

#: Journals rejected outright.
BLACKLIST_JOURNALS: Tuple[str, ...] = (
    "circulation", "lancet", "nejm", "new england journal of medicine",
    "jama", "bmj", "british medical journal",
    "journal of eating disorders", "eating disorders",
    "british journal of sports medicine", "sports medicine",
    "journal of clinical", "clinical psychology review",
    "cochrane database of systematic reviews",
    "ipcc", "nature climate",
    "sensors", "ieee",
    "jmir ai", "jmir",
)

#: Journals trusted for consumer behaviour and marketing.
WHITELIST_JOURNALS: Tuple[str, ...] = (
    "journal of consumer research", "journal of marketing",
    "journal of marketing research", "marketing science",
    "journal of consumer psychology", "psychology & marketing",
    "journal of retailing", "journal of the academy of marketing science",
    "journal of behavioral decision making", "judgment and decision making",
    "organizational behavior and human decision processes",
    "journal of economic behavior", "journal of economic psychology",
    "journal of behavioral economics", "behavioral science",
    "journal of consumer behaviour", "journal of consumer behavior",
    "journal of economic literature",
    "quarterly journal of economics", "american economic review",
    "psychological science", "cognitive psychology",
    "personality and social psychology",
    "journal of experimental social psychology",
    "frontiers in psychology",
)

#: At least one of these must appear, otherwise the paper is off-topic.
REQUIRED_KEYWORDS: Tuple[str, ...] = (
    "consumer", "customer", "shopper", "buyer",
    "marketing", "advertising", "brand", "advertisement",
    "purchase", "purchasing", "buying decision", "willingness to pay",
    "choice", "decision-making", "decision making",
    "behavioral economics", "behavioural economics",
    "prospect theory", "framing effect", "cognitive bias",
    "heuristic", "bias", "nudge", "nudging",
    "e-commerce", "ecommerce", "online shopping", "retail",
    "persuasion", "influence", "social norm",
    "loss aversion", "anchoring", "social proof", "scarcity",
    "peak-end", "peak end", "endowment", "reciprocity",
    "commitment", "consistency", "cognitive ease", "fluency",
    "default effect", "choice architecture",
)


@dataclass(frozen=True)
class FilterVerdict:
    """Outcome of filtering one paper."""

    accepted: bool
    rule: str
    detail: str = ""

    @property
    def reason(self) -> str:
        """Compact reason string, kept in the same shape the log has always used."""

        return f"{self.rule}:{self.detail}" if self.detail else self.rule


class SemanticFilter:
    """Decide whether a paper belongs in the THINC research base.

    Args:
        rejection_log_path: where rejections are appended. Defaults to no logging,
            so importing and using the filter never writes to a read-only install.
        hard_blacklist_wins: when `True`, a blacklisted keyword rejects a paper even
            if it comes from a whitelisted journal. Defaults to `False`, which
            preserves the shipped precedence (journal whitelist first) — behaviour
            is not changed silently.
    """

    def __init__(
        self,
        rejection_log_path: Path | None = None,
        *,
        hard_blacklist_wins: bool = False,
    ) -> None:
        self.rejection_log_path = rejection_log_path
        self.hard_blacklist_wins = hard_blacklist_wins
        self.rejection_log: List[Dict[str, Any]] = self._load_log()

    def _load_log(self) -> List[Dict[str, Any]]:
        if self.rejection_log_path is None or not self.rejection_log_path.exists():
            return []
        try:
            with self.rejection_log_path.open(encoding="utf-8") as handle:
                loaded = json.load(handle)
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(loaded, list):
            return []
        return [entry for entry in loaded if isinstance(entry, dict)]

    def _save_log(self) -> None:
        if self.rejection_log_path is None:
            return
        self.rejection_log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.rejection_log_path.open("w", encoding="utf-8") as handle:
            json.dump(self.rejection_log, handle, ensure_ascii=False, indent=2, default=str)
            handle.write("\n")

    def evaluate(self, paper: ResearchPaper) -> FilterVerdict:
        """Pure accept/reject decision with the rule that decided it."""

        text = f"{paper.title or ''} {paper.abstract or ''}".lower()
        journal = (paper.journal or "").lower()

        blacklisted_keyword = next(
            (kw for kw in HARD_BLACKLIST_KEYWORDS if kw in text), None
        )
        if self.hard_blacklist_wins and blacklisted_keyword is not None:
            return FilterVerdict(False, "blacklist_keyword", blacklisted_keyword)

        for allowed in WHITELIST_JOURNALS:
            if allowed in journal:
                return FilterVerdict(True, "whitelist_journal", allowed)

        for blocked in BLACKLIST_JOURNALS:
            if blocked in journal:
                return FilterVerdict(False, "blacklist_journal", blocked)

        if blacklisted_keyword is not None:
            return FilterVerdict(False, "blacklist_keyword", blacklisted_keyword)

        matched = [kw for kw in REQUIRED_KEYWORDS if kw in text]
        if not matched:
            return FilterVerdict(False, "no_required_keyword_matched")

        return FilterVerdict(True, "required_keywords_matched", ",".join(matched[:3]))

    def filter_papers(
        self, papers: Sequence[ResearchPaper], log_rejections: bool = True
    ) -> List[ResearchPaper]:
        """Return the accepted papers, recording every rejection with its reason."""

        accepted: List[ResearchPaper] = []
        rejections: List[Dict[str, Any]] = []

        for paper in papers:
            verdict = self.evaluate(paper)
            if verdict.accepted:
                accepted.append(paper)
                continue
            rejections.append(
                {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "paper_id": paper.paper_id,
                    "title": (paper.title or "")[:200],
                    "journal": paper.journal,
                    "year": paper.publication_year,
                    "reason": verdict.reason,
                    "citations": paper.cited_by_count,
                }
            )

        if rejections:
            self.rejection_log.extend(rejections)
            if log_rejections:
                self._save_log()

        return accepted

    def stats(self) -> Dict[str, Any]:
        """Rejection counts by rule, for reviewing whether the filter is too strict."""

        if not self.rejection_log:
            return {"total_rejections": 0, "by_reason": {}, "recent": []}
        reasons: Counter[str] = Counter()
        for entry in self.rejection_log:
            reason = str(entry.get("reason", "unknown"))
            reasons[reason.split(":")[0]] += 1
        return {
            "total_rejections": len(self.rejection_log),
            "by_reason": dict(reasons.most_common()),
            "recent": self.rejection_log[-10:],
        }
