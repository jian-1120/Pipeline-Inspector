"""Tests for Check 02 — Material Assignment (pipeline_inspector/checks/materials.py).

Classifiers and run() are exercised with plain fakes so the suite runs under
the bpy stub without touching bpy.data. Fakes model the slice of the Blender
material API the check reads: material_slots, slot.material, use_nodes,
node_tree.nodes, OUTPUT_MATERIAL nodes, and the Surface input socket's
is_linked flag.
"""

from pipeline_inspector import constants, models
from pipeline_inspector.checks import materials


class FakeSocket:
    def __init__(self, name="Surface", is_linked=False):
        self.name = name
        self.is_linked = is_linked


class FakeInputs:
    """Stand-in for node.inputs: subscriptable by socket name and iterable."""

    def __init__(self, sockets):
        self._sockets = {s.name: s for s in sockets}

    def __getitem__(self, key):
        return self._sockets[key]

    def __iter__(self):
        return iter(self._sockets.values())


class FakeNode:
    def __init__(self, node_type, surface_linked=None):
        self.type = node_type
        if surface_linked is None:
            self.inputs = FakeInputs([])
        else:
            self.inputs = FakeInputs([FakeSocket("Surface", surface_linked)])


class FakeNodeTree:
    def __init__(self, nodes):
        self.nodes = nodes


class FakeMaterial:
    def __init__(self, use_nodes=True, node_tree=None):
        self.use_nodes = use_nodes
        self.node_tree = node_tree


class FakeSlot:
    def __init__(self, material):
        self.material = material


class FakeObject:
    def __init__(self, name, materials):
        self.name = name
        self.material_slots = [FakeSlot(m) for m in materials]


# --- builders -------------------------------------------------------------


def _connected_material():
    """Node material with a connected Material Output surface."""
    out = FakeNode("OUTPUT_MATERIAL", surface_linked=True)
    bsdf = FakeNode("BSDF_PRINCIPLED")
    return FakeMaterial(use_nodes=True, node_tree=FakeNodeTree([bsdf, out]))


def _disconnected_material():
    """Node material whose Material Output surface has no incoming link."""
    out = FakeNode("OUTPUT_MATERIAL", surface_linked=False)
    return FakeMaterial(use_nodes=True, node_tree=FakeNodeTree([out]))


def _no_output_material():
    """Node material with no OUTPUT_MATERIAL node at all."""
    bsdf = FakeNode("BSDF_PRINCIPLED")
    return FakeMaterial(use_nodes=True, node_tree=FakeNodeTree([bsdf]))


def _legacy_material():
    """Legacy material with use_nodes off."""
    return FakeMaterial(use_nodes=False, node_tree=None)


def _run(objs):
    return materials.run({"mesh_objects": objs})


# --- classify_material (pure) ---------------------------------------------


def test_classify_connected_is_valid():
    assert materials.classify_material(_connected_material()) == materials._MAT_VALID


def test_classify_disconnected_is_disconnected():
    assert (
        materials.classify_material(_disconnected_material())
        == materials._MAT_DISCONNECTED
    )


def test_classify_no_output_node_is_disconnected():
    assert (
        materials.classify_material(_no_output_material())
        == materials._MAT_DISCONNECTED
    )


def test_classify_legacy_is_legacy():
    assert materials.classify_material(_legacy_material()) == materials._MAT_LEGACY


def test_classify_use_nodes_without_tree_is_disconnected():
    mat = FakeMaterial(use_nodes=True, node_tree=None)
    assert materials.classify_material(mat) == materials._MAT_DISCONNECTED


def test_classify_multiple_outputs_one_connected_is_valid():
    out_a = FakeNode("OUTPUT_MATERIAL", surface_linked=False)
    out_b = FakeNode("OUTPUT_MATERIAL", surface_linked=True)
    mat = FakeMaterial(use_nodes=True, node_tree=FakeNodeTree([out_a, out_b]))
    assert materials.classify_material(mat) == materials._MAT_VALID


# --- material_status (pure) -----------------------------------------------


def test_status_no_slots_fails():
    obj = FakeObject("Cube", [])
    outcome, reason = materials.material_status(obj)
    assert outcome == materials._FAIL
    assert reason == "Object has no material slots."


def test_status_slots_no_material_fails():
    obj = FakeObject("Cube", [None, None])
    outcome, reason = materials.material_status(obj)
    assert outcome == materials._FAIL
    assert reason == "Object has material slots but none are assigned."


def test_status_all_disconnected_fails():
    obj = FakeObject("Cube", [_disconnected_material()])
    outcome, reason = materials.material_status(obj)
    assert outcome == materials._FAIL
    assert reason == "Assigned material has a disconnected surface output."


def test_status_connected_passes():
    obj = FakeObject("Cube", [_connected_material()])
    outcome, reason = materials.material_status(obj)
    assert outcome is None
    assert reason is None


def test_status_one_valid_one_disconnected_passes():
    # FAIL requires ALL assigned materials disconnected; one valid is enough.
    obj = FakeObject("Cube", [_connected_material(), _disconnected_material()])
    outcome, _ = materials.material_status(obj)
    assert outcome is None


def test_status_legacy_only_warns():
    obj = FakeObject("Cube", [_legacy_material()])
    outcome, reason = materials.material_status(obj)
    assert outcome == materials._WARN
    assert reason == "Material does not use nodes (legacy material)."


