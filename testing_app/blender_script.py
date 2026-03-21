# copypasta nonsense that I will henceforth edit


import bpy

# --- Config ---
VDB_PATHS = [
    "media/vdb_out/anat_offset.vdb",
    "media/vdb_out/pyramid_offset.vdb",
]
MATERIAL_BLEND = "blender_files/newbrains.blend"
MATERIAL_NAME = "anat_party"
OUTPUT_PATH = "media/png_out/render.png"


scene = bpy.context.scene
eevee = scene.eevee

# Resolution — 0 = 1:1, 1 = Half, 2 = Quarter
eevee.volumetric_tile_size = "1"  # '2', '4', '8', '16' — use '2' for 1:1...

# --- Append material from another .blend ---
with bpy.data.libraries.load(MATERIAL_BLEND, link=False) as (data_from, data_to):
    data_to.materials = [MATERIAL_NAME]

mat = bpy.data.materials.get(MATERIAL_NAME)
if mat is None:
    raise RuntimeError(f"Material '{MATERIAL_NAME}' not found in {MATERIAL_BLEND}")

# --- Load VDBs and assign material ---
for vdb_path in VDB_PATHS:
    bpy.ops.object.volume_import(filepath=vdb_path)
    vdb_obj = bpy.context.selected_objects[0]
    if vdb_obj.data.materials:
        vdb_obj.data.materials[0] = mat
    else:
        vdb_obj.data.materials.append(mat)

# --- Render ---
bpy.context.scene.render.filepath = OUTPUT_PATH
bpy.context.scene.render.image_settings.file_format = "PNG"
bpy.ops.render.render(write_still=True)
