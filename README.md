# 📡 WiFi Strength Scanner (WSS)

A comprehensive tool for scanning and visualizing WiFi signal strength with interactive heatmap generation.

## 🎯 Features

### Core Functionality
- **Blueprint Upload**: Load floor plans, maps, or any image as a blueprint for WiFi analysis
  - Supports multiple formats: PNG, JPG, JPEG, SVG, BMP, GIF, WebP
  - Auto-scaling to fit viewer while maintaining aspect ratio
  - Pixel-perfect coordinate mapping for accurate measurements

- **Interactive WiFi Scanning**: Click anywhere on the blueprint to scan WiFi strength
  - Automatic WiFi detection using Windows `netsh` command
  - Manual RSSI input option for custom measurements
  - Visual markers (red circles) show scanned locations
  - Real-time RSSI values displayed next to each marker

- **✨ NEW: Edit Marker Capability**: Click existing markers to update their RSSI values
  - **Rescan Option**: Take a new automatic WiFi measurement at the same location
  - **Manual Update**: Edit RSSI values manually for corrections or custom data
  - Smart click detection (10-pixel radius) to distinguish between adding and editing
  - Live data synchronization - changes immediately reflected in heatmap generation
  - Visual feedback showing current RSSI values during editing

### Heatmap & Visualization
- **Advanced Heatmap Generation**: Creates beautiful, accurate WiFi coverage heatmaps
  - IDW (Inverse Distance Weighting) interpolation algorithm
  - Smooth color gradients from red (strong) to blue (weak signal)
  - Customizable interpolation parameters
  - Real-time preview in the viewer

- **Image Blending**: Sophisticated overlay of heatmaps on original blueprints
  - Adjustable transparency for optimal visibility
  - High-quality alpha blending preserves blueprint details
  - Clear visualization of WiFi coverage patterns

### Data Management
- **Scan History**: Browse and manage all previous WiFi scans
  - Timestamped records of all heatmap generations
  - Quick access to historical data and images
  - JSON export of raw scan data for external analysis

- **Data Persistence**: Automatic saving of scan data and results
  - Heatmap images saved with timestamps (PNG format)
  - Scan point data exported as JSON files
  - Blueprint-organized folder structure for easy management
  - Format: `[(x, y, rssi), ...]` for easy integration

### User Interface
- **Modern Dark Theme UI**: Sleek, sci-fi inspired interface
  - Built with PySide6 and QFluentWidgets
  - Smooth animations and hover effects
  - Glassy, translucent panels with gradient accents
  - Responsive layout that adapts to window size

- **Real-time Status Panel**: Live feedback during scanning
  - Displays current point coordinates
  - Shows WiFi details (SSID, BSSID, Signal %, RSSI, Channel, Radio, Band)
  - Running total of collected scan points
  - Color-coded success/error messages

- **Speed Test Integration**: Built-in internet speed testing (separate feature)
  - Download and upload speed measurements
  - Network performance monitoring

### Technical Features
- **Pixel Coordinate System**: All measurements use precise image pixel coordinates
  - No grid-based limitations - place markers anywhere
  - Sub-pixel precision for accurate positioning
  - Coordinate system independent of widget size

- **Smart Marker Management**: Intelligent handling of scan point markers
  - Add new markers by clicking empty space
  - Edit existing markers by clicking on them
  - Visual RSSI display on each marker
  - Automatic synchronization between markers and data array

- **Flexible Input Methods**: Multiple ways to input WiFi strength data
  - Auto-scan: Automatic detection of current WiFi connection
  - Manual input: Enter RSSI values manually (-100 to 0 dBm range)
  - Edit mode: Update existing measurements without re-adding

- **Error Handling & Validation**: Robust error checking throughout
  - WiFi connection validation
  - Input range validation for RSSI values
  - Image loading verification
  - User-friendly error messages with InfoBar notifications

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
   - Choose your input method:
     - **Auto-scan WiFi**: Automatically detects current WiFi signal strength
     - **Manual input**: Enter RSSI value manually (e.g., -45 dBm)
   - Red circular markers appear showing where you've scanned
   - RSSI values are displayed next to each marker
   - View detailed scan information in the status panel

## 🆕 Recent Updates

### December 9, 2025 - Edit Marker Feature
**NEW!** You can now edit existing WiFi scan points by clicking on them:
- ✨ Click on any marker to edit its RSSI value
- 🔄 Rescan WiFi at the same location to update measurements
- ✏️ Manually update RSSI values for corrections
- 📊 Real-time synchronization with heatmap data
- 🎯 Smart click detection (10px radius) distinguishes add vs edit

This makes it easy to:
- Correct measurements without deleting and re-adding
- Update signal strength after network changes
- Fine-tune data before generating heatmaps
- Track signal changes at specific locations over time

See `EDIT_MARKER_FEATURE.md` and `QUICK_START_EDIT.md` for detailed documentation.

4. **✨ Edit Existing Markers** (NEW):
   - Click directly on any existing marker (red circle)
   - Edit dialog opens showing current RSSI value
   - Choose your update method:
     - **Rescan WiFi**: Take a new measurement at the same location
     - **Manual input**: Enter a new RSSI value (pre-filled with current value)
   - Click "Update" to save changes or "Cancel" to keep original
   - Marker updates immediately on the blueprint
   - Changes are automatically synced to the scan data

5. **Generate Heatmap**:
   - After scanning multiple points (recommended: 10+ points for good coverage)
   - Click "Generate Heatmap"
   - The heatmap will be saved to a `heatmaps/` folder next to your blueprint
   - The result will be displayed in the viewer

6. **Review Results**:
   - Heatmap images are saved with timestamps
   - Scan data is saved in JSON format for later analysis
   - Red areas indicate strong signal, blue areas indicate weak signal
   - Access history through the "History" tab to view previous scans

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
   - Detects if clicking on existing marker or empty space
   - Existing marker: Opens edit dialog
   - Empty space: Opens add dialog
2. **WiFi Scan** → Runs `netsh wlan show interfaces` to get RSSI (signal strength in dBm)
   - Or manual input option for custom values
3. **Store/Update Data** → Saves or updates point as tuple: `(x, y, rssi)`
   - New points: Appended to scan_points array
   - Edited points: Updates existing entry in array
4. **Generate Heatmap** → 
   - Uses IDW interpolation to create a continuous heat field from discrete points
   - Applies color mapping (red = strong, blue = weak)
   - Blends heatmap with original blueprint
5. **Save & Display** → Outputs final image and JSON data
   - Heatmap PNG with timestamp
   - JSON file with all scan point coordinates and RSSI values

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

**Dialog doesn't appear when clicking on the blueprint?**
- Make sure you've uploaded a blueprint image first
- Try clicking slightly away from existing markers if you want to add a new point
- If editing, click directly on the marker's center (within 10 pixels)

**Can't edit an existing marker?**
- Click directly on the red circular marker (not next to it)
- The marker's RSSI value should be visible - click near that area
- A 10-pixel click radius is used for detection

**Marker shows wrong RSSI after editing?**
- Check the status panel to verify the update was successful
- The marker should update immediately after clicking "Update"
- Console logs will show the updated value for debugging

## 📝 License

See LICENSE file for details.

## 👥 Credits

Developed by: Saqlain • Farhan • Tamim • Govt
Organization: Quantum Innovar

---

**Note**: This is a Windows-specific application due to its reliance on the `netsh` command for WiFi scanning.
