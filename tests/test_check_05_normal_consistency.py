"""Tests for Check 05 — Normal Consistency (pipeline_inspector/checks/normals.py).

The winding algorithm reads ordered polygon vertex loops, so the fakes model
just that slice of the Blender mesh API: mesh.polygons (each with .vertices),
mesh.has_custom_normals, and obj.data / obj.name. No bpy, no BMesh.

Winding convention: two faces sharing a MANIFOLD edge (exactly two incident
faces) are consistent when they traverse that edge in OPPOSITE directions.
Same-direction traversal on a manifold edge is the contradiction this check
flags. Boundary edges (one incident face) are open-mesh edges and never fail.
"""

from pipeline_inspector import constants, models
from pipeline_inspector.checks import normals


# --- fakes ----------------------------------------------------------------


class FakePolygon:
    def __init__(self, vertices):
        self.vertices = tuple(vertices)


class FakeMesh:
    def __init__(self, faces, has_custom_normals=False):
        self.polygons = [FakePolygon(f) for f in faces]
        self.has_custom_normals = has_custom_normals


class BigPolygons:
    """Sized-but-not-iterated polygon collection for the oversize skip path."""

    def __init__(self, count):
        self._count = count

    def __len__(self):
        return self._count

    def __bool__(self):
        return self._count > 0

    def __iter__(self):  # pragma: no cover - skip path returns before iterating
        raise AssertionError("oversize mesh must not be traversed")


class OversizeMesh:
    def __init__(self, count):
        self.polygons = BigPolygons(count)
        self.has_custom_normals = False


class FakeObject:
    def __init__(self, name, mesh):
        self.name = name
        self.data = mesh


# --- geometry builders ----------------------------------------------------


# Two triangles meeting at a shared, consistently-wound edge.
_CONSISTENT_QUAD = [(0, 1, 2), (2, 1, 3)]
# Same two triangles, but the second traverses the shared edge the same way.
_INCONSISTENT_QUAD = [(0, 1, 2), (1, 2, 3)]
# Three triangles fanning off a single edge {1,2} -> non-manifold edge.
_NONMANIFOLD = [(0, 1, 2), (2, 1, 3), (1, 2, 4)]
# A single open face: every edge is a boundary edge.
_OPEN_PATCH = [(0, 1, 2)]


def _consistent(name):
    return FakeObject(name, FakeMesh(_CONSISTENT_QUAD))


def _inconsistent(name):
    return FakeObject(name, FakeMesh(_INCONSISTENT_QUAD))


def _nonmanifold(name):
    return FakeObject(name, FakeMesh(_NONMANIFOLD))


def _custom_normals(name):
    return FakeObject(name, FakeMesh(_CONSISTENT_QUAD, has_custom_normals=True))


def _oversize(name):
    return FakeObject(name, OversizeMesh(constants.POLYCOUNT_CAP + 1))


def _run(objs):
    return normals.run({"mesh_objects": objs})


# --- classify_winding (pure) ----------------------------------------------


def test_winding_consistent_quad():
    assert normals.classify_winding(_CONSISTENT_QUAD) == (False, False)


def test_winding_inconsistent_quad():
    has_inconsistent, has_excluded = normals.classify_winding(_INCONSISTENT_QUAD)
    assert has_inconsistent is True
    assert has_excluded is False


def test_winding_nonmanifold_excluded_not_failed():
    has_inconsistent, has_excluded = normals.classify_winding(_NONMANIFOLD)
    assert has_inconsistent is False
    assert has_excluded is True


def test_winding_open_patch_passes():
    assert normals.classify_winding(_OPEN_PATCH) == (False, False)


def test_winding_empty_mesh_passes():
    assert normals.classify_winding([]) == (False, False)


def test_winding_closed_envelope_consistent():
    # Two triangles sharing all three edges with opposite winding (a closed,
    # fully-manifold surface). Every shared edge is traversed oppositely.
    faces = [(0, 1, 2), (0, 2, 1)]
    assert normals.classify_winding(faces) == (False, False)


def test_winding_inconsistent_in_one_of_many_components():
    # Component A (verts 0-3) is consistent; component B (verts 10-13) is not.
    faces = _CONSISTENT_QUAD + [(10, 11, 12), (11, 12, 13)]
    has_inconsistent, has_excluded = normals.classify_winding(faces)
    assert has_inconsistent is True
    assert has_excluded is False


# --- classify_object (pure) -----------------------------------------------


def test_object_consistent_is_pass():
    assert normals.classify_object(
        [FakePolygon(f) for f in _CONSISTENT_QUAD], 2, False
    ) == (None, None)


def test_object_inconsistent_is_fail():
    outcome, reason = normals.classify_object(
        [FakePolygon(f) for f in _INCONSISTENT_QUAD], 2, False
    )
    assert outcome == normals._FAIL
    assert reason == "Inconsistent face winding within a manifold component."


def test_object_nonmanifold_is_info():
    outcome, reason = normals.classify_object(
        [FakePolygon(f) for f in _NONMANIFOLD], 3, False
    )
    assert outcome == normals._INFO
    assert reason == "Non-manifold component skipped; winding not evaluated."


def test_object_custom_normals_is_skip():
    outcome, reason = normals.classify_object([], 0, True)
    assert outcome == normals._SKIP
    assert reason == "Custom normals present; consistency check skipped."


def test_object_oversize_is_skip_before_reading_geometry():
    # poly_count over the cap must short-circuit; passing no polygons proves
    # the geometry is never read on the skip path.
    outcome, reason = normals.classify_object(
        None, constants.POLYCOUNT_CAP + 1, False
    )
    assert outcome == normals._SKIP
    assert "500k" in reason


