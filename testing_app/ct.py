import datasets
import numpy as np
from pathlib import Path
import os
import neurovolume as nv
from util import env_field as e
import numpy as np

# WIP: conitnue here!
def bunny():
    print("gz path and url: ", e("bunny_gz_path"), e("bunny_ct_url"))
    #DRY with mri BOLD?
    os.makedirs(os.path.dirname(e("bunny_gz_path")), exist_ok=True)
    bunny = datasets.get_tar_gz(e("bunny_gz_path"), e("bunny_ct_url"))
    print(bunny)

    slice_files = sorted(
        [f for f in Path(bunny).iterdir() if f.name.isdigit()],
        key=lambda f: int(f.name),
    )
    volume = np.stack(
        #FIX: hard coded resolution
        [np.frombuffer(f.read_bytes(), dtype="<u2").reshape(512, 512) for f in slice_files],
        axis=0,
    )
    print("volume shape: ", volume.shape)
    prepped = nv.prep_ndarray(volume, (0,1,2))
    prepped[prepped < 0.4] = 0.0 # thresholding
    nv.ndarray_to_vdb(
                      prepped,
                      "bunny_ct",
                      output_dir=e("vdb_out"),
                      transform=nv.scale(np.eye(4), 0.0015)
                  )
