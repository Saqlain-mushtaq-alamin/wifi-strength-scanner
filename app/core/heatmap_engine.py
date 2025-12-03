# ===== File: app/core/heatmap_engine.py =====
"""
Heatmap generation pipeline.
Exposes:

    generate_heatmap(points, width, height, colormap=cv2.COLORMAP_JET)

- points: list of (x,y,rssi)
- width, height: output image size
- returns: BGR image (uint8) suitable for OpenCV display / saving

This module depends on interpolation.idw_interpolate
"""

import numpy as np
import cv2
from .interpolation import idw_interpolate


def apply_colormap_from_rssi(rssi_grid, vmin=None, vmax=None, colormap=cv2.COLORMAP_JET):
    """Turn a float RSSI grid into a BGR color image using OpenCV colormap.

    - rssi_grid may contain NaNs; they will be normalized to the minimum value.
    - vmin / vmax: if not provided, computed from the data (ignoring NaNs)
    """
    # Convert to float32 and handle NaNs
    arr = np.array(rssi_grid, dtype=np.float32)
    finite_mask = np.isfinite(arr)

    if not np.any(finite_mask):
        # nothing to map – return a transparent-like black image
        h, w = arr.shape
        return np.zeros((h, w, 3), dtype=np.uint8)

    if vmin is None:
        vmin = float(np.nanmin(arr))
    if vmax is None:
        vmax = float(np.nanmax(arr))
    if vmin == vmax:
        vmax = vmin + 1.0

    # Normalize to 0..255
    norm = (arr - vmin) / (vmax - vmin)
    norm = np.clip(norm, 0.0, 1.0)
    norm_8u = (norm * 255).astype(np.uint8)

    # Apply colormap
    colored = cv2.applyColorMap(norm_8u, colormap)  # returns BGR

    # Optional: set fully-NaN pixels to transparent/black — here we paint them black
    nan_mask = ~finite_mask
    if np.any(nan_mask):
        colored[nan_mask] = (0, 0, 0)

    return colored


def generate_heatmap(points, width, height, power=2, colormap=cv2.COLORMAP_JET):
    """Full pipeline: points -> interpolated RSSI grid -> colored heatmap image

    Returns a BGR uint8 image (height, width, 3).
    """
    rssi_grid = idw_interpolate(points, width, height, power=power)
    # Choose vmin/vmax based on typical Wi-Fi dBm range or data-driven
    # Use data-driven here but clamp to common Wi-Fi range for stability
    finite = rssi_grid[np.isfinite(rssi_grid)]
    if finite.size == 0:
        vmin, vmax = -100.0, -30.0
    else:
        vmin = float(np.nanmin(rssi_grid))
        vmax = float(np.nanmax(rssi_grid))
        # clamp a bit to avoid tiny ranges
        vmin = max(vmin, -100.0)
        vmax = min(vmax, -30.0)
        if vmin >= vmax:
            vmin, vmax = -100.0, -30.0

    colored = apply_colormap_from_rssi(rssi_grid, vmin=vmin, vmax=vmax, colormap=colormap)
    return colored