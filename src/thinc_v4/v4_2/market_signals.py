# -*- coding: utf-8 -*-
"""Auditable market-signal evidence gate for THINC v4.2."""

from __future__ import annotations

import csv
import io
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Type, TypeVar


EnumT = TypeVar("EnumT", bound=Enum)


def _normalized_enum_text(value: Any) -> str:
    return str(value).strip().lower().replace("-", "_").replace(" ", "_")


def _coerce_enum(enum_cls: Type[EnumT], raw: Any, field_name: str) -> EnumT:
    if isinstance(raw, enum_cls):
        return raw
    normalized = _normalized_enum_text(raw)
    for item in enum_cls:
        if normalized in {
            _normalized_enum_text(item.name),
            _normalized_enum_text(item.value),
        }:
            return item
    allowed = ", ".join(str(item.value) for item in enum_cls)
    raise ValueError(f"Unsupported {field_name}: {raw!r}. Allowed: {allowed}")


def _parse_datetime(raw: Any) -> tuple[datetime | None, List[str]]:
    if raw in (None, ""):
        return None, []
    if isinstance(raw, datetime):
        return raw, []
    try:
        text = str(raw).strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        return datetime.fromisoformat(text), []
    except ValueError:
        return None, ["collected_at must be a valid ISO-8601 timestamp"]


class MarketSignalSource(Enum):
    GOOGLE_TRENDS = "google_trends"
    META_AD_LIBRARY = "meta_ad_library"
    MARKETPLACE = "marketplace"
    FIRST_PARTY_CAMPAIGN = "first_party_campaign"


class CollectionMethod(Enum):
    BROWSER_ASSISTED = "browser_assisted"
    FILE_UPLOAD = "file_upload"
    AUTOMATED_PROVIDER = "automated_provider"


class EvidenceStatus(Enum):
    COLLECTED = "COLLECTED"
    NOT_COLLECTED = "NOT_COLLECTED"
    STALE = "STALE"
    INVALID = "INVALID"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class DecisionStage(Enum):
    PRE_TEST_RESEARCH = "pre_test_research"
    CONTROLLED_TEST = "controlled_test"
    SCALE = "scale"


class GateDecision(Enum):
    PASS = "PASS"
    HOLD_FOR_RESEARCH = "HOLD_FOR_RESEARCH"
    BLOCK_SCALE = "BLOCK_SCALE"


