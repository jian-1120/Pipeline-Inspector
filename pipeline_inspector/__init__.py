"""Pipeline Inspector — pre-delivery inspection add-on for Blender 4.2 LTS.

Scaffold phase: registration shell + placeholder check pipeline.
Real check logic lands in later phases. See SCAFFOLD_PLAN_V1.md.
"""

bl_info = {
    "name": "Pipeline Inspector",
    "author": "Pipeline Inspector Team",
    "version": (0, 1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Pipeline Inspector",
    "description": "Pre-delivery inspection that produces a READY FOR DELIVERY score.",
    "category": "3D View",
}

import bpy

from . import state
from .ui import PIPELINE_INSPECTOR_OT_run, PIPELINE_INSPECTOR_PT_panel

_CLASSES = (
    PIPELINE_INSPECTOR_OT_run,
    PIPELINE_INSPECTOR_PT_panel,
)


def register():
    for cls in _CLASSES:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            bpy.utils.unregister_class(cls)
            bpy.utils.register_class(cls)
    state.clear()


def unregister():
    state.clear()
    for cls in reversed(_CLASSES):
        try:
            bpy.utils.unregister_class(cls)
        except (RuntimeError, ValueError):
            pass
