"""Tests for the Applied Scale detail block in pipeline_inspector/report.py."""

from datetime import datetime

from pipeline_inspector import models, report
from pipeline_inspector.checks import transforms


class FakeObject:
    def __init__(self, name, scale=(1.0, 1.0, 1.0), delta_scale=(1.0, 1.0, 1.0)):
        self.name = name
        self.scale = scale
        self.delta_scale = delta_scale


def _result_with(check_result, verdict=models.Verdict.NOT_READY):
    return models.InspectionResult(
        results=[check_result],
        score=0,
        verdict=verdict,
        blocker_count=1,
        warning_count=0,
        generated_at=datetime(2026, 6, 8, 12, 0, 0),
        blender_version="4.2.0",
        total_objects_inspected=1,
    )


def _render(objs, verdict=models.Verdict.NOT_READY):
    check_result = transforms.run({"mesh_objects": objs})
    return report.render(_result_with(check_result, verdict))


def test_pass_shows_object_scale_identity_message():
    lines = _render([FakeObject("Cube")], verdict=models.Verdict.READY)
    assert "Applied Scale: PASS" in lines
    assert "All inspected mesh objects have Object Scale = 1,1,1." in lines


def test_fail_single_object_block_contents():
    lines = _render([FakeObject("Suzanne", scale=(2.0, 2.0, 2.0))])
    assert "Applied Scale: FAIL" in lines
    assert "Affected Objects:" in lines
    assert "- Suzanne" in lines
    assert "Current Scale:" in lines
    assert "X: 2.0" in lines
    assert "Y: 2.0" in lines
    assert "Z: 2.0" in lines
    assert "Why it matters:" in lines
    assert (
        "Unapplied object scale can cause incorrect asset size "
        "after export or import."
    ) in lines
    assert "Fix:" in lines
    assert "Object Mode" in lines
    assert "→ Ctrl+A" in lines
    assert "→ Apply Scale" in lines
    assert "Note:" in lines
    assert "This check detects Object Mode scale only." in lines


def test_fail_multiple_objects_label_each_scale():
    lines = _render(
        [
            FakeObject("Suzanne", scale=(2.0, 2.0, 2.0)),
            FakeObject("Cube", scale=(0.5, 1.0, 1.0)),
        ]
    )
    assert "Affected Objects:" in lines
    assert "- Cube" in lines
    assert "- Suzanne" in lines
    assert "Suzanne:" in lines
    assert "  X: 2.0" in lines
    assert "Cube:" in lines
    assert "  X: 0.5" in lines


def test_fail_block_appears_after_checks_summary():
    lines = _render([FakeObject("Suzanne", scale=(2.0, 2.0, 2.0))])
    assert lines.index("Checks:") < lines.index("Applied Scale: FAIL")