@dataclass
class MarketSignalEvidence:
    source: MarketSignalSource
    status: EvidenceStatus
    query: str = ""
    country: str = ""
    timeframe: str = ""
    collected_at: datetime | None = None
    collection_method: CollectionMethod | None = None
    source_reference: str = ""
    summary: str = ""
    metrics: Dict[str, Any] = field(default_factory=dict)
    limitations: List[str] = field(default_factory=list)
    collector: str = ""
    competitor_or_marketplace: str = ""
    raw_evidence_hash: str = ""
    ingestion_errors: List[str] = field(default_factory=list, repr=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MarketSignalEvidence:
        if not isinstance(data, dict):
            raise ValueError("Each market evidence record must be an object.")
        if "source" not in data:
            raise ValueError("Market evidence field 'source' is required.")
        source = _coerce_enum(MarketSignalSource, data["source"], "market source")
        status = _coerce_enum(
            EvidenceStatus,
            data.get("status", EvidenceStatus.NOT_COLLECTED.value),
            "evidence status",
        )
        method_raw = data.get("collection_method")
        method = (
            _coerce_enum(CollectionMethod, method_raw, "collection method")
            if method_raw not in (None, "")
            else None
        )
        collected_at, parse_errors = _parse_datetime(data.get("collected_at"))
        metrics = data.get("metrics", {})
        limitations = data.get("limitations", [])
        return cls(
            source=source,
            status=status,
            query=str(data.get("query", "")).strip(),
            country=str(data.get("country", "")).strip(),
            timeframe=str(data.get("timeframe", "")).strip(),
            collected_at=collected_at,
            collection_method=method,
            source_reference=str(data.get("source_reference", "")).strip(),
            summary=str(data.get("summary", "")).strip(),
            metrics=dict(metrics) if isinstance(metrics, dict) else {},
            limitations=(
                [str(item) for item in limitations]
                if isinstance(limitations, list)
                else [str(limitations)]
            ),
            collector=str(data.get("collector", "")).strip(),
            competitor_or_marketplace=str(
                data.get("competitor_or_marketplace", "")
            ).strip(),
            raw_evidence_hash=str(data.get("raw_evidence_hash", "")).strip(),
            ingestion_errors=(
                parse_errors
                + ([] if isinstance(metrics, dict) else ["metrics must be an object"])
            ),
        )

    def validation_errors(self) -> List[str]:
        errors = list(self.ingestion_errors)
        if self.status is EvidenceStatus.COLLECTED:
            required_strings = {
                "query": self.query,
                "country": self.country,
                "timeframe": self.timeframe,
                "source_reference": self.source_reference,
                "summary": self.summary,
            }
            errors.extend(
                f"{name} is required when status is COLLECTED"
                for name, value in required_strings.items()
                if not value
            )
            if self.collected_at is None:
                errors.append("collected_at is required when status is COLLECTED")
            elif (
                self.collected_at.tzinfo is None
                or self.collected_at.utcoffset() is None
            ):
                errors.append("collected_at must include a timezone")
            if self.collection_method is None:
                errors.append("collection_method is required when status is COLLECTED")
            if not self.metrics:
                errors.append("metrics is required when status is COLLECTED")
            elif self.metrics.get("example_only") is True:
                errors.append(
                    "synthetic example metrics cannot satisfy the market evidence gate"
                )
        elif self.status in {
            EvidenceStatus.NOT_COLLECTED,
            EvidenceStatus.NOT_APPLICABLE,
        } and self.metrics:
            errors.append(
                f"metrics must be empty when status is {self.status.value}"
            )
        return errors

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source.value,
            "status": self.status.value,
            "query": self.query,
            "country": self.country,
            "timeframe": self.timeframe,
            "collected_at": (
                self.collected_at.isoformat() if self.collected_at else None
            ),
            "collection_method": (
                self.collection_method.value if self.collection_method else None
            ),
            "source_reference": self.source_reference,
            "summary": self.summary,
            "metrics": dict(self.metrics),
            "limitations": list(self.limitations),
            "collector": self.collector,
            "competitor_or_marketplace": self.competitor_or_marketplace,
            "raw_evidence_hash": self.raw_evidence_hash,
        }


@dataclass
class MarketSignalGateResult:
    decision: GateDecision
    stage: DecisionStage
    coverage_status_by_source: Dict[str, str]
    freshness_status_by_source: Dict[str, str]
    contradictions: List[str]
    reasons: List[str]
    required_actions: List[str]
    evidence_snapshot: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision": self.decision.value,
            "stage": self.stage.value,
            "coverage_status_by_source": dict(self.coverage_status_by_source),
            "freshness_status_by_source": dict(self.freshness_status_by_source),
            "contradictions": list(self.contradictions),
            "reasons": list(self.reasons),
            "required_actions": list(self.required_actions),
            "evidence_snapshot": list(self.evidence_snapshot),
        }


class BrowserAssistedProvider:
    """Normalize browser-documented findings into the shared evidence schema."""

    @staticmethod
    def ingest(records: Sequence[Dict[str, Any]]) -> List[MarketSignalEvidence]:
        normalized: List[MarketSignalEvidence] = []
        for record in records:
            payload = dict(record)
            payload.setdefault(
                "collection_method", CollectionMethod.BROWSER_ASSISTED.value
            )
            normalized.append(MarketSignalEvidence.from_dict(payload))
        return normalized


