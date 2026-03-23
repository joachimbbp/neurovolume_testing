# LLM copy pasta to starta
#
#
import numpy as np
from pathlib import Path
import os
import neurovolume as nv

nv.hello()

DATA_DIR = Path("/Users/joachimpfefferkorn/Downloads/bunny ct 01")
SLICE_FILES = sorted(
    [f for f in DATA_DIR.iterdir() if f.name.isdigit()],
    key=lambda f: int(f.name),
)

# Load all axial slices into a volume: shape (Z, Y, X) = (361, 512, 512)
print(f"Loading {len(SLICE_FILES)} slices...")
volume = np.stack(
    [np.frombuffer(f.read_bytes(), dtype="<u2").reshape(512, 512) for f in SLICE_FILES],
    axis=0,
)
print(f"Volume shape: {volume.shape}, dtype: {volume.dtype}")


output_dir = "../media/vdb_out"
os.makedirs(output_dir, exist_ok=True)

prepped_bunny = nv.prep_ndarray(volume, (2, 1, 0))  # shot in the dark nums
nv.ndarray_to_vdb(
    prepped_bunny,
    "pyramid_offset",
    output_dir=output_dir,
)

print("bunny saved")

# Axial slices are the Z axis → coronal slice is perpendicular (fixed Y index)
# volume[z, y, x]: coronal = volume[:, y_mid, :] → shape (Z, X)
# y_mid = volume.shape[1] // 2
# coronal = volume[:, y_mid, :]  # shape (361, 512)

# # Normalize to 8-bit for saving as PNG
# lo, hi = coronal.min(), coronal.max()
# coronal_8bit = ((coronal - lo) / (hi - lo) * 255).astype(np.uint8)

# out_path = DATA_DIR / "coronal_slice.png"
# Image.fromarray(coronal_8bit).save(out_path)
# print(f"Saved coronal slice (y={y_mid}) → {out_path}")
