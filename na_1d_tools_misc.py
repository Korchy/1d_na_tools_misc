# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/1d_na_tools_misc

import bpy
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class

bl_info = {
    "name": "NA 1D Tools Misc",
    "description": "Some additional separate functions for NA 1D Tools",
    "author": "Nikita Akimov, Paul Kotelevets",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tool panel > 1D > NA 1D Tools Misc",
    "doc_url": "https://github.com/Korchy/1d_na_tools_misc",
    "tracker_url": "https://github.com/Korchy/1d_na_tools_misc",
    "category": "All"
}


# MAIN CLASS

class NA1DToolsMisc:

    @classmethod
    def untriangle_modifier(cls, context):
        # remove the "Triangle" modifier from all selected objects
        for obj in context.selected_objects:
            triangulate_modifiers = [_modifier for _modifier in obj.modifiers if _modifier.type == 'TRIANGULATE']
            for modifier in triangulate_modifiers:
                obj.modifiers.remove(modifier)

    @classmethod
    def multiclear_normal_data(cls, context):
        # remove the "custom split normal" from all selected objects
        active_object = context.active_object
        for obj in context.selected_objects:
            context.scene.objects.active = obj
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
        context.scene.objects.active = active_object

    @staticmethod
    def ui(layout, context):
        # ui panel
        layout.operator(
            operator='na_1d_tools_misc.untriangle_modifier',
            icon='MOD_TRIANGULATE'
        )
        layout.operator(
            operator='na_1d_tools_misc.multiclear_normal_data',
            icon='MOD_NORMALEDIT'
        )

# OPERATORS

class NA_1D_Tools_Misc_Untriangle_Modifier(Operator):
    bl_idname = 'na_1d_tools_misc.untriangle_modifier'
    bl_label = 'Untriangle Modifier'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        NA1DToolsMisc.untriangle_modifier(
            context=context
        )
        return {'FINISHED'}

class NA_1D_Tools_Misc_Multiclear_Normal_Data(Operator):
    bl_idname = 'na_1d_tools_misc.multiclear_normal_data'
    bl_label = 'Multiclear Normal Data'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        NA1DToolsMisc.multiclear_normal_data(
            context=context
        )
        return {'FINISHED'}


# PANELS

class NA_1D_Tools_Misc_PT_panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'NA 1D Tools Misc'
    bl_category = '1D'

    def draw(self, context):
        NA1DToolsMisc.ui(
            layout=self.layout,
            context=context
        )


# REGISTER

def register(ui=True):
    register_class(NA_1D_Tools_Misc_Untriangle_Modifier)
    register_class(NA_1D_Tools_Misc_Multiclear_Normal_Data)
    if ui:
        register_class(NA_1D_Tools_Misc_PT_panel)


def unregister(ui=True):
    if ui:
        unregister_class(NA_1D_Tools_Misc_PT_panel)
    unregister_class(NA_1D_Tools_Misc_Multiclear_Normal_Data)
    unregister_class(NA_1D_Tools_Misc_Untriangle_Modifier)


if __name__ == '__main__':
    register()
