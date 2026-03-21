# INSTRUCTIONS: must be run from project root, NOT ./tests
import numpy as np
from urllib.request import urlretrieve
import gzip
import shutil
import os
from dotenv import load_dotenv
from pathlib import Path

import neurovolume as nv  # will give an error before you run the makefile

# use-case specific dependencies:
import nibabel as nib
from nibabel.nifti1 import Nifti1Image

load_dotenv(Path(__file__).parent.parent / ".env")
# NOTE: this has to be run form root
test_data_path = "./media/test_files"
vdb_out = "./media/vdb_out"


def download_test_data():
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


# TODO:
# this is blocky and making it higher resolution makes it gigantic
# once we add transform, make this much MUCH larger and then scale down
# so it matches the default cube!
def _build_pyramid(size=64):
    # LLM: generated this for testing
    """
    Build a 3D pyramid in a numpy array.

    Args:
        size: Size of the cubic array (default 64x64x64)

    Returns:
        3D numpy array with pyramid structure (1.0 inside, 0.0 outside)
    """
    arr = np.zeros((size, size, size), dtype=np.float32)

    center = size // 2

    # Build pyramid layer by layer from bottom to top
    for z in range(size):
        # Calculate the radius at this height
        # Pyramid tapers from base (bottom) to point (top)
        height_ratio = 1.0 - (z / size)
        max_radius = center * height_ratio

        # Fill the square cross-section at this height
        for y in range(size):
            for x in range(size):
                # Distance from center in x and y
                dx = abs(x - center)
                dy = abs(y - center)

                # Check if point is inside pyramid at this height
                # Using Chebyshev distance (square pyramid)
                if max(dx, dy) <= max_radius:
                    arr[z, y, x] = 1.0

    print("Pyramid build")
    return arr, True


def test_hello():
    nv.hello()


# TODO: Better testing! This is very incomplete as of now


# TODO: rewrite this with the new functionality
def test_pyramid(size=64000):
    pyramid, built = _build_pyramid()
    assert built, "Pyramid should build successfully"

    identity = np.eye(4)
    # perhaps this pattern isn't the best?
    print(f"identity matrix: \n{identity}")
    scaled = nv.scale(identity, 0.030)
    print(f"scaled affine: \n{scaled}")
    translated = nv.translate(scaled, 1.6, 0.7, 0.2)
    print(f"translated affine:\n{translated}")
    rotated = nv.rotate(translated, 0, 0, np.deg2rad(44))
    print(f"rotated matrix: \n{rotated}")

    prepped_pyramid = nv.prep_ndarray(pyramid, (2, 1, 0))

    os.makedirs(vdb_out, exist_ok=True)
    nv.ndarray_to_vdb(
        prepped_pyramid,
        "pyramid_offset",
        output_dir=vdb_out,
        transform=rotated,
    )
    print("pyramids saved")


def _test_pattern_pos(affine: np.ndarray) -> np.ndarray:
    brain_scale = 0.01
    brain_y_move = -2.38251
    scaled = nv.scale(affine, brain_scale)
    moved = nv.translate(scaled, 0, brain_y_move, 0)
    return moved


# TODO: throughout, maybe use paths not str
def test_anat_static(nii: str):
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


def test_bold_seq_direct(nii: str):
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
