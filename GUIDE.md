# WiFi Strength Scanner - Setup & Usage Guide

## 🎯 Overview

This application helps you visualize WiFi signal strength across a physical space by:
1. Uploading a blueprint/floor plan
2. Clicking on locations to scan WiFi strength
3. Generating a color-coded heatmap showing signal coverage

## 📋 Prerequisites

- Windows 10/11 (required for WiFi scanning)
- Python 3.8 or higher
- Active WiFi connection
- A blueprint image (PNG, JPG, SVG, etc.)

## 🔧 Installation

### Step 1: Install Python

If you don't have Python installed:
1. Download from https://www.python.org/downloads/
2. Run installer and **check "Add Python to PATH"**
3. Verify installation: Open PowerShell and run `python --version`

### Step 2: Install Dependencies

Open PowerShell in the project directory and run:

```powershell
pip install -r requirements.txt
```

This installs:
- PySide6 (GUI framework)
- PySide6-Fluent-Widgets (modern UI components)
- OpenCV (image processing)
- NumPy (numerical computations)

### Step 3: Verify Installation

Test the core functionality:

```powershell
python test_core.py
```

You should see success messages and two test images generated.

## 🚀 Running the Application

Start the application:

```powershell
python main.py
```

The main window will open with three options:
- **Scan Blueprint** - Start scanning
- **Heatmap List** - View saved heatmaps (coming soon)
- **Speed Test** - Test internet speed (coming soon)

## 📖 How to Use

### Step 1: Open Scan Page

Click **"Scan Blueprint"** on the main screen.

### Step 2: Upload Blueprint

1. Click the **"Upload Blueprint"** button (bottom right)
2. Select your floor plan image
3. The image will appear in the viewer

### Step 3: Scan WiFi Points

1. **Click anywhere** on the blueprint where you want to measure WiFi
2. The app will:
   - Show a red dot at that location
   - Automatically scan WiFi strength
   - Display signal info in the status panel
3. **Repeat** this at multiple locations:
   - Corners of rooms
   - Near walls
   - Open areas
   - Problem spots
   
**Tip**: Scan at least 10-15 points for good coverage!

### Step 4: Generate Heatmap

1. After scanning enough points, click **"Generate Heatmap"**
2. The app will:
   - Process all scan data
   - Create interpolated heatmap
   - Blend it with your blueprint
   - Save the result
3. A success message shows where the file was saved

### Step 5: View Results

- The heatmap appears in the viewer
- Files are saved in a `heatmaps/` folder next to your blueprint:
  - `heatmap_YYYYMMDD_HHMMSS.png` - The visual heatmap
  - `scan_data_YYYYMMDD_HHMMSS.json` - Raw scan data

## 🎨 Understanding the Heatmap

**Color Legend:**
- 🔴 **Red** - Strong signal (-30 to -50 dBm)
- 🟡 **Yellow** - Good signal (-50 to -60 dBm)
- 🟢 **Green** - Medium signal (-60 to -70 dBm)
- 🔵 **Blue** - Weak signal (-70 to -90 dBm)
- ⚫ **Dark Blue** - Very weak/no signal (-90 to -100 dBm)

**RSSI (Signal Strength) Guide:**
- `-30 to -50 dBm` - Excellent
- `-50 to -60 dBm` - Very Good
- `-60 to -70 dBm` - Good
- `-70 to -80 dBm` - Fair
- `-80 to -90 dBm` - Weak
- Below `-90 dBm` - Very Weak

## ⚙️ Advanced Settings

### Adjust Grid Size

Use the vertical slider on the left to change grid resolution:
- **Higher values** (150-200) - Coarser grid, faster processing
- **Lower values** (50-100) - Finer grid, more detail

### Customization

Edit `config.py` to change:

```python
DEFAULT_GRID_SIZE = 100      # Grid resolution
DEFAULT_IDW_POWER = 2        # Smoothing (higher = more localized)
DEFAULT_BLEND_ALPHA = 0.6    # Transparency (0.0-1.0)
```

## 🐛 Troubleshooting

### Problem: "No WiFi data detected"

**Solutions:**
1. Make sure you're connected to WiFi
2. Run PowerShell as Administrator
3. Test manually: `netsh wlan show interfaces`
4. Check that Windows WiFi service is running

### Problem: "Import Error" or "Module not found"

**Solutions:**
1. Reinstall dependencies: `pip install -r requirements.txt`
2. Use a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python main.py
   ```

### Problem: Heatmap looks patchy or weird

**Solutions:**
1. Scan more points (aim for 15-20)
2. Distribute points evenly across the area
3. Include corner and edge points
4. Reduce the IDW power in config.py (try 1.5)

### Problem: Can't find saved heatmaps

**Solutions:**
1. Check the console output for the exact path
2. Look in the same folder as your blueprint
3. Check for a `heatmaps/` subdirectory

### Problem: Application crashes or freezes

**Solutions:**
1. Check Python version: `python --version` (must be 3.8+)
2. Update dependencies: `pip install --upgrade -r requirements.txt`
3. Check console for error messages
4. Try with a smaller blueprint image

## 📊 Best Practices

### For Best Results:

1. **Coverage**
   - Scan every room
   - Include hallways and transition areas
   - Don't skip corners

2. **Point Distribution**
   - Aim for 1 point per 10-20 square meters
   - More points in problem areas
   - Even spacing produces better interpolation

3. **Consistency**
   - Scan at the same height (e.g., desk level)
   - Keep device in same orientation
   - Don't move router during scanning

4. **Blueprint Quality**
   - Use high-resolution images
   - Clear, simple floor plans work best
   - Avoid overly detailed blueprints

## 💡 Tips & Tricks

1. **Multiple Scans**: Take 2-3 scans at the same location and average them for accuracy

2. **Time of Day**: WiFi congestion varies - scan at peak usage times

3. **Comparison**: Save multiple heatmaps to compare before/after router changes

4. **Documentation**: The JSON data files let you re-process scans with different settings

5. **Export**: Use the PNG heatmaps in reports or presentations

## 📁 Output Files

Each scan session creates two files:

**1. Heatmap Image** (`heatmap_YYYYMMDD_HHMMSS.png`)
- Visual representation
- Blueprint with color overlay
- Ready to share/print

**2. Scan Data** (`scan_data_YYYYMMDD_HHMMSS.json`)
```json
{
  "blueprint": "C:/path/to/blueprint.png",
  "timestamp": "20251209_143022",
  "points": [
    [245.5, 180.2, -45],
    [450.0, 200.5, -52]
  ],
  "grid_size": 100
}
```

## 🔄 Workflow Example

1. Measure your space and create/obtain a floor plan
2. Upload the floor plan to WSS
3. Walk around with your laptop
4. Click and scan at each location
5. Generate heatmap
6. Identify weak spots
7. Reposition router or add extenders
8. Scan again to verify improvements

## 📞 Support

For issues or questions:
- Check this guide first
- Review error messages in the console
- Check GitHub issues (if applicable)

## 🎓 Understanding the Technology

**IDW (Inverse Distance Weighting)**
- Estimates values between points
- Closer points have more influence
- Power parameter controls smoothness

**RSSI (Received Signal Strength Indicator)**
- Measured in dBm (decibel-milliwatts)
- Negative numbers (lower = weaker)
- Affected by walls, distance, interference

**Heatmap Blending**
- Alpha compositing
- Preserves blueprint features
- Adjustable transparency

---

**Version**: 1.0.0  
**Last Updated**: December 2024  
**Platform**: Windows 10/11

