import bpy, os
from colour import read_LUT
from colour import write_image, read_image

class LUT_OT_ExportOperator(bpy.types.Operator):
    bl_idname = "lut.apply_lut"
    bl_label = "apply lut"
    bl_options = {"REGISTER", "UNDO"}

    def save_temp_rendered_image(self, context, temp_image):
        render_img = bpy.data.images["Render Result"]
        render_img.colorspace_settings.name = "sRGB"
        # render_img.use_alpha = True
        
        # scene settings
        context.scene.render.image_settings.file_format = "TIFF"
        context.scene.render.image_settings.color_mode = "RGB"
        context.scene.render.image_settings.color_depth = "16"
        
        # image settings
        render_img.alpha_mode = "NONE"
        render_img.file_format = 'TIFF'
        render_img.filepath = temp_image
        render_img.save_render(temp_image, scene = context.scene)
        context.scene["temp_image_pass"] = temp_image

    def apply_lut(self, context, temp_image, temp_pass):
        lut3d = read_LUT(context.scene["lut_import_pass"])
        luminance_map_img = lut3d.apply(read_image(temp_image))
        
        write_image(luminance_map_img, temp_pass, bit_depth='uint8')
        new_image = bpy.data.images.load(temp_pass, check_existing=True)

    def execute(self, context):
        print("test : lut_execute")
        temp_dir = os.path.dirname(os.path.abspath(__file__))
        temp_image = temp_dir + "\\img.tiff"
        temp_pass = temp_dir + "\\temp.tiff"

        self.save_temp_rendered_image(context, temp_image)
        self.apply_lut(context, temp_image, temp_pass)

        return {"FINISHED"}
