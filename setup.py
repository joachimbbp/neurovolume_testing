import subprocess
import os
import shutil

source_url = "https://github.com/joachimbbp/neurovolume.git"
source_repo = "/Users/joachimpfefferkorn/repos/neurovolume/"
fixture_repo = "./neurovolume/"


def _establish_folder(folder):
    # clear folder if its there
    if os.path.isdir(folder):
        subprocess.run(
            [f"rm -rf {folder} y"],
            check=True,
            shell=True,
        )
    else:
        os.mkdir(folder)


def from_local(
    path,
    source_repo=source_repo,
    fixture_repo=fixture_repo,
):
    shutil.copytree(source_repo, fixture_repo)


#
# import shutil
#
# shutil.copytree("source_folder", "destination_folder")
#


def from_hash(
    commit_hash,
    source_url=source_url,
    fixture_repo=fixture_repo,
):

    # Clone the repo first
    subprocess.run(
        [f"git clone {source_url} {fixture_repo}"],
        check=True,
        shell=True,
    )
    # Then checkout the specific hash
    subprocess.run(
        ["git checkout", commit_hash],
        cwd=fixture_repo,
        check=True,
        shell=True,
    )

    subprocess.run(
        ["uv build"],
        cwd=fixture_repo,
        check=True,
        shell=True,
    )
    subprocess.run(
        "uv run python -m ziglang build && uv run pytest tests -s",
        cwd=fixture_repo,
        check=True,
        shell=True,
    )
