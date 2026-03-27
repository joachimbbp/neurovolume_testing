import bpy
from dotenv import load_dotenv
from pathlib import Path
import json
import os

load_dotenv(Path(__file__).parent.parent / ".env")
bridge = os.getenv('bridge')

# with open("/path/to/output.json") as f:
#       data = json.load(f)load_dotenv(Path(__file__).parent.parent / ".env")

bpy.ops.object.volume_import(
    filepath="/path/to/yourfile.vdb",
    files=[{"name": "yourfile.vdb"}]
)

bpy.ops.wm.save_as_mainfile(filepath="/path/to/output.blend")
