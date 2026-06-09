"""Tests for placeholder checks (01 Texture, 02 Material, 05 Normal).

Placeholder checks must not present as PASS. They emit a NOT_IMPLEMENTED
status with INFO severity so the report shows them as skipped and the
READY FOR DELIVERY score/verdict is never influenced by a check that did
not actually inspect anything.
"""

from datetime import datetime

from pipeline_inspector import models, report, scoring
from pipeline_inspector.checks import materials, normals

PLACEHOLDERS = [materials, normals]


def _run(mod):
    return mod.run({"mesh_objects": []})


def test_placeholders_are_not_pass():
    for mod in PLACEHOLDERS:
        result = _run(mod)
        assert result.status == models.Status.NOT_IMPLEMENTED
        assert result.status != models.Status.PASS


def test_placeholders_use_info_severity():
    for mod in PLACEHOLDERS:
        assert _run(mod).severity == models.Severity.INFO


def test_placeholder_message_states_not_implemented():
    for mod in PLACEHOLDERS:
        result = _run(mod)
        assert "Not implemented" in result.message
        assert result.message != "Placeholder PASS — check not yet implemented."


def test_placeholders_carry_no_issues_or_affected_objects():
    for mod in PLACEHOLDERS:
        result = _run(mod)
        assert result.affected_objects == []
        assert result.issues == []


def test_placeholders_do_not_change_score_or_verdict():
    results = [_run(mod) for mod in PLACEHOLDERS]
    score, verdict, blocker_count, warning_count = scoring.derive(results)
    assert score == 100
    assert verdict == models.Verdict.READY
    assert blocker_count == 0
    assert warning_count == 0


def test_placeholder_does_not_count_as_blocker_alongside_a_real_fail():
    failing = models.CheckResult(
        id="03_applied_scale",
        name="Applied Scale",
        status=models.Status.FAIL,
        severity=models.Severity.BLOCKER,
        message="x",
    )
    results = [_run(materials), failing]
    score, verdict, blocker_count, warning_count = scoring.derive(results)
    assert blocker_count == 1
    assert score == 85
    assert verdict == models.Verdict.NOT_READY


def _result_with(check_results):
    return models.InspectionResult(
        results=check_results,
        score=100,
        verdict=models.Verdict.READY,
        blocker_count=0,
        warning_count=0,
        generated_at=datetime(2026, 6, 8, 12, 0, 0),
        blender_version="4.2.0",
        total_objects_inspected=0,
    )


def test_report_renders_skip_token_not_pass():
    lines = report.render(_result_with([_run(materials)]))
    summary = [ln for ln in lines if "02_material_assignment" in ln]
    assert len(summary) == 1
    assert summary[0].startswith("SKIP")
    assert "PASS" not in summary[0]


def test_report_summary_line_explains_skip():
    lines = report.render(_result_with([_run(materials)]))
    summary = [ln for ln in lines if "02_material_assignment" in ln][0]
    assert "Not implemented" in summary


def test_report_does_not_crash_on_not_implemented_status():
    lines = report.render(
        _result_with([_run(materials), _run(normals)])
    )
    assert any("05_normal_consistency" in ln for ln in lines)
