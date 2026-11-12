# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/1d_na_tools_misc

import bmesh
import bpy
from bpy.props import FloatProperty
from bpy.types import Operator, Panel, WindowManager
from bpy.utils import register_class, unregister_class
from math import radians

bl_info = {
    "name": "NA 1D Tools Misc",
    "description": "Some additional separate functions for NA 1D Tools",
    "author": "Nikita Akimov, Paul Kotelevets",
    "version": (1, 1, 0),
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

    @classmethod
    def filter_face_angles(cls, context, angle_deg=70.0):
        # select all edges which face angle is grater than required
        # switch to edge select mode
        context.tool_settings.mesh_select_mode = (False, True, False)
        # current mode
        mode = context.active_object.mode
        if context.active_object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        # switch to vertex selection mode
        bm = bmesh.new()
        bm.from_mesh(context.active_object.data)
        # deselect
        cls._deselect_all_bm(bm=bm)
        # check face angles for all edges
        for edge in bm.edges:
            face_angle_rad = edge.calc_face_angle(None) # None returns for non-manifold edges
            if face_angle_rad and face_angle_rad > radians(angle_deg):
                edge.select = True
        # save changed data to mesh
        bm.to_mesh(context.active_object.data)
        bm.free()
        # return mode back
        bpy.ops.object.mode_set(mode=mode)

    @staticmethod
    def _deselect_all_bm(bm):
        # remove all selection in bmesh
        for face in bm.faces:
            face.select = False
        for edge in bm.edges:
            edge.select = False
        for vertex in bm.verts:
            vertex.select = False

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
        box = layout.box()
        box.operator(
            operator='na_1d_tools_misc.filter_face_angles',
            icon='PREVIEW_RANGE'
        )
        box.prop(
            data=context.window_manager,
            property='na_1d_tools_misc_prop_face_angle'
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

class NA_1D_Tools_Misc_Filter_Face_Angles(Operator):
    bl_idname = 'na_1d_tools_misc.filter_face_angles'
    bl_label = 'Filter Face Angles'
    bl_options = {'REGISTER', 'UNDO'}

    face_angle = FloatProperty(
        name='Face Angle',
        default=70.0,
        min=0.0
    )

    def execute(self, context):
        NA1DToolsMisc.filter_face_angles(
            context=context,
            angle_deg=self.face_angle
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
    WindowManager.na_1d_tools_misc_prop_face_angle = FloatProperty(
        name='Face Angle',
        default=70.0,
        min=0.0
    )
    register_class(NA_1D_Tools_Misc_Untriangle_Modifier)
    register_class(NA_1D_Tools_Misc_Multiclear_Normal_Data)
    register_class(NA_1D_Tools_Misc_Filter_Face_Angles)
    if ui:
        register_class(NA_1D_Tools_Misc_PT_panel)


def unregister(ui=True):
    if ui:
        unregister_class(NA_1D_Tools_Misc_PT_panel)
    unregister_class(NA_1D_Tools_Misc_Filter_Face_Angles)
    unregister_class(NA_1D_Tools_Misc_Multiclear_Normal_Data)
    unregister_class(NA_1D_Tools_Misc_Untriangle_Modifier)
    del WindowManager.na_1d_tools_misc_prop_face_angle


if __name__ == '__main__':
    register()
