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
