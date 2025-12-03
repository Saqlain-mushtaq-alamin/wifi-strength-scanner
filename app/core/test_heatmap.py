# ===== File: test_heatmap.py =====
"""
Tiny test script to validate the starter module locally.

Run: python test_heatmap.py

It will write two files:
 - debug_heatmap.png   (colored heatmap alone)
 - debug_blended.png   (heatmap blended on white "blueprint")

Make sure you have: numpy, opencv-python installed.
"""

import cv2
import numpy as np
from app.core.heatmap_engine import generate_heatmap
from app.core.image_blender import blend


def main():
    width, height = 1000, 700

    # Fake blueprint: plain white background with a simple rectangle to mimic a floor plan
    blueprint = np.ones((height, width, 3), dtype=np.uint8) * 255
    cv2.rectangle(blueprint, (50, 50), (950, 650), (220, 220, 220), thickness=-1)

    # Fake sample measurement points: (x, y, rssi)
    points = [
        (150, 150, -45),
        (800, 120, -60),
        (500, 350, -50),
        (250, 500, -75),
        (850, 520, -80),
    ]

    heatmap = generate_heatmap(points, width, height)
    blended = blend(blueprint, heatmap, alpha=0.55)

    cv2.imwrite("debug_heatmap.png", heatmap)
    cv2.imwrite("debug_blended.png", blended)
    print("Wrote debug_heatmap.png and debug_blended.png")


if __name__ == "__main__":
    main()
