"""Tests for Check 04 — UV Existence (pipeline_inspector/checks/uvs.py)."""

from pipeline_inspector import constants, models
from pipeline_inspector.checks import uvs


class FakeUVLayer:
    def __init__(self, loop_count=3):
        self.data = [object() for _ in range(loop_count)]


class FakeUVLayers:
    """Stand-in for mesh.uv_layers: a sized collection with an .active layer."""

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


def _run(objs):
    return uvs.run({"mesh_objects": objs})


def test_uv_status_present_returns_none():
    assert uvs.uv_status(_with_uv("Cube")) is None


def test_uv_status_no_map():
    assert uvs.uv_status(_no_uv("Cube")) == "Object has no UV map."


def test_uv_status_empty_map():
    assert (
        uvs.uv_status(_empty_uv("Cube"))
        == "UV map exists but contains no UV data."
    )


def test_empty_scene_passes():
    result = _run([])
    assert result.status == models.Status.PASS
    assert result.message == "All mesh objects have UV maps."
    assert result.affected_objects == []
    assert result.issues == []


def test_all_uv_present_passes():
    result = _run([_with_uv("Cube"), _with_uv("Plane")])
    assert result.status == models.Status.PASS
    assert result.severity == models.Severity.BLOCKER


def test_single_no_uv_fails():
    result = _run([_no_uv("Cube")])
    assert result.status == models.Status.FAIL
    assert result.severity == models.Severity.BLOCKER
    assert result.affected_objects == ["Cube"]
    assert result.message == "1 object(s) have no usable UV map: Cube."
    assert len(result.issues) == 1
    assert result.issues[0].object_name == "Cube"
    assert result.issues[0].reason == "Object has no UV map."


def test_single_empty_uv_fails():
    result = _run([_empty_uv("Cube")])
    assert result.status == models.Status.FAIL
    assert result.affected_objects == ["Cube"]
    assert result.issues[0].reason == "UV map exists but contains no UV data."


def test_mixed_objects_fail_only_offenders():
    objs = [
        _with_uv("Good"),
        _no_uv("zebra"),
        _empty_uv("alpha"),
    ]
    result = _run(objs)
    assert result.status == models.Status.FAIL
    assert result.affected_objects == ["alpha", "zebra"]
    assert result.message == "2 object(s) have no usable UV map: alpha, zebra."


def test_affected_objects_sorted():
    objs = [_no_uv("zebra"), _no_uv("alpha"), _no_uv("mango")]
    result = _run(objs)
    assert result.affected_objects == ["alpha", "mango", "zebra"]


def test_affected_objects_cap_and_overflow():
    cap = constants.AFFECTED_OBJECTS_CAP
    objs = [_no_uv(f"obj_{i:03d}") for i in range(cap + 5)]
    result = _run(objs)
    assert result.status == models.Status.FAIL
    assert len(result.affected_objects) == cap
    assert "(... and 5 more)" in result.message
    assert result.message.startswith(f"{cap + 5} object(s) have no usable UV map:")
