import bpy
import logging
import subprocess
import sys
import numpy as np
from pathlib import Path
import openvdb as vdb

repo_path = Path(bpy.data.filepath).parent.parent
sys.path.insert(0, str((repo_path) / "app"))  # mostly claude copypasta
import geo

print("hello from openVDB_builder.py")


# from util import display_message


def pyramid() -> np.ndarray:
    pyramid, built = geo.build_pyramid()
    assert built, "Pyramid should build successfully"

    # perhaps this pattern isn't the best?
    return pyramid


def ndarray_to_openVDB(input: np.ndarray, output_basename: str):
    # claude copypasta to start

    # to match the ndarray rotation in geo.pyramid
    prepped = np.ascontiguousarray(np.transpose(input, (2, 1, 0)))  # Z,Y,X → X,Y,Z

    grid = vdb.FloatGrid()
    grid.copyFromArray(prepped)  # 3D float32 array → FloatGrid

    # ──  Set grid class and name ────────────────────────────────────────────────
    grid.gridClass = vdb.GridClass.FOG_VOLUME
    grid.name = "density"

    # ──  (Optional) Set a world-space transform ─────────────────────────────────
    # grid.transform = vdb.createLinearTransform(voxelSize=0.01)  # 1cm voxels

    # ──  (Optional) Attach metadata ────────────────────────────────────────────
    # grid["author"] = "me"
    # grid["source"] = "numpy"

    # ──  Write to disk ──────────────────────────────────────────────────────────
    vdb.write(f"./media/vdb_out/{output_basename}.vdb", grids=[grid])


ndarray_to_openVDB(pyramid(), "openVDB_pyramid")
