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
with open(".bridge", 'r') as b:
    # with open(e('bridge'), 'r') as b:
    data = json.load(b)
    print("type: ", type(data))
    print(data)
