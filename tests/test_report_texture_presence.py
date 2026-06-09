"""Tests for the Texture Presence detail block in pipeline_inspector/report.py."""

from datetime import datetime

from pipeline_inspector import models, report
from pipeline_inspector.checks import textures


class FakeImage:
    def __init__(self, name, packed=False, source="FILE", has_data=True, exists=True):
        self.name = name
        self.packed_file = object() if packed else None
        self.source = source
        self.has_data = has_data
        self.exists = exists


class FakeNode:
    def __init__(self, image):
        self.type = "TEX_IMAGE"
        self.image = image


class FakeNodeTree:
    def __init__(self, nodes):
        self.nodes = nodes


class FakeMaterial:
    def __init__(self, nodes):
        self.use_nodes = True
        self.node_tree = FakeNodeTree(nodes)


class FakeSlot:
    def __init__(self, material):
        self.material = material


class FakeObject:
    def __init__(self, name, images):
        self.name = name
        self.material_slots = [FakeSlot(FakeMaterial([FakeNode(i) for i in images]))]


def _resolver(image):
    return image.exists


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


def _render(objs, is_saved=True, verdict=models.Verdict.NOT_READY):
    check_result = textures.run(
        {"mesh_objects": objs}, is_saved=is_saved, resolve_exists=_resolver
    )
    return report.render(_result_with(check_result, verdict))


def test_pass_shows_reachable_message():
    objs = [FakeObject("Cube", [FakeImage("ok.png", exists=True)])]
    lines = _render(objs, verdict=models.Verdict.READY)
    assert "Texture Presence: PASS" in lines
    assert "All referenced textures are packed or reachable." in lines


def test_fail_block_contents():
    objs = [FakeObject("Suzanne", [FakeImage("wood.png", exists=False)])]
    lines = _render(objs)
    assert "Texture Presence: FAIL" in lines
    assert "1 texture file(s) are missing or unreachable: wood.png." in lines
    assert "Affected Objects:" in lines
    assert "- Suzanne" in lines
    assert "Fix:" in lines
    assert "Note:" in lines
    assert "This check verifies texture reachability only." in lines


def test_warning_block_shows_unsaved_message():
    objs = [FakeObject("Cube", [FakeImage("wood.png", exists=False)])]
    lines = _render(objs, is_saved=False)
    assert "Texture Presence: WARN" in lines
    assert (
        "File is unsaved; texture paths cannot be verified. "
        "Save the file and re-run." in lines
    )


def test_fail_block_appears_after_checks_summary():
    objs = [FakeObject("Suzanne", [FakeImage("wood.png", exists=False)])]
    lines = _render(objs)
    assert lines.index("Checks:") < lines.index("Texture Presence: FAIL")
