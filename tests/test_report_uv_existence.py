"""Tests for the UV Existence detail block in pipeline_inspector/report.py."""

from datetime import datetime

from pipeline_inspector import models, report
from pipeline_inspector.checks import uvs


class FakeUVLayer:
    def __init__(self, loop_count=3):
        self.data = [object() for _ in range(loop_count)]


class FakeUVLayers:
    def __init__(self, layers=None):
        self._layers = list(layers) if layers else []
        self.active = self._layers[0] if self._layers else None

    def __len__(self):
        return len(self._layers)


class FakeMesh:
    def __init__(self, uv_layers):
        self.uv_layers = uv_layers


class FakeObject:
    def __init__(self, name, uv_layers=None):
        self.name = name
        self.data = FakeMesh(uv_layers)


def _with_uv(name):
    return FakeObject(name, FakeUVLayers([FakeUVLayer(loop_count=4)]))


def _no_uv(name):
    return FakeObject(name, FakeUVLayers([]))


def _empty_uv(name):
    return FakeObject(name, FakeUVLayers([FakeUVLayer(loop_count=0)]))


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
    check_result = uvs.run({"mesh_objects": objs})
    return report.render(_result_with(check_result, verdict))


def test_pass_shows_uv_identity_message():
    lines = _render([_with_uv("Cube")], verdict=models.Verdict.READY)
    assert "UV Existence: PASS" in lines
    assert "All inspected mesh objects have a UV map." in lines


def test_fail_block_contents():
    lines = _render([_no_uv("Suzanne")])
    assert "UV Existence: FAIL" in lines
    assert "Affected Objects:" in lines
    assert "- Suzanne" in lines
    assert "  Object has no UV map." in lines
    assert "Fix:" in lines
    assert "Edit Mode → U → UV Unwrap" in lines
    assert "or add a UV Map before export." in lines
    assert "Note:" in lines
    assert "This check verifies UV existence only." in lines


def test_fail_empty_uv_reason_shown():
    lines = _render([_empty_uv("Plane")])
    assert "- Plane" in lines
    assert "  UV map exists but contains no UV data." in lines


def test_fail_block_appears_after_checks_summary():
    lines = _render([_no_uv("Suzanne")])
    assert lines.index("Checks:") < lines.index("UV Existence: FAIL")
