import subprocess
import setup


def render_tests():
    result = subprocess.run(
        [
            "blender",
            "--background",  # no UI
            "--python",
            "scene.py",
        ],
        capture_output=True,
        text=True,
    )

    print(result.stdout)
    print(result.stderr)  # Blender logs and Python errors go here


setup.from_hash("62c0c14e40312474d218baaac66c3e5adb812fb0")

# render_tests()
