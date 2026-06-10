"""Tests for the NOT_IMPLEMENTED placeholder mechanism.

All five v1 checks are now real (Check 05 Normal Consistency was the last
placeholder). No check module returns NOT_IMPLEMENTED anymore, but the
machinery that renders a placeholder as a skipped, score-neutral result is
retained and still worth covering: a future scaffold check must present as
SKIP, never PASS, and must not influence the READY FOR DELIVERY verdict.

These tests therefore exercise base.make_not_implemented and the report SKIP
token against a synthetic placeholder CheckResult rather than a real module.
"""

from datetime import datetime

from pipeline_inspector import models, report, scoring
from pipeline_inspector.checks import base


def _placeholder():
    return base.make_not_implemented("99_demo_placeholder", "Demo Placeholder")


def test_placeholder_is_not_pass():
    result = _placeholder()
    assert result.status == models.Status.NOT_IMPLEMENTED
    assert result.status != models.Status.PASS


def test_placeholder_uses_info_severity():
    assert _placeholder().severity == models.Severity.INFO


def test_placeholder_message_states_not_implemented():
    result = _placeholder()
    assert "Not implemented" in result.message
    assert result.message != "Placeholder PASS — check not yet implemented."


def test_placeholder_carries_no_issues_or_affected_objects():
    result = _placeholder()
    assert result.affected_objects == []
    assert result.issues == []


def test_placeholder_does_not_change_score_or_verdict():
    score, verdict, blocker_count, warning_count = scoring.derive([_placeholder()])
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
    score, verdict, blocker_count, warning_count = scoring.derive(
        [_placeholder(), failing]
    )
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
    lines = report.render(_result_with([_placeholder()]))
    summary = [ln for ln in lines if "99_demo_placeholder" in ln]
    assert len(summary) == 1
    assert summary[0].startswith("SKIP")
    assert "PASS" not in summary[0]


def test_report_summary_line_explains_skip():
    lines = report.render(_result_with([_placeholder()]))
    summary = [ln for ln in lines if "99_demo_placeholder" in ln][0]
    assert "Not implemented" in summary


def test_report_does_not_crash_on_not_implemented_status():
    lines = report.render(_result_with([_placeholder()]))
    assert any("99_demo_placeholder" in ln for ln in lines)
