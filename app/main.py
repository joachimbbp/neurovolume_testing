import dither
import debug
import env
from dotenv import load_dotenv
from pathlib import Path
import subprocess
import geo
import datasets
from util import env_field as e
import ct
import numpy as np
# RUN FROM ROOT!

# WARN: this is becomeing sort of a scratch atm

env.build()
load_dotenv(Path(__file__).parent.parent / ".env")

# inlined bunny stuff:
bunny = datasets.get_tar_gz(e("bunny_gz_path"), e("bunny_ct_url"))
slice_files = sorted(
    [f for f in Path(bunny).iterdir() if f.name.isdigit()],
    key=lambda f: int(f.name),
)
volume = np.stack(
    # FIX: hard coded resolution
    [np.frombuffer(f.read_bytes(), dtype="<u2").reshape(512, 512) for f in slice_files],
    axis=0,
)
comp_index = int(volume.shape[0] / 2)
# show non dithered
debug.save_slice_as_png(volume, comp_index, "./og.png")
print(comp_index)
volume_dithered = dither.dither(volume, 2)
print(volume_dithered)
debug.save_slice_as_png(volume_dithered, comp_index, "./dithered.png")
print("DONE!")
# ct_bunny = ct.bunny()


# # build the pyramid with Neurovolume
# compare_folder = Path(e("vdb_out"))
# geo.pyramid("neurovolume_pyramid")

# # builds the pyramid with OpenVDB
# subprocess.run(
#     [
#         "blender",
#         "--background",  # no UI
#         "--python",
#         # until you modify the bridge, this will need to have the
#         # vdb paths hard coded in it!
#         "./blender_scripts/openVDB_builder.py",
#     ]
# )

# print("OpenVDB and Neurovolume written for comparison!")
