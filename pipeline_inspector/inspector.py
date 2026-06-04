"""Orchestrator. Runs all registered checks and produces an InspectionResult."""

from datetime import datetime

import bpy

from . import models, scoring, state
from .checks import CHECK_REGISTRY


def run_inspection(context=None):
    if context is None:
        context = bpy.context

    scene = context.scene
    mesh_objects = [
        obj for obj in scene.objects
        if obj.type == "MESH" and obj.visible_get() and obj.library is None
    ]
    inputs = {"context": context, "scene": scene, "mesh_objects": mesh_objects}

    results = [check_fn(inputs) for _, _, check_fn in CHECK_REGISTRY]

    score, verdict, blocker_count, warning_count = scoring.derive(results)

    inspection_result = models.InspectionResult(
        results=results,
        score=score,
        verdict=verdict,
        blocker_count=blocker_count,
        warning_count=warning_count,
        generated_at=datetime.now(),
        blender_version=bpy.app.version_string,
        total_objects_inspected=len(mesh_objects),
    )

    state.set_latest_result(inspection_result)
    return inspection_result
