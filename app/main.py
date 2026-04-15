import neurovolume as nv
from scipy.ndimage import gaussian_filter
from skimage.restoration import denoise_bilateral
import scipy
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
from scipy.ndimage import median_filter
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

bunny = np.stack(
    # FIX: hard coded resolution
    [np.frombuffer(f.read_bytes(), dtype="<u2").reshape(512, 512) for f in slice_files],
    axis=0,
)


def snr_image(arr, noise_max=2000, signal_min=8000):
    noise_region = arr[arr < noise_max]  # definitely air
    signal_region = arr[arr >= signal_min]  # definitely tissue
    return np.mean(signal_region) / np.std(noise_region)


print(f"bunny vol range: {bunny.min()} - {bunny.max()}")

# okay sort of unhinged idea but what if we just start by clipping the top and bottom 10%?
# low = np.percentile(bunny, 0)  # crazy high noise floor on this one tbh
# prepped = np.where(bunny < low, 0, bunny)

# prepped = median_filter(prepped, size=3)


# BIG JANKY MESS: I think we should jsut try median filter for the vdbs lets see
denoised_bunny = median_filter(bunny, size=3)
# sort of renders snr useless if low is the floor!
comp_index = int(bunny.shape[0] / 2)


print(f"bunny_vol signal to noise: {snr_image(bunny)}")
print(f"bunny denoise signal to noise: {snr_image(denoised_bunny)}")

# blurred = gaussian_filter(bunny_vol_clip, sigma=1.0)

debug.save_slice_as_png(denoised_bunny, comp_index, "./bunny_denoise.png")
debug.save_slice_as_png(bunny, comp_index, "./bunny.png")


output_dir = Path(e("vdb_out"))
print(output_dir)

nv.ndarray_to_vdb(
    nv.prep_ndarray(denoised_bunny, (0, 1, 2)),
    "denoised_bunny",
    output_dir=str(output_dir),
    transform=nv.scale(np.eye(4), 0.0015),
)

nv.ndarray_to_vdb(
    nv.prep_ndarray(bunny, (0, 1, 2)),
    "bunny",
    output_dir=str(output_dir),
    transform=nv.scale(np.eye(4), 0.0015),
)

# show non dithered
# debug.save_slice_as_png(bunny_vol, comp_index, "./og.png")
# print(comp_index)
# volume_dithered = dither.dither(blurred, 256)
# # print(volume_dithered)
# debug.save_slice_as_png(volume_dithered, comp_index, "./dithered_8bit.png")
# print("DONE!")
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
