# ===== File: app/core/interpolation.py =====
"""
Simple IDW interpolation implementation.
This file exposes a single function:

    idw_interpolate(points, width, height, power=2, eps=1e-6)

- points: list of (x, y, rssi) where x in [0..width-1], y in [0..height-1]
- returns: 2D numpy array shaped (height, width) with interpolated RSSI floats

The implementation is straightforward and reasonably vectorized with NumPy.
"""

import numpy as np


def idw_interpolate(points, width, height, power=2, eps=1e-6):
    """Interpolate scattered (x,y,rssi) points onto a regular grid using IDW.

    Args:
        points (list of tuples): [(x, y, rssi), ...]
        width (int): output grid width (pixels)
        height (int): output grid height (pixels)
        power (float): IDW power parameter (default 2)
        eps (float): small value to avoid division by zero

    Returns:
        np.ndarray: shape (height, width), dtype float32
    """
    if len(points) == 0:
        # nothing to interpolate — return NaNs
        return np.full((height, width), np.nan, dtype=np.float32)

    # Convert to numpy arrays for vectorized math
    pts = np.array(points, dtype=np.float32)
    xs = pts[:, 0]
    ys = pts[:, 1]
    vals = pts[:, 2]

    # Create grid coordinates (note: Y first for image coordinates)
    grid_x = np.arange(width, dtype=np.float32)
    grid_y = np.arange(height, dtype=np.float32)
    gx, gy = np.meshgrid(grid_x, grid_y)  # shape (height, width)

    # Initialize numerator and denominator
    numerator = np.zeros((height, width), dtype=np.float64)
    denominator = np.zeros((height, width), dtype=np.float64)

    # For each sample point, accumulate weighted contributions
    for xi, yi, vi in zip(xs, ys, vals):
        # compute squared distance to avoid extra sqrt cost
        dx = gx - xi
        dy = gy - yi
        dist_sq = dx * dx + dy * dy

        # If a grid cell exactly matches a sample point, set value directly
        exact_mask = dist_sq == 0
        if np.any(exact_mask):
            numerator[exact_mask] = vi
            denominator[exact_mask] = 1.0
            # mask out these positions from further accumulation
            # set dist_sq to eps so weights will be very large but won't divide by 0
            dist_sq[exact_mask] = eps

        # weight = 1 / (distance^power) -> using dist_sq to compute distance^power
        # distance = sqrt(dist_sq) -> distance^power = dist_sq^(power/2)
        weights = 1.0 / (np.power(dist_sq, power / 2.0) + eps)

        numerator += weights * vi
        denominator += weights

    # avoid division by zero
    mask_zero = denominator == 0
    denominator[mask_zero] = np.nan

    grid = numerator / denominator
    # convert to float32
    return grid.astype(np.float32)
