import subprocess


def render()
    result = subprocess.run(
        [
            "blender",
            "--background",  # no UI
            "--python",
            "./testing_app/blender_script.py",  # because you will run from root
        ],
        capture_output=True,
        text=True,
    )

    # print(result.stdout)
    # print(result.stderr)  # Blender logs and Python errors go here

def from_bridge(bridge: dict):
    for scene in bridge:
        for vdb in bridge[scene]:
            print("  vdb: ", vdb)
            print("    vdb path: ", bridge[scene][vdb]['vdb'])
            print("    vdb mat: ", bridge[scene][vdb]['mat'])
