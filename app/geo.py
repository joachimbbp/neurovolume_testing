# INSTRUCTIONS: must be run from project root, NOT ./tests
import numpy as np
from urllib.request import urlretrieve
import os
from util import env_field as e
import neurovolume as nv  # will give an error before you run the makefile


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


# TODO: rewrite this with the new functionality
def pyramid(size=64000):
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
    output_dir = e("vdb_out")

    os.makedirs(output_dir, exist_ok=True)
    nv.ndarray_to_vdb(
        prepped_pyramid,
        "pyramid_offset",
        output_dir=output_dir,
        transform=rotated,
    )
    print("pyramids saved")
