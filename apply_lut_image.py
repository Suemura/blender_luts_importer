import bpy, os, shutil, pathlib

class LUT_OT_ExportOperator(bpy.types.Operator):
    bl_idname = "lut.apply_lut"
    bl_label = "apply lut"
    bl_options = {"REGISTER", "UNDO"}

    def copy_current_image(self, context, temp_image):
        select_image = bpy.data.images[context.scene.image_list_enum]
        original_path = pathlib.Path(select_image.filepath)
        original_path = str(original_path.resolve())
        print("original_path : " + original_path)
        shutil.copyfile(original_path, temp_image)

    def save_image_and_render_setting(self, context, img):
        img_settings = {}
        # scene settings
        img_settings["render_file_format"] = context.scene.render.image_settings.file_format
        img_settings["render_color_mode"] = context.scene.render.image_settings.color_mode
        img_settings["render_color_depth"] = context.scene.render.image_settings.color_depth
        # image settings
        img_settings["img_colorspace_settings"] = img.colorspace_settings.name
        img_settings["img_alpha_mode"] = img.alpha_mode
        img_settings["img_file_format"] = img.file_format
        img_settings["img_filepath"] = img.filepath

        return img_settings

    def undo_image_and_render_setting(self, context, img, original_setting):
        original_setting
        # scene settings
        context.scene.render.image_settings.file_format = original_setting["render_file_format"]
        context.scene.render.image_settings.color_mode = original_setting["render_color_mode"]
        context.scene.render.image_settings.color_depth = original_setting["render_color_depth"]
        # image settings
        img.colorspace_settings.name = original_setting["img_colorspace_settings"]
        img.alpha_mode = original_setting["img_alpha_mode"]
        img.file_format = original_setting["img_file_format"]
        img.filepath = original_setting["img_filepath"]

    def save_temp_rendered_image(self, context, temp_image, img):
        # scene settings
        context.scene.render.image_settings.file_format = "TIFF"
        context.scene.render.image_settings.color_mode = "RGB"
        context.scene.render.image_settings.color_depth = "16"
        # image settings
        img.colorspace_settings.name = "sRGB"
        img.alpha_mode = "NONE"
        img.file_format = 'TIFF'
        img.filepath = temp_image
        img.save_render(temp_image, scene = context.scene)
        context.scene["temp_image_pass"] = temp_image

    def apply_lut(self, context, temp_image, temp_pass):
        from colour import read_LUT
        from colour import write_image, read_image
        lut3d = read_LUT(context.scene["lut_import_pass"])
        luminance_map_img = lut3d.apply(read_image(temp_image))

        write_image(luminance_map_img, temp_pass, bit_depth='uint8')
        new_image = bpy.data.images.load(temp_pass, check_existing=True)
        new_image.reload()

    def execute(self, context):
        print("test : lut_execute")
        temp_dir = os.path.dirname(os.path.abspath(__file__))
        temp_image = temp_dir + "\\img.tiff"
        temp_pass = temp_dir + "\\temp.tiff"
        if os.path.isfile(temp_image):
            os.remove(temp_image)

        select_image_name = context.scene.image_list_enum
        img = bpy.data.images[select_image_name]
        original_setting = self.save_image_and_render_setting(context, img)

        if select_image_name == "Render Result":
            pass
        else:
            self.copy_current_image(context, temp_image)
        self.save_temp_rendered_image(context, temp_image, img)
        self.apply_lut(context, temp_image, temp_pass)

        self.undo_image_and_render_setting(context, img, original_setting)
        os.remove(temp_image)

        return {"FINISHED"}
