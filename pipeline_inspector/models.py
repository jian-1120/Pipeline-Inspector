"""Plain-data records for inspection results. No bpy import. No methods."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List


class Status(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"


class Severity(str, Enum):
    BLOCKER = "BLOCKER"
    WARNING = "WARNING"
    INFO = "INFO"


class Verdict(str, Enum):
    READY = "READY"
    READY_WITH_WARNINGS = "READY_WITH_WARNINGS"
    NOT_READY = "NOT_READY"


@dataclass
class IssueRecord:
    check_id: str
    severity: Severity
    object_name: str
    reason: str
    detail: str = ""


@dataclass
class CheckResult:
    id: str
    name: str
    status: Status
    severity: Severity
    message: str
    affected_objects: List[str] = field(default_factory=list)
    evidence_reason: str = ""
    issues: List[IssueRecord] = field(default_factory=list)


@dataclass
class InspectionResult:
    results: List[CheckResult]
    score: int
    verdict: Verdict
    blocker_count: int
    warning_count: int
    generated_at: datetime
    blender_version: str
    total_objects_inspected: int = 0
