"""Tests for Check 03 — Applied Scale (pipeline_inspector/checks/transforms.py)."""

from pipeline_inspector import constants, models
from pipeline_inspector.checks import transforms


class FakeObject:
    """Stand-in for a Blender mesh object exposing only scale/delta_scale/name."""

    def __init__(self, name, scale=(1.0, 1.0, 1.0), delta_scale=(1.0, 1.0, 1.0)):
        self.name = name
        self.scale = scale
        self.delta_scale = delta_scale


def _run(objs):
    return transforms.run({"mesh_objects": objs})


def test_scale_is_applied_identity():
    assert transforms.scale_is_applied((1.0, 1.0, 1.0), (1.0, 1.0, 1.0))


def test_scale_is_applied_within_epsilon():
    near = 1.0 + constants.SCALE_EPSILON / 2
    assert transforms.scale_is_applied((near, near, near), (1.0, 1.0, 1.0))


def test_scale_is_applied_rejects_outside_epsilon():
    off = 1.0 + constants.SCALE_EPSILON * 2
    assert not transforms.scale_is_applied((off, 1.0, 1.0), (1.0, 1.0, 1.0))


def test_scale_is_applied_rejects_nonidentity_delta():
    assert not transforms.scale_is_applied((1.0, 1.0, 1.0), (2.0, 1.0, 1.0))


def test_empty_scene_passes():
    result = _run([])
    assert result.status == models.Status.PASS
    assert result.message == "All mesh objects have applied scale."
    assert result.affected_objects == []
    assert result.issues == []


def test_all_applied_passes():
    result = _run([FakeObject("Cube"), FakeObject("Plane")])
    assert result.status == models.Status.PASS
    assert result.severity == models.Severity.BLOCKER


def test_single_unapplied_fails():
    result = _run([FakeObject("Cube", scale=(2.0, 2.0, 2.0))])
    assert result.status == models.Status.FAIL
    assert result.severity == models.Severity.BLOCKER
    assert result.affected_objects == ["Cube"]
    assert result.message == "1 object(s) have unapplied scale: Cube."
    assert len(result.issues) == 1
    assert result.issues[0].object_name == "Cube"


def test_issue_detail_holds_display_scale_axes():
    result = _run([FakeObject("Cube", scale=(2.0, 0.5, 1.0))])
    assert result.issues[0].detail == "X: 2.0\nY: 0.5\nZ: 1.0"


def test_unapplied_delta_scale_fails():
    result = _run([FakeObject("Cube", delta_scale=(1.0, 0.5, 1.0))])
    assert result.status == models.Status.FAIL
    assert result.affected_objects == ["Cube"]


def test_affected_objects_sorted_and_mixed():
    objs = [
        FakeObject("zebra", scale=(3.0, 3.0, 3.0)),
        FakeObject("alpha", scale=(0.5, 0.5, 0.5)),
        FakeObject("clean"),
    ]
    result = _run(objs)
    assert result.status == models.Status.FAIL
    assert result.affected_objects == ["alpha", "zebra"]
    assert result.message == "2 object(s) have unapplied scale: alpha, zebra."


def test_affected_objects_cap_and_overflow():
    cap = constants.AFFECTED_OBJECTS_CAP
    objs = [
        FakeObject(f"obj_{i:03d}", scale=(2.0, 2.0, 2.0))
        for i in range(cap + 5)
    ]
    result = _run(objs)
    assert result.status == models.Status.FAIL
    assert len(result.affected_objects) == cap
    assert f"(... and {5} more)" in result.message
    assert result.message.startswith(f"{cap + 5} object(s) have unapplied scale:")
