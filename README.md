# 📁 WiFi Strength Scanner

A comprehensive tool for scanning and visualizing WiFi signal strength with heatmap generation.

## Project Structure

```
wifi-strength-scanner/
├── app/
│   │
│   ├── resources/              # Icons, QRC files, default images
│   ├── ui/                     # UI-related files
│   │   ├── main_window.py
│   │   ├── upload_page.py
│   │   ├── scan_page.py
│   │   ├── heatmap_page.py
│   │   └── widgets/
│   │       ├── blueprint_viewer.py
│   │       └── point_marker.py
│   ├── core/                   # Backend logic
│   │   ├── scanner.py          # Netsh parser
│   │   ├── heatmap_engine.py
│   │   ├── interpolation.py    # IDW algorithm
│   │   ├── data_store.py       # JSON/SQLite wrapper
│   │   ├── project_manager.py
│   │   └── image_blender.py    # Blend heatmap + blueprint
│   └── utils/
│       ├── file_dialogs.py
│       ├── paths.py
│       └── logger.py
├── build/
│   ├── installer/              # NSIS or Inno Setup scripts
│   ├── dist/                   # Final .exe output
│   └── pyinstaller.spec
├── main.py
├── config.py
├── requirements.txt
├── README.md
└── LICENSE
```