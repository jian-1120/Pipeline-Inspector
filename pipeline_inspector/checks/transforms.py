"""Check 03 — Applied Scale.

FAILs any visible non-linked mesh object whose scale or delta_scale differs
from (1, 1, 1) beyond SCALE_EPSILON. Read-only; binary (no WARNING state).
"""

from .. import constants, models
from . import base

CHECK_ID = "03_applied_scale"
CHECK_NAME = "Applied Scale"
SEVERITY = models.Severity.BLOCKER

_PASS_MESSAGE = "All mesh objects have applied scale."


def _is_identity(components):
    return all(abs(c - 1.0) <= constants.SCALE_EPSILON for c in components)


def scale_is_applied(scale, delta_scale):
    """Pure predicate over two 3-component sequences of floats."""
    return _is_identity(scale) and _is_identity(delta_scale)


def run(inputs):
    offenders = []
    issues = []

    for obj in inputs["mesh_objects"]:
        if scale_is_applied(obj.scale, obj.delta_scale):
            continue
        offenders.append(obj.name)
        issues.append(
            models.IssueRecord(
                check_id=CHECK_ID,
                severity=SEVERITY,
                object_name=obj.name,
                reason="Object has unapplied scale.",
                detail=(
                    f"scale=({obj.scale[0]:.4f}, {obj.scale[1]:.4f}, {obj.scale[2]:.4f}) "
                    f"delta_scale=({obj.delta_scale[0]:.4f}, "
                    f"{obj.delta_scale[1]:.4f}, {obj.delta_scale[2]:.4f})"
                ),
            )
        )

    if not offenders:
        return base.make_pass(CHECK_ID, CHECK_NAME, SEVERITY, _PASS_MESSAGE)

    capped, overflow = base.dedupe_sort_cap(offenders)
    names = ", ".join(capped)
    if overflow:
        names = f"{names} (... and {overflow} more)"
    message = f"{len(set(offenders))} object(s) have unapplied scale: {names}."

    return base.make_fail(
        CHECK_ID, CHECK_NAME, SEVERITY, message, offenders, issues
    )
