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
    models.Status.NOT_IMPLEMENTED: "SKIP",
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

_TEXTURE_PRESENCE_ID = "01_texture_presence"
_TEXTURE_PRESENCE_FIX = (
    "Pack textures via File → External Data → Pack Resources,",
    "or restore the missing files at their referenced paths before export.",
)
_TEXTURE_PRESENCE_NOTE = (
    "This check verifies texture reachability only.",
    "It does not validate texture resolution, color space, or UV layout.",
)
_TEXTURE_PRESENCE_PASS = "All referenced textures are packed or reachable."

_MATERIAL_ASSIGNMENT_ID = "02_material_assignment"
_MATERIAL_ASSIGNMENT_FIX = (
    "Assign a material in the Material Properties tab,",
    "and connect a shader node to the Material Output Surface input,",
    "or remove unused empty material slots before export.",
)
_MATERIAL_ASSIGNMENT_NOTE = (
    "This check verifies material assignment and surface connectivity only.",
    "It does not validate shader quality, PBR correctness, or texture content.",
)
_MATERIAL_ASSIGNMENT_PASS = (
    "All inspected mesh objects have export-relevant materials."
)

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

_NORMAL_CONSISTENCY_ID = "05_normal_consistency"
_NORMAL_CONSISTENCY_FIX = (
    "Edit Mode → select all → Mesh → Normals → Recalculate Outside,",
    "then re-check before export.",
)
_NORMAL_CONSISTENCY_NOTE = (
    "This check flags contradictory face winding inside manifold components only.",
    "It does not judge inward vs outward orientation, and it skips "
    "non-manifold components, custom-normal meshes, and meshes over 500k polygons.",
)
_NORMAL_CONSISTENCY_PASS = (
    "Face winding is consistent across all inspected meshes."
)


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


def _texture_presence_detail(result):
    """Detailed, artist-readable block for the Texture Presence check."""
    lines = ["", f"{result.name}: {_STATUS_TOKEN[result.status]}", ""]

    if result.status == models.Status.PASS:
        lines.append(_TEXTURE_PRESENCE_PASS)
        return lines

    if result.status == models.Status.WARNING:
        lines.append(result.message)
        return lines

    lines.append(result.message)
    lines.append("")
    lines.append("Affected Objects:")
    for name in result.affected_objects:
        lines.append(f"- {name}")
    lines.append("")

    lines.append("Fix:")
    lines.extend(_TEXTURE_PRESENCE_FIX)
    lines.append("")

    lines.append("Note:")
    lines.extend(_TEXTURE_PRESENCE_NOTE)
    return lines


def _material_assignment_detail(result):
    """Detailed, artist-readable block for the Material Assignment check."""
    lines = ["", f"{result.name}: {_STATUS_TOKEN[result.status]}", ""]

    if result.status == models.Status.PASS:
        lines.append(_MATERIAL_ASSIGNMENT_PASS)
        return lines

    lines.append(result.message)
    lines.append("")
    lines.append("Affected Objects:")
    for issue in result.issues:
        lines.append(f"- {issue.object_name}")
        lines.append(f"  {issue.reason}")
    lines.append("")

    lines.append("Fix:")
    lines.extend(_MATERIAL_ASSIGNMENT_FIX)
    lines.append("")

    lines.append("Note:")
    lines.extend(_MATERIAL_ASSIGNMENT_NOTE)
    return lines


def _normal_consistency_detail(result):
    """Detailed, artist-readable block for the Normal Consistency check.

    PASS may carry an informational non-manifold note in its message; WARN is
    the skip path (custom normals / oversize) and shows its skip reason only.
    """
    lines = ["", f"{result.name}: {_STATUS_TOKEN[result.status]}", ""]

    if result.status == models.Status.PASS:
        lines.append(result.message or _NORMAL_CONSISTENCY_PASS)
        return lines

    if result.status == models.Status.WARNING:
        lines.append(result.message)
        return lines

    lines.append(result.message)
    lines.append("")
    lines.append("Affected Objects:")
    for issue in result.issues:
        lines.append(f"- {issue.object_name}")
        lines.append(f"  {issue.reason}")
    lines.append("")

    lines.append("Fix:")
    lines.extend(_NORMAL_CONSISTENCY_FIX)
    lines.append("")

    lines.append("Note:")
    lines.extend(_NORMAL_CONSISTENCY_NOTE)
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
        if r.status == models.Status.NOT_IMPLEMENTED:
            lines.append(f"{token}  {r.id}  {r.name} — {r.message}")
        else:
            lines.append(f"{token}  {r.id}  {r.name}")
    for r in inspection_result.results:
        if r.id == _APPLIED_SCALE_ID:
            lines.extend(_applied_scale_detail(r))
        elif r.id == _UV_EXISTENCE_ID:
            lines.extend(_uv_existence_detail(r))
        elif r.id == _TEXTURE_PRESENCE_ID:
            lines.extend(_texture_presence_detail(r))
        elif r.id == _MATERIAL_ASSIGNMENT_ID:
            lines.extend(_material_assignment_detail(r))
        elif r.id == _NORMAL_CONSISTENCY_ID:
            lines.extend(_normal_consistency_detail(r))
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
