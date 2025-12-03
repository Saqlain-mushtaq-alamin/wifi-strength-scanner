📁 🔥 Perfect Repo Structure 
# WiFi Strength Scanner

wifi-strength-scanner/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── resources/           # icons, qrc, default images
│   ├── ui/                  # all UI-related files
│   │   ├── main_window.py
│   │   ├── upload_page.py
│   │   ├── scan_page.py
│   │   ├── heatmap_page.py
│   │   └── widgets/
│   │       ├── blueprint_viewer.py
│   │       └── point_marker.py
│   │
│   ├── core/                # backend logic
│   │   ├── scanner.py       # netsh parser
│   │   ├── heatmap_engine.py
│   │   ├── interpolation.py # IDW
│   │   ├── data_store.py    # JSON / sqlite wrapper
│   │   ├── project_manager.py
│   │   └── image_blender.py # blend heatmap + blueprint
│   │
│   └── utils/
│       ├── file_dialogs.py
│       ├── paths.py
│       └── logger.py
│
├── build/
│   ├── installer/           # NSIS or Inno Setup scripts
│   ├── dist/                # final .exe goes here
│   └── pyinstaller.spec
│
├── requirements.txt
├── README.md
└── LICENSE (optional)
