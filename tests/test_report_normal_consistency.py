"""Tests for the Normal Consistency detail block in pipeline_inspector/report.py."""

from datetime import datetime

from pipeline_inspector import models, report
from pipeline_inspector.checks import normals


class FakePolygon:
    def __init__(self, vertices):
        self.vertices = tuple(vertices)


class FakeMesh:
    def __init__(self, faces, has_custom_normals=False):
        self.polygons = [FakePolygon(f) for f in faces]
        self.has_custom_normals = has_custom_normals


class FakeObject:
    def __init__(self, name, mesh):
        self.name = name
        self.data = mesh


_CONSISTENT = [(0, 1, 2), (2, 1, 3)]
_INCONSISTENT = [(0, 1, 2), (1, 2, 3)]
_NONMANIFOLD = [(0, 1, 2), (2, 1, 3), (1, 2, 4)]


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
    check_result = normals.run({"mesh_objects": objs})
    return report.render(_result_with(check_result, verdict))


def test_pass_shows_consistency_message():
    lines = _render(
        [FakeObject("Cube", FakeMesh(_CONSISTENT))], verdict=models.Verdict.READY
    )
    assert "Normal Consistency: PASS" in lines
    assert "Face winding is consistent across all inspected meshes." in lines


def test_fail_block_contents():
    lines = _render([FakeObject("Suzanne", FakeMesh(_INCONSISTENT))])
    assert "Normal Consistency: FAIL" in lines
    assert "1 object(s) have inconsistent face winding: Suzanne." in lines
    assert "Affected Objects:" in lines
    assert "- Suzanne" in lines
    assert "  Inconsistent face winding within a manifold component." in lines
    assert "Fix:" in lines
    assert "Note:" in lines
    assert any("inward vs outward" in ln for ln in lines)


def test_warning_skip_block_shows_reason():
    obj = FakeObject("Hero", FakeMesh(_CONSISTENT, has_custom_normals=True))
    lines = _render([obj], verdict=models.Verdict.READY_WITH_WARNINGS)
    assert "Normal Consistency: WARN" in lines
    assert "1 object(s) skipped; winding not checked: Hero." in lines


def test_pass_with_nonmanifold_note_shows_message():
    lines = _render(
        [FakeObject("Sculpt", FakeMesh(_NONMANIFOLD))], verdict=models.Verdict.READY
    )
    assert "Normal Consistency: PASS" in lines
    assert any("non-manifold" in ln for ln in lines)


def test_fail_block_appears_after_checks_summary():
    lines = _render([FakeObject("Suzanne", FakeMesh(_INCONSISTENT))])
    assert lines.index("Checks:") < lines.index("Normal Consistency: FAIL")
