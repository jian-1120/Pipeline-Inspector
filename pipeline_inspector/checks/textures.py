"""Check 01 — Texture Presence.

FAILs (BLOCKER) any image referenced by a TEX_IMAGE node in a material on a
visible non-linked mesh object that is neither packed, generated, nor reachable
on disk. WARNs when the .blend is unsaved so `//`-relative paths have no anchor
to resolve against. Read-only: never mutates the scene and never writes to disk.
"""

import concurrent.futures
import os

from .. import constants, models
from . import base

CHECK_ID = "01_texture_presence"
CHECK_NAME = "Texture Presence"
SEVERITY = models.Severity.BLOCKER

_FILE_SOURCES = {"FILE", "TILED", "SEQUENCE"}

_PASS_MESSAGE = "All referenced textures are packed or reachable."
_UNSAVED_MESSAGE = (
    "File is unsaved; texture paths cannot be verified. "
    "Save the file and re-run."
)
_REASON_MISSING = "Material references missing or unreachable texture(s)."
_REASON_UNVERIFIABLE = "Texture paths cannot be verified while the file is unsaved."

# Per-image classifier outcomes.
_PASS = None
_FAIL = "fail"
_UNVERIFIABLE = "unverifiable"


def image_status(image, is_saved, resolve_exists):
    """Pure per-image classifier. Returns _PASS / _FAIL / _UNVERIFIABLE.

    `is_saved` is the .blend save state; `resolve_exists(image)` returns whether
    the image's resolved absolute path exists on disk. Neither this function nor
    its callees mutate the image.
    """
    if getattr(image, "packed_file", None) is not None:
        return _PASS

    source = getattr(image, "source", None)
    if source == "GENERATED":
        return _PASS

    if source in _FILE_SOURCES:
        if not is_saved:
            return _UNVERIFIABLE
        if resolve_exists(image) and getattr(image, "has_data", False):
            return _PASS
        return _FAIL

    # Not packed, not generated, not a known file source. Reachable only if it
    # already carries pixel data; otherwise it is broken.
    return _PASS if getattr(image, "has_data", False) else _FAIL


def _iter_object_images(obj):
    """Yield each Image referenced by a TEX_IMAGE node in the object's materials.

    Procedural-only materials (no image nodes) contribute nothing and so are
    never flagged. Linked/empty slots are skipped.
    """
    for slot in getattr(obj, "material_slots", []) or []:
        material = getattr(slot, "material", None)
        if material is None or not getattr(material, "use_nodes", False):
            continue
        node_tree = getattr(material, "node_tree", None)
        if node_tree is None:
            continue
        for node in getattr(node_tree, "nodes", []) or []:
            if getattr(node, "type", None) != "TEX_IMAGE":
                continue
            image = getattr(node, "image", None)
            if image is not None:
                yield image


def _path_exists_with_timeout(abspath):
    """os.path.exists guarded by FILE_EXISTS_TIMEOUT_MS to survive slow drives.

    A stalled network path is treated as not-present rather than blocking the
    UI; the delivery gate flags unverifiable textures instead of hanging.
    """
    timeout_s = constants.FILE_EXISTS_TIMEOUT_MS / 1000.0
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(os.path.exists, abspath)
        try:
            return future.result(timeout=timeout_s)
        except concurrent.futures.TimeoutError:
            return False


def _first_udim_path(image, raw):
    """Substitute the first declared UDIM tile number into a `<UDIM>` token.

    v1 only requires the first tile to resolve; missing higher tiles are not
    validated here (spec treats them as INFO, not FAIL). Falls back to the raw
    path when the token or tile list is absent.
    """
    if "<UDIM>" not in raw:
        return raw
    tiles = getattr(image, "tiles", None)
    numbers = sorted(getattr(t, "number", 0) for t in tiles) if tiles else []
    if not numbers:
        return raw
    return raw.replace("<UDIM>", str(numbers[0]))


def _resolve_exists(image):
    """Resolve an image's `//`-relative path and test on-disk existence."""
    import bpy

    raw = getattr(image, "filepath_raw", "") or getattr(image, "filepath", "")
    if not raw:
        return False
    if getattr(image, "source", None) == "TILED":
        raw = _first_udim_path(image, raw)
    return _path_exists_with_timeout(bpy.path.abspath(raw))


def _blend_is_saved():
    import bpy

    return bool(getattr(bpy.data, "is_saved", False))


def run(inputs, *, is_saved=None, resolve_exists=None):
    if is_saved is None:
        is_saved = _blend_is_saved()
    if resolve_exists is None:
        resolve_exists = _resolve_exists

    fail_objects = []
    fail_image_names = []
    fail_issues = []

    warn_objects = []
    warn_issues = []

    for obj in inputs["mesh_objects"]:
        obj_failing = []
        obj_unverifiable = []
        seen = set()
        for image in _iter_object_images(obj):
            name = getattr(image, "name", "")
            if name in seen:
                continue
            seen.add(name)
            status = image_status(image, is_saved, resolve_exists)
            if status == _FAIL:
                obj_failing.append(name)
            elif status == _UNVERIFIABLE:
                obj_unverifiable.append(name)

        if obj_failing:
            fail_objects.append(obj.name)
            fail_image_names.extend(obj_failing)
            detail = f"{_REASON_MISSING} {', '.join(sorted(set(obj_failing)))}."
            fail_issues.append(
                models.IssueRecord(
                    check_id=CHECK_ID,
                    severity=SEVERITY,
                    object_name=obj.name,
                    reason=_REASON_MISSING,
                    detail=detail,
                )
            )
        elif obj_unverifiable:
            warn_objects.append(obj.name)
            warn_issues.append(
                models.IssueRecord(
                    check_id=CHECK_ID,
                    severity=models.Severity.WARNING,
                    object_name=obj.name,
                    reason=_REASON_UNVERIFIABLE,
                    detail=_REASON_UNVERIFIABLE,
                )
            )

    if fail_objects:
        capped, overflow = base.dedupe_sort_cap(fail_image_names)
        names = ", ".join(capped)
        if overflow:
            names = f"{names} (... and {overflow} more)"
        message = (
            f"{len(set(fail_image_names))} texture file(s) are missing or "
            f"unreachable: {names}."
        )
        return base.make_fail(
            CHECK_ID, CHECK_NAME, SEVERITY, message, fail_objects, fail_issues
        )

    if warn_objects:
        return base.make_warning(
            CHECK_ID, CHECK_NAME, _UNSAVED_MESSAGE, warn_objects, warn_issues
        )

    return base.make_pass(CHECK_ID, CHECK_NAME, SEVERITY, _PASS_MESSAGE)
