import subprocess
import os


def get_repo(
    commit_hash,
    folder,
    url="https://github.com/joachimbbp/neurovolume.git",
):
    # clear folder if its there
    if os.path.isdir(folder):
        subprocess.run(
            [f"rm -rf {folder} y"],
            check=True,
            shell=True,
        )
    else:
        os.mkdir(folder)

    # Clone the repo first
    subprocess.run(
        [f"git clone {url} {folder}"],
        check=True,
        shell=True,
    )
    # Then checkout the specific hash
    subprocess.run(
        ["git checkout", commit_hash],
        cwd=folder,
        check=True,
        shell=True,
    )

    subprocess.run(["uv build"], cwd=folder, check=True, shell=True)
    subprocess.run(
        "uv run python -m ziglang build && uv run pytest tests -s",
        cwd=folder,
        check=True,
        shell=True,
    )


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


folder = "./neurovolume/"

get_repo("62c0c14e40312474d218baaac66c3e5adb812fb0", folder)

render_tests()
