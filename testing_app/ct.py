from urllib.request import urlretrieve
import gzip
import shutil
import numpy as np
from pathlib import Path
import os
import neurovolume as nv


# WIP:
def bunny():
    scaled = nv.scale(volume, 0.015)
    prepped = nv.prep_ndarray(volume, axes)
    prepped[prepped < THRESH] = 0.0
    nv.ndarray_to_vdb(prepped, label, output_dir=output_dir)