class FileEvidenceProvider:
    """Normalize user-supplied JSON/CSV rows into the shared evidence schema."""

    @staticmethod
    def ingest(records: Sequence[Dict[str, Any]]) -> List[MarketSignalEvidence]:
        normalized: List[MarketSignalEvidence] = []
        for record in records:
            payload = dict(record)
            payload.setdefault("collection_method", CollectionMethod.FILE_UPLOAD.value)
            normalized.append(MarketSignalEvidence.from_dict(payload))
        return normalized

    @classmethod
    def ingest_csv_text(cls, csv_text: str) -> List[MarketSignalEvidence]:
        """Parse a normalized evidence CSV, including JSON metrics/limitations cells."""

        if not str(csv_text).strip():
            return []
        reader = csv.DictReader(io.StringIO(csv_text))
        if not reader.fieldnames:
            raise ValueError("Evidence CSV must include a header row.")
        records: List[Dict[str, Any]] = []
        for row_number, row in enumerate(reader, start=2):
            payload: Dict[str, Any] = dict(row)
            json_fields: tuple[tuple[str, Any, type], ...] = (
                ("metrics", {}, dict),
                ("limitations", [], list),
            )
            for field_name, empty_value, expected_type in json_fields:
                raw = payload.get(field_name)
                if raw in (None, ""):
                    payload[field_name] = empty_value
                    continue
                try:
                    parsed = json.loads(str(raw))
                except json.JSONDecodeError as exc:
                    raise ValueError(
                        f"Evidence CSV row {row_number} field '{field_name}' must contain valid JSON."
                    ) from exc
                if not isinstance(parsed, expected_type):
                    raise ValueError(
                        f"Evidence CSV row {row_number} field '{field_name}' must decode to {expected_type.__name__}."
                    )
                payload[field_name] = parsed
            records.append(payload)
        return cls.ingest(records)


class AutomatedProvider:
    """Report automation readiness without treating configuration as evidence."""

    @staticmethod
    def status(env_key: str, provider_implemented: bool = False) -> Dict[str, Any]:
        credential_configured = bool(os.environ.get(env_key))
        automation_enabled = provider_implemented and credential_configured
        return {
            "methodological_status": "METHODOLOGICALLY_REQUIRED",
            "browser_status": "BROWSER_ASSISTED_AVAILABLE",
            "file_status": "FILE_INGESTION_AVAILABLE",
            "automation_status": (
                "AUTOMATED_PROVIDER_ENABLED"
                if automation_enabled
                else "AUTOMATED_PROVIDER_PENDING"
            ),
            "credential_configured": credential_configured,
            "evidence_available": False,
        }


