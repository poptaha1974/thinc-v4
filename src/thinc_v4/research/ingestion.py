# -*- coding: utf-8 -*-
"""Research ingestion from open scientific databases.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

Sources (both free, no API key): OpenAlex (~250M works) and Semantic Scholar
(~200M). This is the only module in the research line that reaches the network, and
it does so through an injected `JsonFetcher`, so every test runs against a local
double and the suite never depends on an external service being up.
"""
from __future__ import annotations

import hashlib
import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Protocol, Sequence
from urllib.parse import quote_plus

from .models import ResearchPaper, utc_now

OPENALEX_URL = "https://api.openalex.org/works"
SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
USER_AGENT = "THINC/Egy-Pioneers-Academy (Dr. Ehab Taha)"
#: Cached responses older than this are refetched.
CACHE_TTL_SECONDS = 7 * 24 * 3600
DEFAULT_TIMEOUT = 30.0


class JsonFetcher(Protocol):
    """Anything that can turn a URL into a JSON document (or None on failure)."""

    def __call__(self, url: str, *, timeout: float = ...) -> Dict[str, Any] | None: ...


@dataclass
class FetchOutcome:
    """What a single query produced, so callers can report failures honestly."""

    query: str
    papers: List[ResearchPaper]
    failed: bool = False
    detail: str = ""


def http_json_fetcher(url: str, *, timeout: float = DEFAULT_TIMEOUT) -> Dict[str, Any] | None:
    """Default fetcher: a plain GET returning parsed JSON, or None on any failure."""

    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        return None
    return payload if isinstance(payload, dict) else None


def _expand_inverted_abstract(inverted: Dict[str, Sequence[int]]) -> str:
    """OpenAlex ships abstracts as {word: [positions]}; rebuild the text."""

    positions: Dict[int, str] = {}
    for word, indexes in inverted.items():
        for index in indexes:
            positions[index] = word
    return " ".join(positions[key] for key in sorted(positions))


