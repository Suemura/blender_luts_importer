# bl_info
bl_info = {
    "name": "3Dlut_addon",
    "description": "import&apply 3Dlut",
    "author": "Suemura",
    "version": (0, 0, 1, 1),
    "blender": (2, 82, 0),
    "support": "TESTING",
    "category": "Render",
    "location": "UV/Image Editor",
    "warning": "",
    "wiki_url": "",
    "tracker_url": ""
}

import bpy
import os, os.path, sys, subprocess
from . import apply_lut_image
from bpy.props import *
from bpy_extras.io_utils import ImportHelper

class LUT_OT_InstallColuur(bpy.types.Operator):
    bl_idname = "lut.install_colour"
    bl_label = "apply lut"
    bl_options = {"REGISTER", "UNDO"}
    mode = StringProperty()

    def check_installed_package(self, context, python_dir):
        # get installed package
        packages_message = subprocess.check_output(".\python.exe -m pip freeze", shell=True)
        package_message_list = packages_message.decode().split("\n")
        package_list = []
        for p in package_message_list:
            package_name = p.replace("\r", "")
            package_name = package_name.split("==")[0]
            package_list.append(package_name)
        print(package_list)

        if "colour-science" in package_list:
            context.scene["colour_science_status"] = "Installed!"
            return True
        else:
            context.scene["colour_science_status"] = "Not Installed."
            return False

    def execute(self, context):
        # python.exeのパスを取得
        blender_version = str(bpy.app.version_string)[:4]
        blender_pass = str(sys.executable)
        python_dir = os.path.dirname(blender_pass) +"\\"+blender_version+ "\\python\\bin\\"
        python_pass = python_dir + "python.exe"
        os.chdir(python_dir)
        pip_install_command = ".\python.exe -m pip install colour-science"
        pip_uninstall_command = ".\python.exe -m pip uninstall colour-science"

        installed = False
        if self.mode == "CHECK":
            installed = self.check_installed_package(context, python_dir)
        elif self.mode == "INSTALL":
            subprocess.call(pip_install_command, shell=True)
        elif self.mode == "UNINSTALL":
            subprocess.call(pip_uninstall_command, shell=True)
            
        return {"FINISHED"}

class LUT_PT_preferences(bpy.types.AddonPreferences):
    bl_idname = __package__
    bpy.types.Scene.colour_science_status = bpy.props.StringProperty(name = "", default="Please Check.")
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.label(text="initial settings : ")
        row = layout.row(align=True)
        row.operator("lut.install_colour", text="check").mode = "CHECK"
        row.prop(scene, "colour_science_status", text="")
        layout.operator("lut.install_colour", text="install colour-science package").mode = "INSTALL"
        layout.label(text="If you want to uninstall the library, please show the console", icon="ERROR")
        layout.operator("lut.install_colour", text="uninstall colour-science package").mode = "UNINSTALL"

class LUT_PT_tools(bpy.types.Panel):
    bl_label = "Lut_panel"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = "UI"
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

        col.label(text="select image:")
        col.prop(scene, "image_list_enum", text="")
        col.separator()
        col.operator("lut.apply_lut", text="apply LUT", icon="OUTLINER_OB_IMAGE")

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

        

def register():
    for cls in classes:
        print("Register : " + str(cls))
        bpy.utils.register_class(cls)
    init_props()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

classes = [
    apply_lut_image.LUT_OT_ExportOperator,
    LUT_PT_tools,
    LUT_PT_preferences,
    LUT_OT_open_import_filebrowser,
    LUT_OT_InstallColuur
]

if __name__ == '__main__':
    register()
