import subprocess


def render_tests():
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

    print(result.stdout)
    print(result.stderr)  # Blender logs and Python errors go here
