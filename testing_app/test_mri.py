# INSTRUCTIONS: must be run from project root, NOT ./tests
import numpy as np
from urllib.request import urlretrieve
import gzip
import shutil
import os

import neurovolume as nv  # will give an error before you run the makefile

# use-case specific dependencies:
import nibabel as nib
from nibabel.nifti1 import Nifti1Image


def download():
    # download and unzip
    def dau(gz_path: str, url: str):
        nii_name = f"{gz_path}".split("/")[-1][:-3]
        nii_path = f"{os.getenv('test_file_folder')}/{nii_name}"
        if not os.path.exists(gz_path):
            print(f"Downloading {nii_name} source file from {url}...")
            urlretrieve(url, gz_path)
        else:
            print(f"{nii_name} alreay exists")
        # TODO: some edge cases
        if not os.path.exists(nii_path):
            print(f"Unzipping {nii_path}")
            with gzip.open(gz_path, "rb") as f_in:
                with open(nii_path, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
        return nii_path

    anat = dau(str(os.getenv("anat_gz_path")), str(os.getenv("anat_url")))
    bold = dau(str(os.getenv("bold_gz_path")), str(os.getenv("bold_url")))
    return anat, bold


def _get_fps(img, loud=False) -> float:
    # this should probably live in whatever
    # fMRI processing pipeline you are working on
    header = img.header
    tr = header["pixdim"][4]
    time_unit = header.get_xyzt_units()[1]

    if time_unit == "msec":
        tr /= 1000
    elif time_unit == "usec":
        tr /= 1_000_000

    fps: float = 1.0 / tr if tr > 0 else 0
    if loud:
        print(f"time unit {time_unit}, FPS: {fps}")
    return fps


def _test_pattern_pos(affine: np.ndarray) -> np.ndarray:
    brain_scale = 0.01
    brain_y_move = -2.38251
    scaled = nv.scale(affine, brain_scale)
    moved = nv.translate(scaled, 0, brain_y_move, 0)
    return moved


# TODO: throughout, maybe use paths not str
def anat(vdb_out: str, nii: str):
    os.makedirs(vdb_out, exist_ok=True)
    img = nib.load(nii)
    assert isinstance(img, Nifti1Image)  # pyright complained, claude suggested this fix
    data = np.array(img.get_fdata(), order="C", dtype=np.float32)
    affine = img.affine
    assert isinstance(affine, np.ndarray)

    nv.ndarray_to_vdb(
        nv.prep_ndarray(data, (0, 2, 1)),
        "anat_offset",
        output_dir=vdb_out,
        transform=_test_pattern_pos(affine),
    )


def bold(vdb_out: str, nii: str):
    os.makedirs(vdb_out, exist_ok=True)
    img = nib.load(nii)
    assert isinstance(img, Nifti1Image)
    data = np.array(img.get_fdata(), order="C", dtype=np.float32)

    affine = img.affine
    assert isinstance(affine, np.ndarray)

    nv.ndarray_to_vdb(
        nv.prep_ndarray(data, (3, 0, 2, 1)),
        "bold_direct_offset",
        source_fps=int(_get_fps(img)),
        output_dir=vdb_out,
        transform=_test_pattern_pos(affine),
    )


# def test_bold_seq_fade():
#     img = nib.load(bold)
#     data = np.array(img.get_fdata(), order="C", dtype=np.float32)
#
#     nv.ndarray_to_vdb(
#         nv.prep_ndarray(data, (3, 0, 2, 1)),
#         "bold_fade",
#         source_fps=_get_fps(img),
#         output_dir=vdb_out,
#         interpolation_flag=1,  # TODO: enum on python side with named interpolations
#     )