class MarketSignalTriangulationEngine:
    """Separates market-evidence coverage from THINC economics decisions."""

    RESEARCH_SOURCES = (
        MarketSignalSource.GOOGLE_TRENDS,
        MarketSignalSource.META_AD_LIBRARY,
        MarketSignalSource.MARKETPLACE,
    )
    FRESHNESS_LIMITS = {
        MarketSignalSource.GOOGLE_TRENDS: timedelta(days=7),
        MarketSignalSource.META_AD_LIBRARY: timedelta(days=3),
        MarketSignalSource.MARKETPLACE: timedelta(days=3),
        MarketSignalSource.FIRST_PARTY_CAMPAIGN: timedelta(days=1),
    }
    SOURCE_LABELS = {
        MarketSignalSource.GOOGLE_TRENDS: "Google Trends",
        MarketSignalSource.META_AD_LIBRARY: "Meta Ad Library",
        MarketSignalSource.MARKETPLACE: "Marketplace",
        MarketSignalSource.FIRST_PARTY_CAMPAIGN: "First-party campaign",
    }

    @classmethod
    def _evaluate_record(
        cls,
        record: MarketSignalEvidence,
        now: datetime,
    ) -> tuple[str, float | None, List[str]]:
        errors = record.validation_errors()
        if record.status is EvidenceStatus.INVALID or errors:
            return EvidenceStatus.INVALID.value, None, errors
        if record.status is not EvidenceStatus.COLLECTED:
            return record.status.value, None, errors
        if record.country.casefold() != "egypt".casefold():
            return "WRONG_COUNTRY", None, errors

        if record.collected_at is None:  # pragma: no cover - guarded by validation_errors()
            return EvidenceStatus.INVALID.value, None, ["collected_at is required when status is COLLECTED"]

        collected_utc = record.collected_at.astimezone(timezone.utc)
        age = now - collected_utc
        age_days = max(0.0, age.total_seconds() / 86400.0)
        if age > cls.FRESHNESS_LIMITS[record.source]:
            return EvidenceStatus.STALE.value, age_days, errors
        return "FRESH", age_days, errors

    @staticmethod
    def _selection_priority(evaluated_status: str) -> int:
        return {
            "FRESH": 6,
            EvidenceStatus.STALE.value: 5,
            EvidenceStatus.INVALID.value: 4,
            "WRONG_COUNTRY": 3,
            EvidenceStatus.NOT_APPLICABLE.value: 2,
            EvidenceStatus.NOT_COLLECTED.value: 1,
        }.get(evaluated_status, 0)

    @classmethod
    def evaluate(
        cls,
        evidence: Sequence[MarketSignalEvidence],
        stage: DecisionStage,
        now: datetime | None = None,
    ) -> MarketSignalGateResult:
        stage = _coerce_enum(DecisionStage, stage, "decision stage")
        evaluated_at = now or datetime.now(timezone.utc)
        if evaluated_at.tzinfo is None or evaluated_at.utcoffset() is None:
            raise ValueError("Gate evaluation time must include a timezone.")
        evaluated_at = evaluated_at.astimezone(timezone.utc)

        coverage: Dict[str, str] = {
            source.value: EvidenceStatus.NOT_COLLECTED.value
            for source in MarketSignalSource
        }
        if stage is not DecisionStage.SCALE:
            coverage[MarketSignalSource.FIRST_PARTY_CAMPAIGN.value] = (
                EvidenceStatus.NOT_APPLICABLE.value
            )
        freshness = dict(coverage)
        selected: Dict[MarketSignalSource, tuple[int, datetime, str, List[str]]] = {}
        selected_records: Dict[MarketSignalSource, MarketSignalEvidence] = {}
        snapshots: List[Dict[str, Any]] = []

        for record in evidence:
            if not isinstance(record, MarketSignalEvidence):
                raise ValueError(
                    "MarketSignalTriangulationEngine requires MarketSignalEvidence records."
                )
            evaluated_status, age_days, errors = cls._evaluate_record(
                record, evaluated_at
            )
            snapshot = record.to_dict()
            snapshot.update(
                {
                    "evaluated_status": evaluated_status,
                    "age_days": round(age_days, 3) if age_days is not None else None,
                    "validation_errors": errors,
                }
            )
            snapshots.append(snapshot)
            timestamp = record.collected_at
            if (
                timestamp is None
                or timestamp.tzinfo is None
                or timestamp.utcoffset() is None
            ):
                timestamp = datetime.min.replace(tzinfo=timezone.utc)
            else:
                timestamp = timestamp.astimezone(timezone.utc)
            candidate = (
                cls._selection_priority(evaluated_status),
                timestamp,
                evaluated_status,
                errors,
            )
            current = selected.get(record.source)
            if current is None or candidate[:2] > current[:2]:
                selected[record.source] = candidate
                selected_records[record.source] = record

        for source, (_, _, evaluated_status, _) in selected.items():
            coverage[source.value] = (
                EvidenceStatus.COLLECTED.value
                if evaluated_status == "FRESH"
                else evaluated_status
            )
            freshness[source.value] = evaluated_status

        mandatory_sources = list(cls.RESEARCH_SOURCES)
        if stage is DecisionStage.SCALE:
            mandatory_sources.append(MarketSignalSource.FIRST_PARTY_CAMPAIGN)
        unsatisfied = [
            source
            for source in mandatory_sources
            if coverage[source.value] != EvidenceStatus.COLLECTED.value
        ]
        decision = GateDecision.PASS
        if unsatisfied:
            decision = (
                GateDecision.BLOCK_SCALE
                if stage is DecisionStage.SCALE
                else GateDecision.HOLD_FOR_RESEARCH
            )

        reasons: List[str] = []
        actions: List[str] = []
        for source in unsatisfied:
            label = cls.SOURCE_LABELS[source]
            status = coverage[source.value]
            reasons.append(f"{label} evidence is {status} for the Egypt gate.")
            selected_errors = selected.get(source, (0, evaluated_at, status, []))[3]
            reasons.extend(f"{label}: {error}" for error in selected_errors)
            actions.append(f"Collect fresh, valid {label} evidence for Egypt.")
        if not unsatisfied:
            reasons.append("All mandatory evidence is fresh and valid for Egypt.")

        if (
            stage is DecisionStage.SCALE
            and coverage[MarketSignalSource.FIRST_PARTY_CAMPAIGN.value]
            == EvidenceStatus.COLLECTED.value
        ):
            campaign = selected_records[MarketSignalSource.FIRST_PARTY_CAMPAIGN]
            delivered_orders = campaign.metrics.get("delivered_orders")
            delivered_profit = campaign.metrics.get("delivered_profit")
            metric_errors: List[str] = []
            if delivered_orders is None:
                metric_errors.append("delivered_orders is required for SCALE")
            else:
                try:
                    delivered_orders_number = float(delivered_orders)
                except (TypeError, ValueError):
                    metric_errors.append("delivered_orders must be numeric for SCALE")
                else:
                    if delivered_orders_number <= 0:
                        metric_errors.append(
                            "delivered_orders must be positive for SCALE"
                        )
            if delivered_profit is None:
                metric_errors.append("delivered_profit is required for SCALE")
            else:
                try:
                    delivered_profit_number = float(delivered_profit)
                except (TypeError, ValueError):
                    metric_errors.append("delivered_profit must be numeric for SCALE")
                else:
                    if delivered_profit_number <= 0:
                        metric_errors.append(
                            "delivered_profit must be positive for SCALE"
                        )
            if metric_errors:
                decision = GateDecision.BLOCK_SCALE
                reasons.extend(metric_errors)
                actions.append(
                    "Collect fresh first-party delivered-order and positive-profit evidence."
                )

        directional_sources: Dict[str, List[str]] = {"positive": [], "negative": []}
        positive_labels = {"positive", "high", "rising", "strong", "up"}
        negative_labels = {"negative", "low", "falling", "weak", "down"}
        for source, record in selected_records.items():
            if freshness[source.value] != "FRESH":
                continue
            direction = str(record.metrics.get("signal_direction", "")).casefold()
            if direction in positive_labels:
                directional_sources["positive"].append(cls.SOURCE_LABELS[source])
            elif direction in negative_labels:
                directional_sources["negative"].append(cls.SOURCE_LABELS[source])
        contradictions: List[str] = []
        if directional_sources["positive"] and directional_sources["negative"]:
            contradictions.append(
                "Conflicting signal directions: positive from "
                + ", ".join(directional_sources["positive"])
                + "; negative from "
                + ", ".join(directional_sources["negative"])
                + ". Signals were preserved separately and not averaged."
            )

        return MarketSignalGateResult(
            decision=decision,
            stage=stage,
            coverage_status_by_source=coverage,
            freshness_status_by_source=freshness,
            contradictions=contradictions,
            reasons=reasons,
            required_actions=actions,
            evidence_snapshot=snapshots,
        )
