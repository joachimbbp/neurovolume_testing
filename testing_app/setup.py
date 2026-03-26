import subprocess
import os
import shutil
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")


def _establish_folder(folder):
    # clear folder if its there
    print("establishing folder...")
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


# must build env first
def from_local(
    source_repo=str(os.getenv("source_neurovolume")),
    fixture_repo="./neurovolume",
):
    _establish_folder(fixture_repo)
    print(f"copying contents from {source_repo} to {fixture_repo}...")
    shutil.copytree(source_repo, fixture_repo)


# TODO: later
# source_url = "https://github.com/joachimbbp/neurovolume.git"
# def from_hash(
#     commit_hash,
#     source_url=source_url,
#     fixture_repo=fixture_repo,
# ):

#     _establish_folder(fixture_repo)
#     print(f"cloning repo from {source_url} to {fixture_repo}...")
#     subprocess.run(
#         [f"git clone {source_url} {fixture_repo}"],
#         check=True,
#         shell=True,
#     )
#     print(f"checking out hash {commit_hash}...")
#     subprocess.run(
#         ["git checkout", commit_hash],
#         cwd=fixture_repo,
#         check=True,
#         shell=True,
#     )


def build_and_link(repo="./neurovolume"):
    print("building library...")
    subprocess.run(["uv sync"], cwd=repo, check=True, shell=True)
    subprocess.run(
        ["uv run python -m ziglang build"],
        cwd=repo,
        check=True,
        shell=True,
    )


# def test_pattern():
#     subprocess.run(
#         "uv run python -m ziglang build && uv run pytest tests -s",
#         cwd=fixture_repo,
#         check=True,
#         shell=True,
#     )
