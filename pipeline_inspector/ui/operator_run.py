"""The Run Inspection operator."""

import bpy

from .. import inspector


class PIPELINE_INSPECTOR_OT_run(bpy.types.Operator):
    bl_idname = "pipeline_inspector.run"
    bl_label = "Run Inspection"
    bl_description = "Run pre-delivery inspection on the current scene"
    bl_options = {"REGISTER"}

    def execute(self, context):
        inspector.run_inspection(context)
        for area in context.screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()
        return {"FINISHED"}
