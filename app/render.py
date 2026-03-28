import json
from util import env_field as e

# def render()
#     result = subprocess.run(
#         [
#             "blender",
#             "--background",  # no UI
#             "--python",
#             "./testing_app/blender_script.py",  # because you will run from root
#         ],
#         capture_output=True,
#         text=True,
#     )

#     # print(result.stdout)
#     # print(result.stderr)  # Blender logs and Python errors go here

# def from_bridge(b: dict):
    # such a hacky solution...
    # and could be cleaned up too
    # but it should work
    # with open(e('bridge'), 'w') as f:
    #     json.dump(b, f, indent=4)    
    # for scene in b:
    #     print(scene)
    #     # with open(e('scene'), 'w') as f:
        #     f.write(scene)
        
# blender existing.blend --background --python import_vdb.py    
def from_bridge():
    with open(".bridge", 'r') as b:
        bd = json.load(b)
        for scene in bd:
            print(bd[scene])
            with open(e('scene'), 'w') as f:
                json.dump(bd[scene], f)

            # for data in bd[scene]:
            #     vdb_info = bd[scene][data]
            #     print(vdb_info)
            #     print(type(vdb_info))
                
                # add the vdb
                # and the material
                # rendeer


#=-------
import os
from util import env_field as e
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(__file__).parent.parent / ".env")
def bpy_scratch():
    with open(e('scene'), 'r') as f:
        scene_files = json.load(f)
    for file in scene_files:
        print("file : ", file)
        vdb_path = scene_files[file]['vdb']
        mat = scene_files[file]['mat']
        print(f"mat: {mat}\nvdb: {vdb_path}")
# from_bridge()
bpy_scratch()
# from_bridge()
