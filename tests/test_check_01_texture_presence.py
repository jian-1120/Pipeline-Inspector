"""Tests for Check 01 — Texture Presence (pipeline_inspector/checks/textures.py).

Classifiers and run() are exercised with plain fakes and injected seams
(`is_saved`, `resolve_exists`) so the suite runs under the bpy stub without
touching bpy.data or bpy.path.
"""

from pipeline_inspector import constants, models
from pipeline_inspector.checks import textures


class FakeImage:
    def __init__(
        self,
        name,
        packed=False,
        source="FILE",
        has_data=True,
        exists=True,
    ):
        self.name = name
        self.packed_file = object() if packed else None
        self.source = source
        self.has_data = has_data
        self.exists = exists


class FakeNode:
    def __init__(self, image, node_type="TEX_IMAGE"):
        self.type = node_type
        self.image = image


class FakeNodeTree:
    def __init__(self, nodes):
        self.nodes = nodes


class FakeMaterial:
    def __init__(self, nodes, use_nodes=True):
        self.use_nodes = use_nodes
        self.node_tree = FakeNodeTree(nodes) if nodes is not None else None


class FakeSlot:
    def __init__(self, material):
        self.material = material


class FakeObject:
    def __init__(self, name, materials):
        self.name = name
        self.material_slots = [FakeSlot(m) for m in materials]


def _obj_with_images(name, images):
    nodes = [FakeNode(img) for img in images]
    return FakeObject(name, [FakeMaterial(nodes)])


def _resolver(image):
    return image.exists


def _run(objs, is_saved=True):
    return textures.run(
        {"mesh_objects": objs}, is_saved=is_saved, resolve_exists=_resolver
    )


# --- Pure classifier ------------------------------------------------------


def test_packed_image_passes():
    img = FakeImage("tex", packed=True, exists=False, has_data=False)
    assert textures.image_status(img, True, _resolver) is None


def test_generated_image_passes():
    img = FakeImage("noise", source="GENERATED", exists=False, has_data=False)
    assert textures.image_status(img, True, _resolver) is None


def test_file_image_present_with_data_passes():
    img = FakeImage("wood", source="FILE", exists=True, has_data=True)
    assert textures.image_status(img, True, _resolver) is None


def test_file_image_missing_fails():
    img = FakeImage("wood", source="FILE", exists=False, has_data=True)
    assert textures.image_status(img, True, _resolver) == textures._FAIL


def test_file_image_present_without_data_fails():
    img = FakeImage("wood", source="FILE", exists=True, has_data=False)
    assert textures.image_status(img, True, _resolver) == textures._FAIL


def test_file_image_unsaved_is_unverifiable():
    img = FakeImage("wood", source="FILE", exists=True, has_data=True)
    assert textures.image_status(img, False, _resolver) == textures._UNVERIFIABLE


def test_tiled_image_first_tile_resolves_passes():
    img = FakeImage("udim", source="TILED", exists=True, has_data=True)
    assert textures.image_status(img, True, _resolver) is None


def test_unknown_source_with_data_passes():
    img = FakeImage("odd", source="VIEWER", exists=False, has_data=True)
    assert textures.image_status(img, True, _resolver) is None


def test_unknown_source_without_data_fails():
    img = FakeImage("odd", source="VIEWER", exists=False, has_data=False)
    assert textures.image_status(img, True, _resolver) == textures._FAIL


# --- run(): PASS paths ----------------------------------------------------


def test_empty_scene_passes():
    result = _run([])
    assert result.status == models.Status.PASS
    assert result.message == "All referenced textures are packed or reachable."
    assert result.affected_objects == []
    assert result.issues == []


def test_procedural_only_material_not_flagged():
    obj = FakeObject("Cube", [FakeMaterial([])])
    result = _run([obj])
    assert result.status == models.Status.PASS


def test_material_without_use_nodes_not_flagged():
    obj = FakeObject("Cube", [FakeMaterial(None, use_nodes=False)])
    result = _run([obj])
    assert result.status == models.Status.PASS


def test_empty_slot_not_flagged():
    obj = FakeObject("Cube", [None])
    result = _run([obj])
    assert result.status == models.Status.PASS


def test_all_reachable_passes():
    obj = _obj_with_images("Cube", [FakeImage("a"), FakeImage("b", packed=True)])
    result = _run([obj])
    assert result.status == models.Status.PASS
    assert result.severity == models.Severity.BLOCKER


# --- run(): FAIL paths ----------------------------------------------------


def test_single_missing_texture_fails():
    obj = _obj_with_images("Cube", [FakeImage("wood.png", exists=False)])
    result = _run([obj])
    assert result.status == models.Status.FAIL
    assert result.severity == models.Severity.BLOCKER
    assert result.affected_objects == ["Cube"]
    assert result.message == (
        "1 texture file(s) are missing or unreachable: wood.png."
    )
    assert len(result.issues) == 1
    assert result.issues[0].object_name == "Cube"


def test_object_with_several_missing_images_appears_once():
    obj = _obj_with_images(
        "Cube",
        [FakeImage("a.png", exists=False), FakeImage("b.png", exists=False)],
    )
    result = _run([obj])
    assert result.affected_objects == ["Cube"]
    assert "a.png" in result.message and "b.png" in result.message
    assert result.message.startswith("2 texture file(s)")


def test_affected_objects_sorted_and_image_names_in_message():
    objs = [
        _obj_with_images("zebra", [FakeImage("z.png", exists=False)]),
        _obj_with_images("alpha", [FakeImage("a.png", exists=False)]),
    ]
    result = _run(objs)
    assert result.affected_objects == ["alpha", "zebra"]
    assert result.message == (
        "2 texture file(s) are missing or unreachable: a.png, z.png."
    )


def test_mixed_objects_fail_only_offenders():
    objs = [
        _obj_with_images("Good", [FakeImage("ok.png", exists=True)]),
        _obj_with_images("Bad", [FakeImage("gone.png", exists=False)]),
    ]
    result = _run(objs)
    assert result.status == models.Status.FAIL
    assert result.affected_objects == ["Bad"]


def test_image_name_overflow_in_message():
    cap = constants.AFFECTED_OBJECTS_CAP
    images = [FakeImage(f"img_{i:03d}.png", exists=False) for i in range(cap + 5)]
    obj = _obj_with_images("Cube", images)
    result = _run([obj])
    assert result.status == models.Status.FAIL
    assert "(... and 5 more)" in result.message
    assert result.message.startswith(f"{cap + 5} texture file(s)")


# --- run(): WARNING (unsaved) path ---------------------------------------


def test_unsaved_file_warns_and_skips_resolution():
    obj = _obj_with_images("Cube", [FakeImage("wood.png", exists=False)])
    result = _run([obj], is_saved=False)
    assert result.status == models.Status.WARNING
    assert result.severity == models.Severity.WARNING
    assert result.affected_objects == ["Cube"]
    assert result.message == (
        "File is unsaved; texture paths cannot be verified. "
        "Save the file and re-run."
    )


def test_unsaved_file_with_packed_images_passes():
    obj = _obj_with_images("Cube", [FakeImage("packed", packed=True)])
    result = _run([obj], is_saved=False)
    assert result.status == models.Status.PASS


def test_fail_takes_precedence_over_unsaved_warning_per_object():
    # An object whose file-image is missing under a saved file FAILs; an
    # unsaved file routes the same object to WARNING instead.
    obj = _obj_with_images("Cube", [FakeImage("wood.png", exists=False)])
    assert _run([obj], is_saved=True).status == models.Status.FAIL
    assert _run([obj], is_saved=False).status == models.Status.WARNING
