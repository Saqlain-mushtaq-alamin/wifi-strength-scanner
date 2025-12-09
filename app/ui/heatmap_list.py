from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QAbstractItemView,
    QLabel, QFrame, QSizePolicy, QStackedWidget, QApplication, QPushButton
)
from pathlib import Path
import json
from datetime import datetime

class HeatmapList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.heatmap_data = {}  # Store heatmap metadata
        self.HeatmapListPage()
        self.apply_styles()
        self.load_saved_heatmaps()  # Load existing heatmaps

    def HeatmapListPage(self):
        root = QVBoxLayout()
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        # Header
        header = QFrame()
        header.setMinimumHeight(64)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(12, 12, 12, 12)
        header_layout.setSpacing(8)

        title = QLabel("Wi‑Fi Heatmaps")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
     
         # Back button on the left
        self.back_btn = QPushButton("Back", header)
        self.back_btn.setObjectName("backBtn")
        self.back_btn.setFixedHeight(28)
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.setStyleSheet("""
        #backBtn {
            background: transparent;
            border: none;
            border-right: 1px solid rgba(120, 200, 255, 180);
            color: #d7eaff;
            padding: 0 10px;  /* added padding */
        }
        #backBtn:hover {
            background: rgba(30, 36, 42, 120);  /* hover effect */
            border-right: 1px solid rgba(120, 200, 255, 220);
        }
        #backBtn:pressed {
            background: rgba(21, 212, 253, 80); /* pressed effect */
            border-right: 1px solid rgba(120, 200, 255, 255);
        }
        """)

        def _go_back():
            try:
                # Resolve MainWindow class (prefer main_windw.py, fallback to main_window.py)
                from importlib import import_module
                MainWindow = None
                for mod in ("app.ui.main_windw", "app.ui.main_window"):
                    try:
                        MainWindow = getattr(import_module(mod), "MainWindow")
                        break
                    except Exception:
                        continue

                top = self.window()

                # If embedded inside MainWindow, rebuild its landing view in-place
                if MainWindow is not None and isinstance(top, MainWindow):
                    try:
                        # Recreate the main landing UI (title, viewer, buttons)
                        rebuild = getattr(top, "_setup_ui", None)
                        if callable(rebuild):
                            rebuild()
                            return
                    except Exception:
                        pass

                    # Fallback: try to locate a QStackedWidget and go to index 0
                    parent = self.parentWidget()
                    while parent is not None and not isinstance(parent, QStackedWidget):
                        parent = parent.parentWidget()
                    if isinstance(parent, QStackedWidget):
                        parent.setCurrentIndex(0)
                        return

                # Otherwise, show or create the main window and close this standalone window
                app = QApplication.instance()
                mw = None
                if isinstance(app, QApplication) and MainWindow is not None:
                    mw = next((w for w in app.topLevelWidgets() if isinstance(w, MainWindow)), None)
                    if mw is None:
                        mw = MainWindow()
                if mw is not None:
                    mw.show()
                    try:
                        mw.raise_()
                        mw.activateWindow()
                    except Exception:
                        pass
                if top is not mw and hasattr(top, "close"):
                    top.close()
            except Exception as e:
                print(f"Back navigation failed: {e}")

        self.back_btn.clicked.connect(_go_back)
        header_layout.addWidget(self.back_btn, 0, Qt.AlignmentFlag.AlignLeft)
        header_layout.addStretch(1)


        header_layout.addWidget(title)
 
        root.addWidget(header)

        # Main content split: left list (≈30%), right blueprint + footer (≈70%)
        content = QHBoxLayout()
        content.setSpacing(12)

        # Left bar: heatmap list (constrained width to approximate 30%)
        left = QFrame()
        left.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        left.setMinimumWidth(280)  # tweak as needed
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(12, 12, 12, 12)
        left_layout.setSpacing(8)

        left_header = QLabel("Heatmap Sets")
        left_header.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))

        self.heatmap_list_widget = QListWidget()
        self.heatmap_list_widget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.heatmap_list_widget.itemClicked.connect(self.on_heatmap_selected)
        self.heatmap_list_widget.setObjectName("heatmapList")

        left_layout.addWidget(left_header)
        left_layout.addWidget(self.heatmap_list_widget)

        # Right bar: blueprint + footer
        right = QFrame()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(12, 12, 12, 12)
        right_layout.setSpacing(8)

        blueprint_header = QLabel("Blueprint Preview")
        blueprint_header.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))

        self.blueprint_view = QLabel("No blueprint loaded")
        self.blueprint_view.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.blueprint_view.setObjectName("blueprintView")
        self.blueprint_view.setMinimumHeight(240)
        footer = QLabel("Tip: Select a heatmap to preview its blueprint and coverage.")
        footer.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        footer.setObjectName("footer")
        footer.setMinimumHeight(60)

        right_layout.addWidget(blueprint_header)
        right_layout.addWidget(self.blueprint_view, 1)
        right_layout.addWidget(footer)

        content.addWidget(left, 7)   # ~70%
        content.addWidget(right, 3)  # ~30%
        root.addLayout(content)

        self.setLayout(root)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background: #0f1318;
                color: #e6edf3;
            }
            QFrame {
                background: #151a21;
                border: 1px solid #222935;
                border-radius: 10px;
            }
            QLabel {
                color: #e6edf3;
            }
            QListWidget#heatmapList {
                background: #0f1318;
                border: 1px solid #222935;
                border-radius: 8px;
                padding: 6px;
            }
            QListWidget#heatmapList::item {
                padding: 8px;
                margin: 2px 0;
            }
            QListWidget#heatmapList::item:selected {
                background: #2a3442;
                border-radius: 6px;
            }
            QLabel#blueprintView {
                background: #0f1318;
                border: 1px dashed #334052;
                border-radius: 8px;
            }
            QLabel#footer {
                color: #9fb0c0;
                font-size: 11px;
            }
        """)

    def load_saved_heatmaps(self):
        """Scan the Saved_Scans folder and populate the list with heatmaps."""
        from app.core.save_locations import SaveLocations

        self.heatmap_list_widget.clear()
        self.heatmap_data.clear()

        # Try to migrate old scans first
        try:
            SaveLocations.migrate_old_scans()
        except Exception as e:
            print(f"Migration warning: {e}")

        # Get all scan folders
        scan_folders = SaveLocations.list_all_scans()

        if not scan_folders:
            self.heatmap_list_widget.addItem("No saved heatmaps found")
            self.blueprint_view.setText(
                "No scans yet\n\n"
                "Generate a heatmap from the Scan tab\n"
                "and it will appear here"
            )
            return

        # Process each scan folder
        for scan_folder in scan_folders:
            timestamp_str = scan_folder.name

            # Find heatmap and data files
            heatmap_files = list(scan_folder.glob("heatmap_*.png"))
            data_files = list(scan_folder.glob("scan_data_*.json"))

            if not heatmap_files:
                continue

            heatmap_path = heatmap_files[0]
            data_path = data_files[0] if data_files else None

            # Parse metadata
            metadata = self._parse_heatmap_metadata(data_path, timestamp_str)

            # Store in dictionary
            scan_id = f"scan_{timestamp_str}"
            self.heatmap_data[scan_id] = {
                "heatmap_path": heatmap_path,
                "data_path": data_path,
                "folder_path": scan_folder,
                **metadata
            }

            # Add to list widget
            display_text = f"{metadata['formatted_date']} ({metadata['num_points']} points)"
            self.heatmap_list_widget.addItem(display_text)

        # Update footer
        footer = self.findChild(QLabel, "footer")
        if footer:
            footer.setText(
                f"📊 {len(scan_folders)} saved scan(s)\n"
                f"📁 Location: {SaveLocations.get_saved_scans_folder()}"
            )

    def _parse_heatmap_metadata(self, data_path: Path, timestamp_str: str):
        """Parse metadata from JSON file and timestamp."""
        metadata = {
            "timestamp": timestamp_str,
            "formatted_date": "Unknown Date",
            "num_points": 0,
            "grid_size": 0,
            "min_rssi": None,
            "max_rssi": None,
            "avg_rssi": None,
            "blueprint_dims": None
        }

        # Parse timestamp: "20251210_143045" -> "Dec 10, 2025 02:30 PM"
        try:
            dt = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            metadata["formatted_date"] = dt.strftime("%b %d, %Y %I:%M %p")
        except:
            pass

        # Parse JSON data
        if data_path and data_path.exists():
            try:
                with open(data_path, 'r') as f:
                    data = json.load(f)
                    points = data.get("points", [])
                    metadata["num_points"] = len(points)
                    metadata["grid_size"] = data.get("grid_size", 0)

                    # Get blueprint dimensions
                    dims = data.get("blueprint_dimensions", {})
                    if dims:
                        metadata["blueprint_dims"] = f"{dims.get('width')}×{dims.get('height')}"

                    # Calculate RSSI statistics
                    if points:
                        rssi_values = [p[2] for p in points if len(p) >= 3]
                        if rssi_values:
                            metadata["min_rssi"] = min(rssi_values)
                            metadata["max_rssi"] = max(rssi_values)
                            metadata["avg_rssi"] = sum(rssi_values) / len(rssi_values)
            except Exception as e:
                print(f"Error parsing {data_path}: {e}")

        return metadata

    def on_heatmap_selected(self, item):
        """Update blueprint preview when a heatmap is selected."""
        # Find the corresponding heatmap by list index
        selected_index = self.heatmap_list_widget.currentRow()
        heatmap_keys = list(self.heatmap_data.keys())

        if selected_index < 0 or selected_index >= len(heatmap_keys):
            return

        heatmap_key = heatmap_keys[selected_index]
        heatmap_info = self.heatmap_data[heatmap_key]

        # Load and display the heatmap image
        heatmap_path = heatmap_info.get('heatmap_path')

        if heatmap_path and heatmap_path.exists():
            pixmap = QPixmap(str(heatmap_path))
            if not pixmap.isNull():
                # Scale to fit the preview area
                scaled_pixmap = pixmap.scaled(
                    self.blueprint_view.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.blueprint_view.setPixmap(scaled_pixmap)
                self.blueprint_view.setScaledContents(False)
            else:
                self.blueprint_view.setText("Error: Could not load image")
        else:
            self.blueprint_view.setText("Error: Heatmap file not found")

        # Update footer with detailed metadata
        footer = self.findChild(QLabel, "footer")
        if footer:
            stats_text = f"📊 {heatmap_info['formatted_date']}\n"
            stats_text += f"📍 Scan Points: {heatmap_info['num_points']}\n"

            if heatmap_info.get('blueprint_dims'):
                stats_text += f"📐 Blueprint: {heatmap_info['blueprint_dims']}px\n"

            if heatmap_info.get('avg_rssi'):
                stats_text += f"📶 RSSI Range: {heatmap_info['min_rssi']:.0f} to {heatmap_info['max_rssi']:.0f} dBm "
                stats_text += f"(avg: {heatmap_info['avg_rssi']:.1f} dBm)\n"

            stats_text += f"📁 {heatmap_info['folder_path'].name}"

            footer.setText(stats_text)
        else:
            self.blueprint_view.setText("Error: Heatmap file not found")

    def load_heatmaps(self):
        """Scan the resources/blueprint/heatmaps directory for saved heatmaps."""
        self.heatmap_list_widget.clear()
        self.heatmap_data.clear()

        # Find heatmaps directory
        # Try multiple possible locations
        possible_paths = [
            Path(__file__).parent.parent / "resources" / "blueprint" / "heatmaps",
            Path.cwd() / "app" / "resources" / "blueprint" / "heatmaps",
            Path.cwd() / "resources" / "blueprint" / "heatmaps",
        ]

        heatmaps_dir = None
        for path in possible_paths:
            if path.exists() and path.is_dir():
                heatmaps_dir = path
                break

        if not heatmaps_dir:
            self.heatmap_list_widget.addItem("No heatmaps directory found")
            return

        # Find all heatmap files
        heatmap_files = sorted(heatmaps_dir.glob("heatmap_*.png"), reverse=True)

        if not heatmap_files:
            self.heatmap_list_widget.addItem("No heatmaps saved yet")
            self.blueprint_view.setText("Generate some heatmaps first!")
            return

        # Load each heatmap
        for heatmap_file in heatmap_files:
            # Extract timestamp from filename (e.g., heatmap_20251209_213232.png)
            timestamp_str = heatmap_file.stem.replace("heatmap_", "")

            # Look for corresponding data file
            data_file = heatmaps_dir / f"scan_data_{timestamp_str}.json"

            # Create display name
            display_name = f"Heatmap {timestamp_str}"

            # Store the paths
            self.heatmap_data[display_name] = {
                'heatmap_path': str(heatmap_file),
                'data_path': str(data_file) if data_file.exists() else None
            }

            # Add to list
            item = QListWidgetItem(display_name)
            self.heatmap_list_widget.addItem(item)

        # Set initial message
        self.blueprint_view.setText(f"Found {len(heatmap_files)} heatmap(s).\nSelect one to view.")
