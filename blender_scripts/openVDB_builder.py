import bpy

from pathlib import Path

repo_path = Path(bpy.data.filepath).parent.parent
print("hello from openVDB_builder.py")
