"""Check 05 — Normal Consistency.

FAILs (BLOCKER) any visible non-linked mesh object that has at least one
connected manifold component whose face winding is internally contradictory
(two faces sharing a manifold edge traverse that edge in the same direction).

v1 does NOT judge inward vs outward orientation; it only flags winding that is
self-contradictory inside an otherwise-manifold component. Components that
contain a non-manifold edge cannot be evaluated cleanly and are excluded
(surfaced as INFO, never a FAIL). Meshes with custom normals or above the
polycount cap are skipped with a WARNING (INFO severity).

Read-only: reads obj.data.polygons (ordered vertex loops) plus
mesh.has_custom_normals. Never builds, mutates, or frees scene data, never
calls bpy.ops, never writes to disk. The winding algorithm reads polygon
vertex loops directly rather than allocating a temporary BMesh, which keeps
the check dependency-free and unit-testable outside Blender.
"""

from .. import constants, models
from . import base

CHECK_ID = "05_normal_consistency"
CHECK_NAME = "Normal Consistency"
SEVERITY = models.Severity.BLOCKER

# Per-object outcomes returned by classify_object().
_FAIL = "fail"
_SKIP = "skip"
_INFO = "info"

_PASS_MESSAGE = "Face winding is consistent across all inspected meshes."
_REASON_INCONSISTENT = "Inconsistent face winding within a manifold component."
_REASON_CUSTOM_NORMALS = "Custom normals present; consistency check skipped."
_REASON_OVERSIZE = (
    "Mesh too large to inspect (>500k polygons); run on simplified geometry."
)
_REASON_NONMANIFOLD = "Non-manifold component skipped; winding not evaluated."


def classify_winding(faces):
    """Pure winding classifier over ordered face loops.

    faces is a sequence of vertex-index sequences (each a polygon's ordered
    loop). Returns (has_inconsistent, has_excluded):

    - has_inconsistent: at least one connected manifold component has a
      manifold edge whose two faces traverse it in the SAME direction.
    - has_excluded: at least one connected component contains a non-manifold
      edge (>2 incident faces) and was excluded from evaluation.

    Edge manifold-ness: 1 incident face = boundary (open mesh, allowed),
    2 = manifold (evaluated), >2 = non-manifold (component excluded).
    """
    # undirected edge key -> list of (face_index, directed (a, b)) incidences.
    edges = {}
    parent = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for fi, verts in enumerate(faces):
        parent.setdefault(fi, fi)
        n = len(verts)
        if n < 3:
            continue
        for i in range(n):
            a = verts[i]
            b = verts[(i + 1) % n]
            key = (a, b) if a < b else (b, a)
            edges.setdefault(key, []).append((fi, (a, b)))

    # Faces sharing any edge belong to the same connected component.
    for incidences in edges.values():
        first = incidences[0][0]
        for fi, _ in incidences[1:]:
            union(first, fi)

    # A component is excluded the moment any of its edges is non-manifold.
    excluded_roots = set()
    for incidences in edges.values():
        if len(incidences) > 2:
            excluded_roots.add(find(incidences[0][0]))

    has_inconsistent = False
    for incidences in edges.values():
        if len(incidences) != 2:
            continue
        if find(incidences[0][0]) in excluded_roots:
            continue
        if incidences[0][1] == incidences[1][1]:
            # Both faces traverse the shared edge the same way → contradiction.
            has_inconsistent = True
            break

    return has_inconsistent, bool(excluded_roots)


def classify_object(polygons, poly_count, has_custom_normals):
    """Pure per-object classifier. Returns (outcome, reason).

    outcome is _FAIL, _SKIP, _INFO, or None (PASS). Skip conditions are checked
    before any geometry is read so oversize and custom-normal meshes never pay
    the traversal cost.
    """
    if has_custom_normals:
        return _SKIP, _REASON_CUSTOM_NORMALS
    if poly_count > constants.POLYCOUNT_CAP:
        return _SKIP, _REASON_OVERSIZE

    faces = [tuple(getattr(p, "vertices", p)) for p in polygons]
    has_inconsistent, has_excluded = classify_winding(faces)
    if has_inconsistent:
        return _FAIL, _REASON_INCONSISTENT
    if has_excluded:
        return _INFO, _REASON_NONMANIFOLD
    return None, None


def _format_names(object_names):
    capped, overflow = base.dedupe_sort_cap(object_names)
    names = ", ".join(capped)
    if overflow:
        names = f"{names} (... and {overflow} more)"
    return capped, names


def _issue(severity, name, reason):
    return models.IssueRecord(
        check_id=CHECK_ID,
        severity=severity,
        object_name=name,
        reason=reason,
        detail=reason,
    )


def run(inputs):
    fail_objects, fail_issues = [], []
    skip_objects, skip_issues = [], []
    info_objects, info_issues = [], []

    for obj in inputs["mesh_objects"]:
        mesh = obj.data
        has_custom = bool(getattr(mesh, "has_custom_normals", False))
        polygons = getattr(mesh, "polygons", None) or []
        poly_count = len(polygons)

        outcome, reason = classify_object(polygons, poly_count, has_custom)
        if outcome == _FAIL:
            fail_objects.append(obj.name)
            fail_issues.append(_issue(SEVERITY, obj.name, reason))
        elif outcome == _SKIP:
            skip_objects.append(obj.name)
            skip_issues.append(_issue(models.Severity.INFO, obj.name, reason))
        elif outcome == _INFO:
            info_objects.append(obj.name)
            info_issues.append(_issue(models.Severity.INFO, obj.name, reason))

    # Precedence: a real FAIL outranks a skip WARNING, which outranks a purely
    # informational non-manifold note, which outranks a clean PASS.
    if fail_objects:
        _, names = _format_names(fail_objects)
        message = (
            f"{len(set(fail_objects))} object(s) have inconsistent face "
            f"winding: {names}."
        )
        return base.make_fail(
            CHECK_ID, CHECK_NAME, SEVERITY, message, fail_objects, fail_issues
        )

    if skip_objects:
        capped, names = _format_names(skip_objects)
        message = (
            f"{len(set(skip_objects))} object(s) skipped; winding not "
            f"checked: {names}."
        )
        return models.CheckResult(
            id=CHECK_ID,
            name=CHECK_NAME,
            status=models.Status.WARNING,
            severity=models.Severity.INFO,
            message=message,
            affected_objects=capped,
            issues=skip_issues,
        )

    if info_objects:
        capped, names = _format_names(info_objects)
        message = (
            f"Face winding is consistent; {len(set(info_objects))} object(s) "
            f"contain non-manifold geometry that was not evaluated: {names}."
        )
        return models.CheckResult(
            id=CHECK_ID,
            name=CHECK_NAME,
            status=models.Status.PASS,
            severity=SEVERITY,
            message=message,
            affected_objects=capped,
            issues=info_issues,
        )

    return base.make_pass(CHECK_ID, CHECK_NAME, SEVERITY, _PASS_MESSAGE)
