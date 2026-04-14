import numpy as np


# claude wrote this:
def dither(arr: np.ndarray, num_levels: int) -> np.ndarray:
    """
    Dither a numpy array to a specified number of quantization levels
    using Floyd-Steinberg error diffusion.

    Parameters
    ----------
    arr : np.ndarray
        Input array (2D or 3D) with values in any range.
    num_levels : int
        Number of discrete output levels (e.g., 2 for black/white, 256 for 8-bit).

    Returns
    -------
    np.ndarray
        Dithered array with values quantized to `num_levels` levels,
        scaled back to the original input range.
    """
    if num_levels < 2:
        raise ValueError("num_levels must be at least 2")

    if arr.ndim == 3:
        return np.stack(
            [dither(arr[i], num_levels) for i in range(arr.shape[0])], axis=0
        )
    elif arr.ndim != 2:
        raise ValueError(f"Expected a 2D or 3D array, got shape {arr.shape}")

    # Normalize to [0, 1]
    arr_min, arr_max = arr.min(), arr.max()
    if arr_max == arr_min:
        return arr.copy()

    normalized = (arr.astype(float) - arr_min) / (arr_max - arr_min)
    output = normalized.copy()

    levels = np.linspace(0, 1, num_levels)

    def quantize(value: float) -> float:
        idx = np.argmin(np.abs(levels - value))
        return levels[idx]

    rows, cols = output.shape

    for r in range(rows):
        for c in range(cols):
            old_val = output[r, c]
            new_val = quantize(old_val)
            output[r, c] = new_val
            error = old_val - new_val

            if c + 1 < cols:
                output[r, c + 1] += error * 7 / 16
            if r + 1 < rows:
                if c - 1 >= 0:
                    output[r + 1, c - 1] += error * 3 / 16
                output[r + 1, c] += error * 5 / 16
                if c + 1 < cols:
                    output[r + 1, c + 1] += error * 1 / 16

    return output * (arr_max - arr_min) + arr_min
