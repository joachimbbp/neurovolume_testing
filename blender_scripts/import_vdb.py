import bpy
from dotenv import load_dotenv
from pathlib import Path
import json
import os

load_dotenv(Path(__file__).parent.parent / ".env")
with open(str(os.getenv('scene')), 'r') as f:
    scene_files = json.load(f)
for file in scene_files:
    print("file : ", file)
    vdb_path = scene_files[file]['vdb']
    mat = scene_files[file]['mat']
    print(f"mat: {mat}\nvdb: {vdb_path}")

    bpy.ops.object.volume_import(
        filepath=vdb_path,
        files=[{file: f"{file}.vdb"}]
    )
