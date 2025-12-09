# 📡 WiFi Strength Scanner (WSS)

A comprehensive tool for scanning and visualizing WiFi signal strength with interactive heatmap generation.

## 🎯 Features

- **Blueprint Upload**: Load floor plans or maps as blueprints
- **Interactive Scanning**: Click on the blueprint to scan WiFi strength at specific locations
- **Automatic WiFi Detection**: Uses Windows `netsh` to automatically detect current WiFi signal strength
- **Heatmap Generation**: Creates beautiful heatmaps using IDW (Inverse Distance Weighting) interpolation
- **Image Blending**: Overlays heatmaps on original blueprints for clear visualization
- **Data Export**: Saves both the generated heatmap images and raw scan data in JSON format
- **Modern UI**: Sleek sci-fi themed interface built with PySide6 and Fluent Widgets

## 🚀 Quick Start

### Installation

1. **Install Python 3.8+** (if not already installed)

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

### Usage

1. **Click "Scan Blueprint"** to open the scanning interface

2. **Upload a Blueprint**: 
   - Click the "Upload Blueprint" button
   - Select your floor plan image (PNG, JPG, SVG, etc.)

3. **Scan WiFi Points**:
   - Click anywhere on the blueprint image
   - The app will automatically scan WiFi strength at that location
   - Red dots will appear showing where you've scanned
   - View scan details in the status panel

4. **Generate Heatmap**:
   - After scanning multiple points (recommended: 10+ points for good coverage)
   - Click "Generate Heatmap"
   - The heatmap will be saved to a `heatmaps/` folder next to your blueprint
   - The result will be displayed in the viewer

5. **Review Results**:
   - Heatmap images are saved with timestamps
   - Scan data is saved in JSON format for later analysis
   - Red areas indicate strong signal, blue areas indicate weak signal

## 📁 Project Structure

```
wifi-strength-scanner/
├── app/
│   ├── resources/              # Icons and default images
│   │   ├── blueprint/
│   │   └── icon/
│   ├── ui/                     # UI components
│   │   ├── main_windw.py       # Main window with landing page
│   │   ├── scan_page.py        # Scanning interface
│   │   ├── heatmap_list.py     # Heatmap history viewer
│   │   ├── speedTest.py        # Speed test page
│   │   └── widgets/
│   │       └── blueprint_viewer.py  # Interactive image viewer
│   └── core/                   # Backend logic
│       ├── scanner.py          # WiFi scanner (netsh wrapper)
│       ├── heatmap_engine.py   # Heatmap generation
│       ├── interpolation.py    # IDW algorithm
│       ├── image_blender.py    # Image blending
│       └── data_store.py       # Data persistence
├── build/
│   └── pyinstaller.spec        # Build configuration
├── main.py                     # Application entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md
└── LICENSE
```

## 🔧 How It Works

### Data Flow

1. **Click on Blueprint** → Captures pixel coordinates (x, y)
2. **WiFi Scan** → Runs `netsh wlan show interfaces` to get RSSI (signal strength in dBm)
3. **Store Data** → Saves point as tuple: `(x, y, rssi)`
4. **Generate Heatmap** → 
   - Uses IDW interpolation to create a continuous heat field from discrete points
   - Applies color mapping (red = strong, blue = weak)
   - Blends heatmap with original blueprint
5. **Save & Display** → Outputs final image and JSON data

### Core Algorithms

- **IDW Interpolation**: Inverse Distance Weighting estimates signal strength at unsampled locations
- **Color Mapping**: OpenCV's JET colormap converts signal values to colors
- **Alpha Blending**: Linear blending overlays the heatmap on the blueprint with transparency

## 🎨 Customization

Edit `config.py` to customize:

- `DEFAULT_GRID_SIZE`: Grid resolution (default: 100 pixels)
- `DEFAULT_IDW_POWER`: IDW smoothness (default: 2)
- `DEFAULT_BLEND_ALPHA`: Heatmap transparency (default: 0.6)
- Color schemes and other settings

## 📊 Data Format

Scan data is saved as JSON:

```json
{
  "blueprint": "path/to/blueprint.png",
  "timestamp": "20251209_143022",
  "points": [
    [245.5, 180.2, -45],
    [450.0, 200.5, -52],
    ...
  ],
  "grid_size": 100
}
```

Where each point is `[x_pixels, y_pixels, rssi_dBm]`

## ⚙️ Requirements

- **Windows OS** (for `netsh` WiFi scanning)
- **Python 3.8+**
- **WiFi Connection** (active connection required for scanning)
- See `requirements.txt` for Python package dependencies

## 🐛 Troubleshooting

**No WiFi data detected?**
- Ensure you're connected to a WiFi network
- Run the app with administrator privileges
- Check that `netsh wlan show interfaces` works in your terminal

**Heatmap looks weird?**
- Scan more points (minimum 10-15 recommended)
- Distribute points across the entire area
- Adjust the grid size slider for better granularity

**Can't see the generated heatmap?**
- Check the `heatmaps/` folder next to your blueprint
- Verify the console output for the save path

## 📝 License

See LICENSE file for details.

## 👥 Credits

Developed by: Saqlain • Farhan • Tamim • Govt
Organization: Quantum Innovar

---

**Note**: This is a Windows-specific application due to its reliance on the `netsh` command for WiFi scanning.
