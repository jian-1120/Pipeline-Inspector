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

    def __iter__(self):
        return iter(self._layers)


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


# --- Degenerate active UV layer WARNING path -------------------------------

EPS = constants.UV_BBOX_EPSILON


class FakeLoop:
    def __init__(self, uv):
        self.uv = uv


class CoordUVLayer:
    """UV layer whose per-loop .uv coordinates are explicit (u, v) tuples."""

    def __init__(self, coords):
        self.data = [FakeLoop(c) for c in coords]


def _spread_layer():
    """A non-degenerate layer: UVs spread across the unit square."""
    return CoordUVLayer([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)])


def _collapsed_layer():
    """A degenerate layer: every UV collapsed onto a single point."""
    return CoordUVLayer([(0.5, 0.5), (0.5, 0.5), (0.5, 0.5)])


def _multi_layer_obj(name, layers):
    return FakeObject(name, FakeUVLayers(layers))


def test_degenerate_active_with_good_alternative_warns():
    # active (first) layer is collapsed; a second layer has real data.
    obj = _multi_layer_obj("prop_01", [_collapsed_layer(), _spread_layer()])
    result = _run([obj])
    assert result.status == models.Status.WARNING
    assert result.severity == models.Severity.WARNING
    assert result.affected_objects == ["prop_01"]
    assert result.message == (
        "1 object(s) have a degenerate active UV layer: prop_01."
    )
    assert len(result.issues) == 1
    assert result.issues[0].object_name == "prop_01"
    assert (
        result.issues[0].reason
        == "Active UV layer appears unused; another layer has data."
    )


def test_degenerate_active_single_layer_does_not_warn():
    # Only one layer present: spec WARNING requires an alternative layer.
    obj = _multi_layer_obj("solo", [_collapsed_layer()])
    result = _run([obj])
    assert result.status == models.Status.PASS


def test_all_layers_degenerate_does_not_warn():
    # No non-degenerate alternative exists, so the WARNING does not fire.
    obj = _multi_layer_obj("flat", [_collapsed_layer(), _collapsed_layer()])
    result = _run([obj])
    assert result.status == models.Status.PASS


def test_active_non_degenerate_passes():
    # Active layer has spread; a degenerate secondary layer is irrelevant.
    obj = _multi_layer_obj("ok", [_spread_layer(), _collapsed_layer()])
    result = _run([obj])
    assert result.status == models.Status.PASS


def test_fail_takes_precedence_over_warning():
    bad = _no_uv("missing")
    warn = _multi_layer_obj("degen", [_collapsed_layer(), _spread_layer()])
    result = _run([bad, warn])
    assert result.status == models.Status.FAIL
    assert result.severity == models.Severity.BLOCKER
    assert result.affected_objects == ["missing"]


def test_degenerate_active_classifier_pure():
    obj = _multi_layer_obj("prop_01", [_collapsed_layer(), _spread_layer()])
    assert (
        uvs.degenerate_active_status(obj)
        == "Active UV layer appears unused; another layer has data."
    )
    assert uvs.degenerate_active_status(_with_uv("Cube")) is None


def test_degenerate_warning_sorted_and_counted():
    objs = [
        _multi_layer_obj("zebra", [_collapsed_layer(), _spread_layer()]),
        _multi_layer_obj("alpha", [_collapsed_layer(), _spread_layer()]),
    ]
    result = _run(objs)
    assert result.status == models.Status.WARNING
    assert result.affected_objects == ["alpha", "zebra"]
    assert result.message == (
        "2 object(s) have a degenerate active UV layer: alpha, zebra."
    )
