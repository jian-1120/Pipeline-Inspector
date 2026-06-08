"""Check 04 — UV Existence.

FAILs any visible non-linked mesh object that has no UV map, or whose active
UV map exists but contains no UV data. Read-only; binary (no WARNING state).
"""

from .. import models
from . import base

CHECK_ID = "04_uv_existence"
CHECK_NAME = "UV Existence"
SEVERITY = models.Severity.BLOCKER

_PASS_MESSAGE = "All mesh objects have UV maps."
_REASON_NO_MAP = "Object has no UV map."
_REASON_EMPTY_MAP = "UV map exists but contains no UV data."


def uv_status(obj):
    """Pure classifier. Returns None when UVs are present, else a reason string.

    Reads only object.data.uv_layers and the active layer's per-loop data;
    never mutates the object.
    """
    mesh = obj.data
    uv_layers = getattr(mesh, "uv_layers", None)
    if not uv_layers or len(uv_layers) == 0:
        return _REASON_NO_MAP

    active = getattr(uv_layers, "active", None)
    if active is None or len(active.data) == 0:
        return _REASON_EMPTY_MAP

    return None


def run(inputs):
    offenders = []
    issues = []

    for obj in inputs["mesh_objects"]:
        reason = uv_status(obj)
        if reason is None:
            continue
        offenders.append(obj.name)
        issues.append(
            models.IssueRecord(
                check_id=CHECK_ID,
                severity=SEVERITY,
                object_name=obj.name,
                reason=reason,
                detail=reason,
            )
        )

    if not offenders:
        return base.make_pass(CHECK_ID, CHECK_NAME, SEVERITY, _PASS_MESSAGE)

    capped, overflow = base.dedupe_sort_cap(offenders)
    names = ", ".join(capped)
    if overflow:
        names = f"{names} (... and {overflow} more)"
    message = f"{len(set(offenders))} object(s) have no usable UV map: {names}."

    return base.make_fail(
        CHECK_ID, CHECK_NAME, SEVERITY, message, offenders, issues
    )
