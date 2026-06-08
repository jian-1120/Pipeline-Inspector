"""Check 04 — UV Existence.

FAILs any visible non-linked mesh object that has no UV map, or whose active
UV map exists but contains no UV data (BLOCKER). Additionally WARNs when a
mesh has multiple UV layers, its active layer is degenerate (collapsed to a
point), but a non-active layer carries usable UV data. Read-only.
"""

from .. import constants, models
from . import base

CHECK_ID = "04_uv_existence"
CHECK_NAME = "UV Existence"
SEVERITY = models.Severity.BLOCKER

_PASS_MESSAGE = "All mesh objects have UV maps."
_REASON_NO_MAP = "Object has no UV map."
_REASON_EMPTY_MAP = "UV map exists but contains no UV data."
_REASON_DEGENERATE_ACTIVE = (
    "Active UV layer appears unused; another layer has data."
)


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


def _layer_is_degenerate(layer):
    """True when a UV layer's per-loop bounding box is below epsilon on all axes.

    Degenerate means every UV coordinate collapses onto a single point (the
    common "default unwrap left at origin" failure). An empty layer is treated
    as non-degenerate here; the empty-map case is owned by uv_status/FAIL.
    """
    coords = [loop.uv for loop in layer.data]
    if not coords:
        return False
    us = [c[0] for c in coords]
    vs = [c[1] for c in coords]
    span_u = max(us) - min(us)
    span_v = max(vs) - min(vs)
    return (
        span_u <= constants.UV_BBOX_EPSILON
        and span_v <= constants.UV_BBOX_EPSILON
    )


def degenerate_active_status(obj):
    """Pure classifier for the WARNING path. Returns a reason or None.

    Only meaningful when uv_status(obj) is None (a usable active layer exists).
    Returns the degenerate-active reason when the mesh has more than one UV
    layer, the active layer is degenerate, and at least one non-active layer is
    non-degenerate. Otherwise None.
    """
    mesh = obj.data
    uv_layers = getattr(mesh, "uv_layers", None)
    if not uv_layers or len(uv_layers) <= 1:
        return None

    active = getattr(uv_layers, "active", None)
    if active is None or not _layer_is_degenerate(active):
        return None

    others = [ly for ly in uv_layers if ly is not active]
    if any(len(ly.data) > 0 and not _layer_is_degenerate(ly) for ly in others):
        return _REASON_DEGENERATE_ACTIVE
    return None


def run(inputs):
    offenders = []
    issues = []
    warn_offenders = []
    warn_issues = []

    for obj in inputs["mesh_objects"]:
        reason = uv_status(obj)
        if reason is not None:
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
            continue

        warn_reason = degenerate_active_status(obj)
        if warn_reason is not None:
            warn_offenders.append(obj.name)
            warn_issues.append(
                models.IssueRecord(
                    check_id=CHECK_ID,
                    severity=models.Severity.WARNING,
                    object_name=obj.name,
                    reason=warn_reason,
                    detail=warn_reason,
                )
            )

    if offenders:
        capped, overflow = base.dedupe_sort_cap(offenders)
        names = ", ".join(capped)
        if overflow:
            names = f"{names} (... and {overflow} more)"
        message = (
            f"{len(set(offenders))} object(s) have no usable UV map: {names}."
        )
        return base.make_fail(
            CHECK_ID, CHECK_NAME, SEVERITY, message, offenders, issues
        )

    if warn_offenders:
        capped, overflow = base.dedupe_sort_cap(warn_offenders)
        names = ", ".join(capped)
        if overflow:
            names = f"{names} (... and {overflow} more)"
        message = (
            f"{len(set(warn_offenders))} object(s) have a degenerate "
            f"active UV layer: {names}."
        )
        return base.make_warning(
            CHECK_ID, CHECK_NAME, message, warn_offenders, warn_issues
        )

    return base.make_pass(CHECK_ID, CHECK_NAME, SEVERITY, _PASS_MESSAGE)