class ResearchIngestor:
    """Query open scientific databases for papers about a theory.

    Args:
        fetcher: injected JSON fetcher; defaults to the real HTTP one.
        cache_dir: optional response cache. `None` disables caching entirely, which
            is what tests use.
    """

    def __init__(
        self,
        fetcher: JsonFetcher | None = None,
        cache_dir: Path | None = None,
        *,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self.fetcher: JsonFetcher = fetcher if fetcher is not None else http_json_fetcher
        self.cache_dir = cache_dir
        self.timeout = timeout

    # ── caching ───────────────────────────────────────────────────────────────

    def _cache_path(self, source: str, url: str) -> Path | None:
        if self.cache_dir is None:
            return None
        digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:32]
        return self.cache_dir / f"{source}_{digest}.json"

    def _cached(self, path: Path | None) -> Dict[str, Any] | None:
        if path is None or not path.exists():
            return None
        if time.time() - path.stat().st_mtime > CACHE_TTL_SECONDS:
            return None
        try:
            with path.open(encoding="utf-8") as handle:
                payload = json.load(handle)
        except (OSError, json.JSONDecodeError):
            return None
        return payload if isinstance(payload, dict) else None

    def _store(self, path: Path | None, payload: Dict[str, Any]) -> None:
        if path is None:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with path.open("w", encoding="utf-8") as handle:
                json.dump(payload, handle, ensure_ascii=False)
        except OSError:
            # a cache that cannot be written must never break ingestion
            return

    def _get(self, source: str, url: str) -> Dict[str, Any] | None:
        path = self._cache_path(source, url)
        cached = self._cached(path)
        if cached is not None:
            return cached
        payload = self.fetcher(url, timeout=self.timeout)
        if payload is not None:
            self._store(path, payload)
        return payload

    # ── sources ───────────────────────────────────────────────────────────────

    def openalex_url(
        self,
        query: str,
        *,
        from_year: int,
        min_citations: int = 3,
        max_results: int = 10,
        open_access_only: bool = True,
    ) -> str:
        filters = [f"from_publication_date:{from_year}-01-01"]
        if open_access_only:
            filters.append("is_oa:true")
        filters.append(f"cited_by_count:>{min_citations}")
        return (
            f"{OPENALEX_URL}?search={quote_plus(query)}"
            f"&filter={','.join(filters)}"
            f"&per-page={max_results}"
            f"&sort=cited_by_count:desc"
        )

    def search_openalex(
        self,
        query: str,
        *,
        from_year: int | None = None,
        min_citations: int = 3,
        max_results: int = 10,
    ) -> FetchOutcome:
        year = from_year if from_year is not None else utc_now().year - 3
        url = self.openalex_url(
            query, from_year=year, min_citations=min_citations, max_results=max_results
        )
        payload = self._get("openalex", url)
        if payload is None:
            return FetchOutcome(query, [], failed=True, detail="openalex request failed")

        papers: List[ResearchPaper] = []
        for record in payload.get("results", []):
            if not isinstance(record, dict):
                continue
            papers.append(self._paper_from_openalex(record, fallback_year=year))
        return FetchOutcome(query, papers)

    @staticmethod
    def _paper_from_openalex(record: Dict[str, Any], *, fallback_year: int) -> ResearchPaper:
        inverted = record.get("abstract_inverted_index")
        abstract = _expand_inverted_abstract(inverted) if isinstance(inverted, dict) else None

        authors: List[str] = []
        for authorship in record.get("authorships", [])[:5]:
            if isinstance(authorship, dict):
                name = (authorship.get("author") or {}).get("display_name")
                if name:
                    authors.append(str(name))

        location = record.get("primary_location") or {}
        source = location.get("source") if isinstance(location, dict) else None
        journal = source.get("display_name") if isinstance(source, dict) else None

        keywords: List[str] = [
            str(concept.get("display_name", ""))
            for concept in record.get("concepts", [])[:8]
            if isinstance(concept, dict) and concept.get("display_name")
        ]

        return ResearchPaper(
            source="openalex",
            external_id=str(record.get("id", "")),
            title=str(record.get("title") or "Untitled"),
            authors=authors,
            publication_year=int(record.get("publication_year") or fallback_year),
            journal=str(journal) if journal else None,
            doi=str(record["doi"]) if record.get("doi") else None,
            url=str(record.get("id")) if record.get("id") else None,
            abstract=abstract[:2000] if abstract else None,
            cited_by_count=int(record.get("cited_by_count") or 0),
            keywords=keywords,
        )

    def semantic_scholar_url(self, query: str, *, from_year: int, max_results: int = 5) -> str:
        fields = "title,abstract,year,authors,venue,citationCount,externalIds"
        return (
            f"{SEMANTIC_SCHOLAR_URL}?query={quote_plus(query)}"
            f"&year={from_year}-&limit={max_results}&fields={fields}"
        )

    def search_semantic_scholar(
        self, query: str, *, from_year: int | None = None, max_results: int = 5
    ) -> FetchOutcome:
        year = from_year if from_year is not None else utc_now().year - 3
        url = self.semantic_scholar_url(query, from_year=year, max_results=max_results)
        payload = self._get("semantic_scholar", url)
        if payload is None:
            return FetchOutcome(query, [], failed=True, detail="semantic scholar request failed")

        papers: List[ResearchPaper] = []
        for record in payload.get("data", []):
            if not isinstance(record, dict):
                continue
            papers.append(self._paper_from_semantic_scholar(record, fallback_year=year))
        return FetchOutcome(query, papers)

    @staticmethod
    def _paper_from_semantic_scholar(
        record: Dict[str, Any], *, fallback_year: int
    ) -> ResearchPaper:
        paper_id = str(record.get("paperId", ""))
        authors = [
            str(author.get("name", ""))
            for author in (record.get("authors") or [])[:5]
            if isinstance(author, dict) and author.get("name")
        ]
        external_ids = record.get("externalIds") or {}
        doi = external_ids.get("DOI") if isinstance(external_ids, dict) else None
        abstract = record.get("abstract") or ""

        return ResearchPaper(
            source="semantic_scholar",
            external_id=paper_id,
            title=str(record.get("title") or "Untitled"),
            authors=authors,
            publication_year=int(record.get("year") or fallback_year),
            journal=str(record["venue"]) if record.get("venue") else None,
            doi=str(doi) if doi else None,
            url=f"https://www.semanticscholar.org/paper/{paper_id}" if paper_id else None,
            abstract=str(abstract)[:2000] or None,
            cited_by_count=int(record.get("citationCount") or 0),
        )