def test_object_custom_normals_wins_over_oversize():
    outcome, reason = normals.classify_object(
        None, constants.POLYCOUNT_CAP + 1, True
    )
    assert outcome == normals._SKIP
    assert reason == "Custom normals present; consistency check skipped."


# --- run(): PASS ----------------------------------------------------------


def test_empty_scene_passes():
    result = _run([])
    assert result.status == models.Status.PASS
    assert result.severity == models.Severity.BLOCKER
    assert result.message == "Face winding is consistent across all inspected meshes."
    assert result.affected_objects == []
    assert result.issues == []


def test_all_consistent_passes():
    result = _run([_consistent("Cube"), _consistent("Plane")])
    assert result.status == models.Status.PASS
    assert result.severity == models.Severity.BLOCKER


def test_open_patch_passes():
    result = _run([FakeObject("card", FakeMesh(_OPEN_PATCH))])
    assert result.status == models.Status.PASS


# --- run(): FAIL ----------------------------------------------------------


def test_single_inconsistent_fails():
    result = _run([_inconsistent("Cube")])
    assert result.status == models.Status.FAIL
    assert result.severity == models.Severity.BLOCKER
    assert result.affected_objects == ["Cube"]
    assert result.message == "1 object(s) have inconsistent face winding: Cube."
    assert len(result.issues) == 1
    assert result.issues[0].object_name == "Cube"
    assert result.issues[0].severity == models.Severity.BLOCKER
    assert result.issues[0].reason == (
        "Inconsistent face winding within a manifold component."
    )


def test_mixed_objects_fail_only_offenders():
    objs = [_consistent("Good"), _inconsistent("zebra"), _inconsistent("alpha")]
    result = _run(objs)
    assert result.status == models.Status.FAIL
    assert result.affected_objects == ["alpha", "zebra"]
    assert result.message == (
        "2 object(s) have inconsistent face winding: alpha, zebra."
    )


def test_affected_objects_sorted():
    objs = [_inconsistent("zebra"), _inconsistent("alpha"), _inconsistent("mango")]
    result = _run(objs)
    assert result.affected_objects == ["alpha", "mango", "zebra"]


def test_affected_objects_cap_and_overflow():
    cap = constants.AFFECTED_OBJECTS_CAP
    objs = [_inconsistent(f"obj_{i:03d}") for i in range(cap + 5)]
    result = _run(objs)
    assert result.status == models.Status.FAIL
    assert len(result.affected_objects) == cap
    assert "(... and 5 more)" in result.message
    assert result.message.startswith(f"{cap + 5} object(s) have inconsistent")


# --- run(): WARNING (skip path) -------------------------------------------


def test_custom_normals_warns_with_info_severity():
    result = _run([_custom_normals("Hero")])
    assert result.status == models.Status.WARNING
    assert result.severity == models.Severity.INFO
    assert result.affected_objects == ["Hero"]
    assert result.message == "1 object(s) skipped; winding not checked: Hero."
    assert result.issues[0].reason == (
        "Custom normals present; consistency check skipped."
    )


def test_oversize_warns_with_info_severity():
    result = _run([_oversize("Terrain")])
    assert result.status == models.Status.WARNING
    assert result.severity == models.Severity.INFO
    assert result.affected_objects == ["Terrain"]
    assert result.issues[0].reason.startswith("Mesh too large")


def test_skip_objects_sorted_and_counted():
    objs = [_custom_normals("zebra"), _oversize("alpha")]
    result = _run(objs)
    assert result.status == models.Status.WARNING
    assert result.affected_objects == ["alpha", "zebra"]
    assert result.message == "2 object(s) skipped; winding not checked: alpha, zebra."


# --- run(): INFO (non-manifold note, PASS status) -------------------------


def test_nonmanifold_only_passes_with_note():
    result = _run([_nonmanifold("Sculpt")])
    assert result.status == models.Status.PASS
    assert result.severity == models.Severity.BLOCKER
    assert result.affected_objects == ["Sculpt"]
    assert "non-manifold" in result.message
    assert result.issues[0].severity == models.Severity.INFO
    assert result.issues[0].reason == (
        "Non-manifold component skipped; winding not evaluated."
    )


def test_nonmanifold_does_not_deduct_score_or_block():
    from pipeline_inspector import scoring

    result = _run([_nonmanifold("Sculpt")])
    score, verdict, blocker_count, warning_count = scoring.derive([result])
    assert score == 100
    assert blocker_count == 0
    assert warning_count == 0
    assert verdict == models.Verdict.READY


# --- run(): precedence ----------------------------------------------------


def test_fail_takes_precedence_over_skip():
    result = _run([_inconsistent("bad"), _custom_normals("skipped")])
    assert result.status == models.Status.FAIL
    assert result.severity == models.Severity.BLOCKER
    assert result.affected_objects == ["bad"]


def test_fail_takes_precedence_over_nonmanifold_info():
    result = _run([_inconsistent("bad"), _nonmanifold("sculpt")])
    assert result.status == models.Status.FAIL
    assert result.affected_objects == ["bad"]


def test_skip_takes_precedence_over_nonmanifold_info():
    result = _run([_custom_normals("hero"), _nonmanifold("sculpt")])
    assert result.status == models.Status.WARNING
    assert result.severity == models.Severity.INFO
    assert result.affected_objects == ["hero"]


def test_custom_normals_skip_caps_verdict_but_not_score():
    from pipeline_inspector import scoring

    result = _run([_custom_normals("Hero")])
    score, verdict, blocker_count, warning_count = scoring.derive([result])
    assert score == 100
    assert blocker_count == 0
    assert warning_count == 1
    assert verdict == models.Verdict.READY_WITH_WARNINGS
