"""The single Pipeline Inspector N-panel."""

import bpy

from .. import report, state


class PIPELINE_INSPECTOR_PT_panel(bpy.types.Panel):
    bl_label = "Pipeline Inspector"
    bl_idname = "PIPELINE_INSPECTOR_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Pipeline Inspector"

    def draw(self, context):
        layout = self.layout
        layout.operator("pipeline_inspector.run", text="Run Inspection")
        layout.separator()

        result = state.get_latest_result()
        if result is None:
            layout.label(text="No inspection run yet. Press Run Inspection.")
            return

        for line in report.render(result):
            if line == "":
                layout.separator()
            else:
                layout.label(text=line)
