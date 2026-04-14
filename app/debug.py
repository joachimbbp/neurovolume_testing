import numpy as np
from PIL import Image


def save_slice_as_png(
    arr: np.ndarray,
    index: int,
    filepath: str,
    axis: int = 0,
) -> None:
    """
    Save a 2D slice from a 3D numpy array as a PNG file.

    Parameters
    ----------
    arr      : 3D numpy array (e.g. shape [D, H, W] or [H, W, D])
    index    : Which slice along `axis` to extract
    filepath : Output path, e.g. "slice.png"
    axis     : Axis to slice along (0, 1, or 2). Default is 0.
    """
    if arr.ndim != 3:
        raise ValueError(f"Expected a 3D array, got shape {arr.shape}")
    if not (0 <= axis <= 2):
        raise ValueError("axis must be 0, 1, or 2")

    slice_2d = np.take(arr, index, axis=axis).astype(float)

    # Normalize to [0, 255]
    s_min, s_max = slice_2d.min(), slice_2d.max()
    if s_max > s_min:
        slice_2d = (slice_2d - s_min) / (s_max - s_min) * 255
    else:
        slice_2d = np.zeros_like(slice_2d)

    Image.fromarray(slice_2d.astype(np.uint8)).save(filepath)
    print(f"Saved slice {index} (axis={axis}) → {filepath}")
