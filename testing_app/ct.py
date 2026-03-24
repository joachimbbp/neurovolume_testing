import datasets
import numpy as np
from pathlib import Path
import os
import neurovolume as nv
from util import env_field as e

# WIP: conitnue here!
def bunny():
    print("gz path and url: ", e("bunny_gz_path"), e("bunny_ct_url"))
    #DRY with mri BOLD?
    os.makedirs(os.path.dirname(e("bunny_gz_path")), exist_ok=True)
    bunny = datasets.get_tar_gz(e("bunny_gz_path"), e("bunny_ct_url"))
    print(bunny)
    # scaled = nv.scale(volume, 0.015)
    # prepped = nv.prep_ndarray(volume, axes)
    # prepped[prepped < THRESH] = 0.0
    # nv.ndarray_to_vdb(prepped, label, output_dir=output_dir)
