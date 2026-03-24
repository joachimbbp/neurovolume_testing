import datasets
import numpy as np
from pathlib import Path
import os
import neurovolume as nv
from util import env_field as e

# WIP: conitnue here!
def bunny():
    print("gz path and url: ", e("bunny_gz_path"), e("bunny_ct_url"))
    bunny = datasets.get(e("bunny_gz_path"), e("bunny_ct_url"))
    
    # scaled = nv.scale(volume, 0.015)
    # prepped = nv.prep_ndarray(volume, axes)
    # prepped[prepped < THRESH] = 0.0
    # nv.ndarray_to_vdb(prepped, label, output_dir=output_dir)