def test_status_valid_plus_empty_slot_warns_with_index():
    obj = FakeObject("Cube", [_connected_material(), None])
    outcome, reason = materials.material_status(obj)
    assert outcome == materials._WARN
    assert reason == "Empty material slot at index 1."


def test_status_valid_plus_multiple_empty_slots_lists_indices():
    obj = FakeObject("Cube", [_connected_material(), None, None])
    outcome, reason = materials.material_status(obj)
    assert outcome == materials._WARN
    assert reason == "Empty material slots at indices 1, 2."


def test_status_single_slot_no_empty_warning():
    # A single empty slot is the no-material FAIL path, not an empty-slot WARN.
    obj = FakeObject("Cube", [None])
    outcome, _ = materials.material_status(obj)
    assert outcome == materials._FAIL


def test_status_valid_plus_legacy_warns():
    obj = FakeObject("Cube", [_connected_material(), _legacy_material()])
    outcome, reason = materials.material_status(obj)
    assert outcome == materials._WARN
    assert "legacy" in reason.lower()


# --- run(): PASS paths ----------------------------------------------------


def test_empty_scene_passes():
    result = _run([])
    assert result.status == models.Status.PASS
    assert result.message == "All mesh objects have export-relevant materials."
    assert result.affected_objects == []
    assert result.issues == []


def test_all_connected_passes():
    objs = [
        FakeObject("Cube", [_connected_material()]),
        FakeObject("Plane", [_connected_material()]),
    ]
    result = _run(objs)
    assert result.status == models.Status.PASS
    assert result.severity == models.Severity.BLOCKER


def test_flat_color_node_material_passes():
    # A connected surface with no image texture is still export-relevant.
    out = FakeNode("OUTPUT_MATERIAL", surface_linked=True)
    emission = FakeNode("EMISSION")
    mat = FakeMaterial(use_nodes=True, node_tree=FakeNodeTree([emission, out]))
    result = _run([FakeObject("Lamp", [mat])])
    assert result.status == models.Status.PASS


# --- run(): FAIL paths ----------------------------------------------------


def test_no_slots_fails():
    result = _run([FakeObject("Cube", [])])
    assert result.status == models.Status.FAIL
    assert result.severity == models.Severity.BLOCKER
    assert result.affected_objects == ["Cube"]
    assert result.message == (
        "1 object(s) have missing or disconnected materials: Cube."
    )
    assert len(result.issues) == 1
    assert result.issues[0].object_name == "Cube"
    assert result.issues[0].reason == "Object has no material slots."


def test_disconnected_fails():
    result = _run([FakeObject("Cube", [_disconnected_material()])])
    assert result.status == models.Status.FAIL
    assert result.issues[0].reason == (
        "Assigned material has a disconnected surface output."
    )


def test_mixed_objects_fail_only_offenders():
    objs = [
        FakeObject("Good", [_connected_material()]),
        FakeObject("zebra", [_disconnected_material()]),
        FakeObject("alpha", []),
    ]
    result = _run(objs)
    assert result.status == models.Status.FAIL
    assert result.affected_objects == ["alpha", "zebra"]
    assert result.message == (
        "2 object(s) have missing or disconnected materials: alpha, zebra."
    )


def test_affected_objects_sorted():
    objs = [
        FakeObject("zebra", []),
        FakeObject("alpha", []),
        FakeObject("mango", []),
    ]
    result = _run(objs)
    assert result.affected_objects == ["alpha", "mango", "zebra"]


def test_affected_objects_cap_and_overflow():
    cap = constants.AFFECTED_OBJECTS_CAP
    objs = [FakeObject(f"obj_{i:03d}", []) for i in range(cap + 5)]
    result = _run(objs)
    assert result.status == models.Status.FAIL
    assert len(result.affected_objects) == cap
    assert "(... and 5 more)" in result.message
    assert result.message.startswith(f"{cap + 5} object(s) have missing")


# --- run(): WARNING paths -------------------------------------------------


def test_legacy_material_warns():
    result = _run([FakeObject("Cube", [_legacy_material()])])
    assert result.status == models.Status.WARNING
    assert result.severity == models.Severity.WARNING
    assert result.affected_objects == ["Cube"]
    assert result.message == (
        "1 object(s) have empty or legacy material slots: Cube."
    )


def test_empty_slot_warns():
    result = _run([FakeObject("crate_a", [_connected_material(), None])])
    assert result.status == models.Status.WARNING
    assert result.affected_objects == ["crate_a"]
    assert result.issues[0].reason == "Empty material slot at index 1."


def test_fail_takes_precedence_over_warning():
    bad = FakeObject("missing", [])
    warn = FakeObject("legacy_obj", [_legacy_material()])
    result = _run([bad, warn])
    assert result.status == models.Status.FAIL
    assert result.severity == models.Severity.BLOCKER
    assert result.affected_objects == ["missing"]


def test_warning_objects_sorted_and_counted():
    objs = [
        FakeObject("zebra", [_legacy_material()]),
        FakeObject("alpha", [_legacy_material()]),
    ]
    result = _run(objs)
    assert result.status == models.Status.WARNING
    assert result.affected_objects == ["alpha", "zebra"]
    assert result.message == (
        "2 object(s) have empty or legacy material slots: alpha, zebra."
    )


