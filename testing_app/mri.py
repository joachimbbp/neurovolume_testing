# INSTRUCTIONS: must be run from project root, NOT ./tests
import numpy as np
from urllib.request import urlretrieve
from util import env_field as e
import os
import datasets
import neurovolume as nv  # will give an error before you run the makefile
from pathlib import Path
# use-case specific dependencies:
import nibabel as nib
from nibabel.nifti1 import Nifti1Image


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
    scaled = nv.scale(affine, 0.0238818)
    moved = nv.translate(scaled,  0.066114, 0.429743, -0.4628) 
    return moved


def anat() -> Path:
    """
    returns path to anat vdb
        
    """
    nii = datasets.get_gz(e("anat_gz_path"), e("anat_url"))
    os.makedirs(e("vdb_out"), exist_ok=True)
    img = nib.load(nii)
    assert isinstance(img, Nifti1Image)  # pyright complained, claude suggested this fix
    data = np.array(img.get_fdata(), order="C", dtype=np.float32)
    affine = img.affine
    assert isinstance(affine, np.ndarray)

    basename = "anat_positioned"
    output_dir = Path(e("vdb_out"))
    return  nv.ndarray_to_vdb(
        nv.prep_ndarray(data, (0, 2, 1)),
        basename,
        output_dir=output_dir,
        transform=_test_pattern_pos(affine),
    )

def bold() -> Path | None:
    """
    returns path to bold folder, or None if error
        
    """
    os.makedirs(os.path.dirname(e("bold_gz_path")), exist_ok=True)
    nii = datasets.get_gz(e("bold_gz_path"), e("bold_url"))
    os.makedirs(e("vdb_out"), exist_ok=True)
    img = nib.load(nii)
    assert isinstance(img, Nifti1Image)
    data = np.array(img.get_fdata(), order="C", dtype=np.float32)

    affine = img.affine
    assert isinstance(affine, np.ndarray)

    basename = "bold_positioned"
    output_dir = Path(e("vdb_out"))
    return nv.ndarray_to_vdb(
        nv.prep_ndarray(data, (3, 0, 2, 1)),
        basename,
        source_fps=int(_get_fps(img)),
        output_dir=output_dir,
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
