# ===== File: app/core/image_blender.py =====
"""
Simple blender that overlays heatmap on top of blueprint image.

Functions:
    blend(blueprint_bgr, heatmap_bgr, alpha=0.5)

- blueprint_bgr: BGR uint8 image (height, width, 3)
- heatmap_bgr: BGR uint8 image same shape as blueprint
- alpha: heatmap strength in [0..1]

Returns blended BGR uint8 image.
"""

import numpy as np
import cv2


def blend(blueprint_bgr, heatmap_bgr, alpha=0.5):
    """Blend two BGR images using simple linear blend.

    If sizes differ, heatmap will be resized to match blueprint.
    """
    if blueprint_bgr is None:
        raise ValueError("blueprint image is None")
    if heatmap_bgr is None:
        raise ValueError("heatmap image is None")

    bh, bw = blueprint_bgr.shape[:2]
    hh, hw = heatmap_bgr.shape[:2]

    if (bh, bw) != (hh, hw):
        heatmap_resized = cv2.resize(heatmap_bgr, (bw, bh), interpolation=cv2.INTER_LINEAR)
    else:
        heatmap_resized = heatmap_bgr

    # convert to float for blending
    b_float = blueprint_bgr.astype(np.float32)
    h_float = heatmap_resized.astype(np.float32)

    blended = (alpha * h_float) + ((1.0 - alpha) * b_float)
    blended = np.clip(blended, 0, 255).astype(np.uint8)
    return blended
