from pathlib import Path
import subprocess


def build_root() -> Path:
    cwd = Path.cwd()
    if not (cwd / "Makefile").exists():
        raise EnvironmentError(f"Must be run from repo root, currently: {cwd}")
    return Path(__file__).parent.parent


ROOT = build_root()
def build(
    source_repo=str(ROOT.parent / "neurovolume"),  # for my setup, assuming running from root
    blender=subprocess.check_output(["which", "blender"]).decode().strip(),
):
    test_file_folder = f"{ROOT}/media/test_files"
    env = {
        "root": ROOT,
        "source_neurovolume": source_repo,
        "blender": blender,
        "blender_template_file": f"{ROOT}/blender_files/newbrains.blend",
        "anat_url": "https://s3.amazonaws.com/openneuro.org/ds003548/sub-01/anat/sub-01_T1w.nii.gz?versionId=5ZTXVLawdWoVNWe5XVuV6DfF2BnmxzQz",
        "bold_url": "https://s3.amazonaws.com/openneuro.org/ds003548/sub-01/func/sub-01_task-emotionalfaces_run-1_bold.nii.gz?versionId=tq8Y3ktm31Aa8JB0991n9K0XNmHyRS1Q",
        "test_file_folder": test_file_folder,
        "anat_gz_path": f"{test_file_folder}/sub-01_T1w.nii.gz",
        "bold_gz_path": f"{test_file_folder}/sub-01_task-emotionalfaces_run-1_bold.nii.gz",
        "bunny_ct_url": "https://graphics.stanford.edu/data/voldata/bunny-ctscan.tar.gz",
        "bunny_gz_path":f"{test_file_folder}/bunny_ct.tar.gz",
        "vdb_out": f"{ROOT}/media/vdb_out",
    }
    env_path = ROOT / ".env"
    with open(env_path, "w") as f:
        for key, value in env.items():
            f.write(f"{key}={value}\n")
    print("ROOT: ", ROOT)
    print("ENV PATH: ", env_path)
