import bpy
import logging
import subprocess
import sys
import numpy as np
from pathlib import Path
import openvdb as vdb

repo_path = Path(bpy.data.filepath).parent.parent
print("hello from openVDB_builder.py")


# from util import display_message
def display_message(message, title="Notification", icon="INFO"):
    """Show a popup message in Blender."""

    def draw(self, context):
        self.layout.label(text=message)

    def show_popup():
        bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)
        return None  # Stops timer

    bpy.app.timers.register(show_popup)


# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_modules_path():
    """Return a writable directory for installing Python packages."""
    return bpy.utils.user_resource("SCRIPTS", path="modules", create=True)


def install_package(package, modules_path):
    """Install a single package using Blender's Python."""
    try:
        logger.info(f"Installing {package}...")
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "--target",
                modules_path,
                package,
            ]
        )
        logger.info(f"{package} installed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install {package}. Error: {e}")
        display_message(
            f"Failed to install {package}. Check console for details.", icon="ERROR"
        )


install_package("nibabel>=5.4.2", get_modules_path())
import nibabel as nib

print("nibable: ", nib)


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


def pyramid(size=64000) -> np.ndarray:
    pyramid, built = _build_pyramid()
    assert built, "Pyramid should build successfully"

    # perhaps this pattern isn't the best?
    return pyramid


# claude copypasta:
grid = vdb.FloatGrid()
grid.copyFromArray(pyramid())  # 3D float32 array → FloatGrid

# ──  Set grid class and name ────────────────────────────────────────────────
grid.gridClass = vdb.GridClass.FOG_VOLUME
grid.name = "density"

# ──  (Optional) Set a world-space transform ─────────────────────────────────
grid.transform = vdb.createLinearTransform(voxelSize=0.01)  # 1cm voxels

# ──  (Optional) Attach metadata ────────────────────────────────────────────
grid["author"] = "me"
grid["source"] = "numpy"

# ──  Write to disk ──────────────────────────────────────────────────────────
vdb.write("./media/vdb_out/openVDB_pyramid.vdb", grids=[grid])
