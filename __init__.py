# bl_info
bl_info = {
    "name": "3Dlut_addon",
    "description": "import&apply 3Dlut",
    "author": "Suemura",
    "version": (0, 0, 1, 0),
    "blender": (2, 83, 0),
    "support": "TESTING",
    "category": "Render",
    "location": "UV/Image Editor and View Layers",
    "warning": "",
    "wiki_url": "",
    "tracker_url": ""
}

import bpy
import os, os.path
from . import apply_lut_image
from bpy.props import *
from bpy_extras.io_utils import ImportHelper

class LUT_PT_tools(bpy.types.Panel):
    bl_label = "Lut_panel"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Luts"

    # properties    
    bpy.types.Scene.lut_import_pass = bpy.props.StringProperty(name = "",)
    bpy.types.Scene.lut_import_directory = bpy.props.StringProperty(name = "",)
    bpy.types.Scene.lut_import_name = bpy.props.StringProperty(name = "",)
    bpy.types.Scene.image_output_directory = bpy.props.StringProperty(name = "",)
    bpy.types.Scene.image_output_name = bpy.props.StringProperty(name = "",)
    bpy.types.Scene.image_output_pass = bpy.props.StringProperty(name = "",)
    bpy.types.Scene.temp_image_pass = bpy.props.StringProperty(name = "",)


    def draw(self, context):
        layout = self.layout
        scene = context.scene
        col = layout.column(align=True)

        col.label(text="import lut")
        col.operator("luts.open_import_filebrowser", text="set_import_lut_directory")
        col.prop(scene, "lut_import_directory", text="")
        col.prop(scene, "lut_import_name", text="")

        # col.label(text="output image pass")
        # col.operator("luts.open_output_filebrowser", text="set_output_image_directory")
        # col.prop(context.scene, "image_output_directory", text="")
        # col.prop(context.scene, "image_output_name", text="")
        
        layout.label(text="select image:")
        layout.prop(scene, "image_list_enum", text="")

        col.prop(scene, "temp_image_pass", text="")
        col.operator("lut.apply_lut", text="apply")



class LUT_OT_open_import_filebrowser(bpy.types.Operator, ImportHelper):
    bl_idname = "luts.open_import_filebrowser"
    bl_label = "Set import path"
    filter_glob = StringProperty( default="*.cube;*.CUBE", options={'HIDDEN'} )

    def execute(self, context):
        filename, extension = os.path.splitext(self.filepath)
        path_pair = os.path.split(self.filepath)
        context.scene["lut_import_directory"] = path_pair[0] + "\\"
        context.scene["lut_import_name"] = path_pair[1]
        context.scene["lut_import_pass"] = context.scene["lut_import_directory"] + context.scene["lut_import_name"]
        return {'FINISHED'}

class LUT_OT_open_output_filebrowser(bpy.types.Operator, ImportHelper):
    bl_idname = "luts.open_output_filebrowser"
    bl_label = "Set output path"
    filter_glob = StringProperty( default="*", options={'HIDDEN'} )

    def execute(self, context):
        filename, extension = os.path.splitext(self.filepath)
        path_pair = os.path.split(self.filepath)
        context.scene["image_output_directory"] = path_pair[0] + "\\"
        context.scene["image_output_name"] = path_pair[1]
        if context.scene["image_output_name"] == "":
            context.scene["image_output_name"] = "out.png"
        context.scene["image_output_pass"] = context.scene["image_output_directory"] + context.scene["image_output_name"]
        return {'FINISHED'}

# update enum property
def get_object_list_callback(scene, context):
    items = []
    images = bpy.data.images
    for img in images:
        img_name = img.name
        items.append((img_name, img_name, ""))
    return items
# apply new enum property
def init_props():
    scene = bpy.types.Scene
    scene.image_list_enum = EnumProperty(
    name="image list",
    description="image list",
    items=get_object_list_callback
    )


# クラスの登録
def register():
    for cls in classes:
        print("Register : " + str(cls))
        bpy.utils.register_class(cls)
    init_props()

# クラスの登録解除
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

# 登録するクラス
classes = [
    # export_gif.GIF_OT_ExportOperator,
    apply_lut_image.LUT_OT_ExportOperator,
    LUT_PT_tools,
    LUT_OT_open_import_filebrowser,
    LUT_OT_open_output_filebrowser
]

if __name__ == '__main__':
    register()


