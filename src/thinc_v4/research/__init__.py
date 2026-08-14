# -*- coding: utf-8 -*-
"""THINC research line — theory registry, evidence grading, and update proposals.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

This subpackage brings the self-updating edition's research engine into the packaged
distribution, under the same gates as the rest of `thinc_v4`: Ruff, MyPy strict, and
tests that never touch the network.

**Human-in-the-Loop:** nothing here changes the model on its own. Papers are fetched,
filtered, graded, and turned into proposals; a proposal only takes effect when it is
explicitly approved.

Layout:

- `models` — `ResearchPaper`, `Theory`, `UpdateProposal`, `UpdateRun`, evidence enums
- `evidence` — Cochrane-style grading (pure functions)
- `semantic_filter` — keeps off-topic (medical, sports, technical) papers out
- `registry` — theory registry and deduplicated paper store
- `proposals` — proposal generation, review, and application
"""
from __future__ import annotations

from .evidence import grade_and_annotate, grade_paper
from .models import (
    EVIDENCE_WEIGHTS,
    EvidenceLevel,
    ProposalType,
    ResearchPaper,
    Theory,
    TheoryStatus,
    UpdateProposal,
    UpdateRun,
    utc_now,
)
from .proposals import ProposalGenerator, ProposalStore
from .registry import (
    PapersStore,
    ResearchStoreError,
    TheoryRegistry,
    load_seed_theories,
    resolve_research_dir,
)
from .semantic_filter import FilterVerdict, SemanticFilter

__all__ = [
    "EVIDENCE_WEIGHTS",
    "EvidenceLevel",
    "FilterVerdict",
    "PapersStore",
    "ProposalGenerator",
    "ProposalStore",
    "ProposalType",
    "ResearchPaper",
    "ResearchStoreError",
    "SemanticFilter",
    "Theory",
    "TheoryRegistry",
    "TheoryStatus",
    "UpdateProposal",
    "UpdateRun",
    "grade_and_annotate",
    "grade_paper",
    "load_seed_theories",
    "resolve_research_dir",
    "utc_now",
]
