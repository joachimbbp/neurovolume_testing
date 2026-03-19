import subprocess
import os
import shutil
import sys

source_url = "https://github.com/joachimbbp/neurovolume.git"
source_repo = "/Users/joachimpfefferkorn/repos/neurovolume/"
fixture_repo = "./neurovolume/"


def _establish_folder(folder):
    # clear folder if its there
    if os.path.isdir(folder):
        print(f"{folder} exists, clearing contents...")
        subprocess.run(
            [f"rm -rf {folder} y"],
            check=True,
            shell=True,
        )
    else:
        print(f"{folder} does not exist, building now...")
        os.mkdir(folder)


def from_local(
    source_repo=source_repo,
    fixture_repo=fixture_repo,
):
    _establish_folder(fixture_repo)
    print(f"copying contents from {source_repo} to {fixture_repo}...")
    shutil.copytree(source_repo, fixture_repo)


def from_hash(
    commit_hash,
    source_url=source_url,
    fixture_repo=fixture_repo,
):

    _establish_folder(fixture_repo)
    print(f"cloning repo from {source_url} to {fixture_repo}...")
    subprocess.run(
        [f"git clone {source_url} {fixture_repo}"],
        check=True,
        shell=True,
    )
    print(f"checking out hash {commit_hash}...")
    subprocess.run(
        ["git checkout", commit_hash],
        cwd=fixture_repo,
        check=True,
        shell=True,
    )


def build_and_link(repo=fixture_repo):
    print("building library...")
    subprocess.run(
        ["uv build"],
        cwd=repo,
        check=True,
        shell=True,
    )
    lib_path = "./neurovolume/src/neurovolume/_native/libneurovolume.dylib"
    if os.path.exists(lib_path):
        print(f"library exists at {lib_path}")
        sys.path.append(lib_path)
    else:
        # TODO: error handling
        print(f"error: no library at {lib_path}")


# def test_pattern():
#     subprocess.run(
#         "uv run python -m ziglang build && uv run pytest tests -s",
#         cwd=fixture_repo,
#         check=True,
#         shell=True,
#     )
