"""Pure report renderer. Returns a list of strings for the panel to draw."""

from . import models

_VERDICT_TEXT = {
    models.Verdict.READY: "READY FOR DELIVERY",
    models.Verdict.READY_WITH_WARNINGS: "READY WITH WARNINGS",
    models.Verdict.NOT_READY: "NOT READY FOR DELIVERY",
}

_STATUS_TOKEN = {
    models.Status.PASS: "PASS",
    models.Status.WARNING: "WARN",
    models.Status.FAIL: "FAIL",
}

_APPLIED_SCALE_ID = "03_applied_scale"
_APPLIED_SCALE_WHY = (
    "Unapplied object scale can cause incorrect asset size "
    "after export or import."
)
_APPLIED_SCALE_FIX = ("Object Mode", "Ctrl+A", "Apply Scale")
_APPLIED_SCALE_NOTE = (
    "This check detects Object Mode scale only.",
    "Edit Mode geometry scaling does not count as unapplied object scale.",
)
_APPLIED_SCALE_PASS = "All inspected mesh objects have Object Scale = 1,1,1."

_UV_EXISTENCE_ID = "04_uv_existence"
_UV_EXISTENCE_FIX = (
    "Edit Mode → U → UV Unwrap",
    "or add a UV Map before export.",
)
_UV_EXISTENCE_NOTE = (
    "This check verifies UV existence only.",
    "It does not validate UV quality, overlap, texel density, "
    "or layout correctness.",
)
_UV_EXISTENCE_PASS = "All inspected mesh objects have a UV map."


def _applied_scale_detail(result):
    """Detailed, artist-readable block for the Applied Scale check."""
    lines = ["", f"{result.name}: {_STATUS_TOKEN[result.status]}", ""]

    if result.status == models.Status.PASS:
        lines.append(_APPLIED_SCALE_PASS)
        return lines

    lines.append("Affected Objects:")
    for name in result.affected_objects:
        lines.append(f"- {name}")
    lines.append("")

    lines.append("Current Scale:")
    if len(result.issues) == 1:
        lines.extend(result.issues[0].detail.split("\n"))
    else:
        for issue in result.issues:
            lines.append(f"{issue.object_name}:")
            lines.extend(f"  {axis}" for axis in issue.detail.split("\n"))
    lines.append("")

    lines.append("Why it matters:")
    lines.append(_APPLIED_SCALE_WHY)
    lines.append("")

    lines.append("Fix:")
    lines.append(_APPLIED_SCALE_FIX[0])
    for step in _APPLIED_SCALE_FIX[1:]:
        lines.append(f"→ {step}")
    lines.append("")

    lines.append("Note:")
    lines.extend(_APPLIED_SCALE_NOTE)
    return lines


def _uv_existence_detail(result):
    """Detailed, artist-readable block for the UV Existence check."""
    lines = ["", f"{result.name}: {_STATUS_TOKEN[result.status]}", ""]

    if result.status == models.Status.PASS:
        lines.append(_UV_EXISTENCE_PASS)
        return lines

    lines.append("Affected Objects:")
    for issue in result.issues:
        lines.append(f"- {issue.object_name}")
        lines.append(f"  {issue.reason}")
    lines.append("")

    lines.append("Fix:")
    lines.extend(_UV_EXISTENCE_FIX)
    lines.append("")

    lines.append("Note:")
    lines.extend(_UV_EXISTENCE_NOTE)
    return lines


def render(inspection_result):
    lines = [
        _VERDICT_TEXT[inspection_result.verdict],
        f"Score: {inspection_result.score}",
        f"{inspection_result.blocker_count} Blocking Issue(s)",
        f"{inspection_result.warning_count} Warning(s)",
        "",
        "Checks:",
    ]
    for r in inspection_result.results:
        token = _STATUS_TOKEN[r.status]
        lines.append(f"{token}  {r.id}  {r.name}")
    for r in inspection_result.results:
        if r.id == _APPLIED_SCALE_ID:
            lines.extend(_applied_scale_detail(r))
        elif r.id == _UV_EXISTENCE_ID:
            lines.extend(_uv_existence_detail(r))
    if inspection_result.total_objects_inspected:
        lines.append("")
        lines.append(
            f"Inspected {inspection_result.total_objects_inspected} mesh object(s)"
        )
    lines.append(
        f"Generated {inspection_result.generated_at.isoformat(timespec='seconds')} "
        f"on Blender {inspection_result.blender_version}"
    )
    return lines
