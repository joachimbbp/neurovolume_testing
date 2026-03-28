import bpy
from dotenv import load_dotenv
from pathlib import Path
import json
import os

load_dotenv(Path(__file__).parent.parent / ".env")
scene = os.getenv('scene')
with open(scene, 'r') as f:
        scene_files = json.load(f)


bpy.ops.object.volume_import(
    filepath="/path/to/yourfile.vdb",
    files=[{"name": "yourfile.vdb"}]
)

bpy.ops.wm.save_as_mainfile(filepath="/path/to/output.blend")
