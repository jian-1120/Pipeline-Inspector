"""Tests for the Material Assignment detail block in pipeline_inspector/report.py."""

from datetime import datetime

from pipeline_inspector import models, report
from pipeline_inspector.checks import materials


class FakeSocket:
    def __init__(self, name="Surface", is_linked=False):
        self.name = name
        self.is_linked = is_linked


class FakeInputs:
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
    def __init__(self, name, mats):
        self.name = name
        self.material_slots = [FakeSlot(m) for m in mats]


def _connected():
    out = FakeNode("OUTPUT_MATERIAL", surface_linked=True)
    bsdf = FakeNode("BSDF_PRINCIPLED")
    return FakeMaterial(use_nodes=True, node_tree=FakeNodeTree([bsdf, out]))


def _legacy():
    return FakeMaterial(use_nodes=False, node_tree=None)


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
    check_result = materials.run({"mesh_objects": objs})
    return report.render(_result_with(check_result, verdict))


def test_pass_shows_export_relevant_message():
    objs = [FakeObject("Cube", [_connected()])]
    lines = _render(objs, verdict=models.Verdict.READY)
    assert "Material Assignment: PASS" in lines
    assert "All inspected mesh objects have export-relevant materials." in lines


def test_fail_block_contents():
    objs = [FakeObject("Suzanne", [])]
    lines = _render(objs)
    assert "Material Assignment: FAIL" in lines
    assert (
        "1 object(s) have missing or disconnected materials: Suzanne." in lines
    )
    assert "Affected Objects:" in lines
    assert "- Suzanne" in lines
    assert "Fix:" in lines
    assert "Note:" in lines
    assert (
        "This check verifies material assignment and surface connectivity only."
        in lines
    )


def test_warning_block_shows_reason():
    objs = [FakeObject("crate_a", [_connected(), None])]
    lines = _render(objs, verdict=models.Verdict.READY_WITH_WARNINGS)
    assert "Material Assignment: WARN" in lines
    assert "  Empty material slot at index 1." in lines


def test_fail_block_appears_after_checks_summary():
    objs = [FakeObject("Suzanne", [])]
    lines = _render(objs)
    assert lines.index("Checks:") < lines.index("Material Assignment: FAIL")
