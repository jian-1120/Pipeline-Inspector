"""Check 02 — Material Assignment.

FAILs (BLOCKER) any visible non-linked mesh object that has no material slot,
has slots but no assigned material, or whose every assigned material is a
node material with a disconnected Material Output surface. WARNs when an object
has a working material but also carries empty slots (multi-slot meshes) or a
legacy non-node material. Read-only: never mutates the scene and never writes
to disk.
"""

from .. import models
from . import base

CHECK_ID = "02_material_assignment"
CHECK_NAME = "Material Assignment"
SEVERITY = models.Severity.BLOCKER

# Per-object outcomes returned by material_status().
_FAIL = "fail"
_WARN = "warn"

# Per-material classifications returned by classify_material().
_MAT_VALID = "valid"
_MAT_LEGACY = "legacy"
_MAT_DISCONNECTED = "disconnected"

_PASS_MESSAGE = "All mesh objects have export-relevant materials."

_REASON_NO_SLOTS = "Object has no material slots."
_REASON_NO_MATERIAL = "Object has material slots but none are assigned."
_REASON_DISCONNECTED = "Assigned material has a disconnected surface output."
_REASON_LEGACY = "Material does not use nodes (legacy material)."


def _surface_socket(output_node):
    """Return the 'Surface' input socket of a Material Output node, or None.

    Works against both Blender's bpy_prop_collection (string subscript) and
    plain dict/list fakes used in tests. Read-only.
    """
    inputs = getattr(output_node, "inputs", None)
    if inputs is None:
        return None
    try:
        return inputs["Surface"]
    except (KeyError, TypeError, IndexError):
        pass
    try:
        for sock in inputs:
            if getattr(sock, "name", None) == "Surface":
                return sock
    except TypeError:
        return None
    return None


def _surface_is_linked(node_tree):
    """True when any OUTPUT_MATERIAL node has an incoming link on Surface.

    Returns None when the tree carries no OUTPUT_MATERIAL node at all (the
    surface cannot be connected). Any single connected output is enough to
    treat the material as export-relevant, so a stray disconnected extra
    output node never produces a false FAIL.
    """
    outputs = [
        n for n in getattr(node_tree, "nodes", []) or []
        if getattr(n, "type", None) == "OUTPUT_MATERIAL"
    ]
    if not outputs:
        return None
    for out in outputs:
        socket = _surface_socket(out)
        if socket is not None and getattr(socket, "is_linked", False):
            return True
    return False


def classify_material(material):
    """Pure per-material classifier.

    Returns one of _MAT_VALID, _MAT_LEGACY, _MAT_DISCONNECTED. A flat-color or
    procedural node material counts as VALID as long as its surface output is
    connected; texture presence is Check 01's concern, not this check's.
    """
    if not getattr(material, "use_nodes", False):
        return _MAT_LEGACY

    node_tree = getattr(material, "node_tree", None)
    if node_tree is None:
        return _MAT_DISCONNECTED

    linked = _surface_is_linked(node_tree)
    if linked:
        return _MAT_VALID
    return _MAT_DISCONNECTED


def _empty_slot_reason(empty_indices):
    if len(empty_indices) == 1:
        return f"Empty material slot at index {empty_indices[0]}."
    joined = ", ".join(str(i) for i in empty_indices)
    return f"Empty material slots at indices {joined}."


def material_status(obj):
    """Pure classifier. Returns (outcome, reason).

    outcome is _FAIL, _WARN, or None (PASS). Reads only obj.material_slots and
    each material's node graph; never mutates the object.
    """
    slots = list(getattr(obj, "material_slots", []) or [])
    if len(slots) == 0:
        return _FAIL, _REASON_NO_SLOTS

    assigned = [
        getattr(s, "material", None) for s in slots
        if getattr(s, "material", None) is not None
    ]
    if not assigned:
        return _FAIL, _REASON_NO_MATERIAL

    classes = [classify_material(m) for m in assigned]
    has_valid = _MAT_VALID in classes
    has_legacy = _MAT_LEGACY in classes
    empty_indices = [
        i for i, s in enumerate(slots) if getattr(s, "material", None) is None
    ]

    if has_valid:
        # The object has at least one export-relevant material; only the
        # non-blocking empty-slot / legacy concerns remain.
        warn_parts = []
        if len(slots) > 1 and empty_indices:
            warn_parts.append(_empty_slot_reason(empty_indices))
        if has_legacy:
            warn_parts.append(_REASON_LEGACY)
        if warn_parts:
            return _WARN, " ".join(warn_parts)
        return None, None

    # No valid material. A legacy material still exports a base colour, so per
    # spec it is a WARNING that "proceeds" rather than a blocker. Only when
    # every assigned material is a disconnected node material does the object
    # FAIL.
    if has_legacy:
        return _WARN, _REASON_LEGACY
    return _FAIL, _REASON_DISCONNECTED


def run(inputs):
    fail_objects = []
    fail_issues = []
    warn_objects = []
    warn_issues = []

    for obj in inputs["mesh_objects"]:
        outcome, reason = material_status(obj)
        if outcome == _FAIL:
            fail_objects.append(obj.name)
            fail_issues.append(
                models.IssueRecord(
                    check_id=CHECK_ID,
                    severity=SEVERITY,
                    object_name=obj.name,
                    reason=reason,
                    detail=reason,
                )
            )
        elif outcome == _WARN:
            warn_objects.append(obj.name)
            warn_issues.append(
                models.IssueRecord(
                    check_id=CHECK_ID,
                    severity=models.Severity.WARNING,
                    object_name=obj.name,
                    reason=reason,
                    detail=reason,
                )
            )

    if fail_objects:
        capped, overflow = base.dedupe_sort_cap(fail_objects)
        names = ", ".join(capped)
        if overflow:
            names = f"{names} (... and {overflow} more)"
        message = (
            f"{len(set(fail_objects))} object(s) have missing or "
            f"disconnected materials: {names}."
        )
        return base.make_fail(
            CHECK_ID, CHECK_NAME, SEVERITY, message, fail_objects, fail_issues
        )

    if warn_objects:
        capped, overflow = base.dedupe_sort_cap(warn_objects)
        names = ", ".join(capped)
        if overflow:
            names = f"{names} (... and {overflow} more)"
        message = (
            f"{len(set(warn_objects))} object(s) have empty or legacy "
            f"material slots: {names}."
        )
        return base.make_warning(
            CHECK_ID, CHECK_NAME, message, warn_objects, warn_issues
        )

    return base.make_pass(CHECK_ID, CHECK_NAME, SEVERITY, _PASS_MESSAGE)
