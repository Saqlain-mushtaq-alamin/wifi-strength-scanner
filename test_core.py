"""
Test script to verify core heatmap functionality
Run this to test the interpolation and heatmap generation without GUI
"""

import numpy as np
import cv2
from app.core.interpolation import idw_interpolate
from app.core.heatmap_engine import generate_heatmap
from app.core.image_blender import blend


def test_interpolation():
    """Test IDW interpolation"""
    print("Testing IDW interpolation...")

    # Create some test points (x, y, rssi)
    points = [
        (100, 100, -40),  # Strong signal
        (300, 100, -60),  # Medium signal
        (100, 300, -70),  # Weak signal
        (300, 300, -50),  # Medium-strong signal
    ]

    # Interpolate on a small grid
    width, height = 400, 400
    grid = idw_interpolate(points, width, height, power=2)

    print(f"  Grid shape: {grid.shape}")
    print(f"  Grid min: {np.nanmin(grid):.2f}")
    print(f"  Grid max: {np.nanmax(grid):.2f}")
    print("  ✓ Interpolation successful!")
    return True


def test_heatmap_generation():
    """Test heatmap generation"""
    print("\nTesting heatmap generation...")

    # Create test points
    points = [
        (100, 100, -40),
        (300, 100, -60),
        (100, 300, -70),
        (300, 300, -50),
        (200, 200, -45),  # Center point
    ]

    # Generate heatmap
    width, height = 400, 400
    heatmap = generate_heatmap(points, width, height, power=2)

    print(f"  Heatmap shape: {heatmap.shape}")
    print(f"  Heatmap dtype: {heatmap.dtype}")
    print(f"  Channels: {heatmap.shape[2] if len(heatmap.shape) > 2 else 'N/A'}")
    print("  ✓ Heatmap generation successful!")

    # Save test heatmap
    cv2.imwrite("test_heatmap.png", heatmap)
    print("  ✓ Test heatmap saved as 'test_heatmap.png'")
    return True


def test_blending():
    """Test image blending"""
    print("\nTesting image blending...")

    # Create a simple test blueprint (white with some features)
    blueprint = np.ones((400, 400, 3), dtype=np.uint8) * 255
    cv2.rectangle(blueprint, (50, 50), (350, 350), (200, 200, 200), 2)
    cv2.rectangle(blueprint, (150, 150), (250, 250), (180, 180, 180), -1)

    # Generate heatmap
    points = [
        (100, 100, -40),
        (300, 100, -60),
        (100, 300, -70),
        (300, 300, -50),
        (200, 200, -45),
    ]
    heatmap = generate_heatmap(points, 400, 400, power=2)

    # Blend
    blended = blend(blueprint, heatmap, alpha=0.6)

    print(f"  Blended shape: {blended.shape}")
    print(f"  Blended dtype: {blended.dtype}")
    print("  ✓ Blending successful!")

    # Save result
    cv2.imwrite("test_blended.png", blended)
    print("  ✓ Test blended image saved as 'test_blended.png'")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("WiFi Strength Scanner - Core Functionality Test")
    print("=" * 60)

    try:
        test_interpolation()
        test_heatmap_generation()
        test_blending()

        print("\n" + "=" * 60)
        print("✓ All tests passed successfully!")
        print("=" * 60)
        print("\nYou can now run 'python main.py' to start the GUI application.")

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    main()

