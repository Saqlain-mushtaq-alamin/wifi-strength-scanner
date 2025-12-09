from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
<<<<<<< HEAD
    QWidget, QFileDialog, QVBoxLayout, QHBoxLayout
=======
    QWidget, QFileDialog, QVBoxLayout, QHBoxLayout, QSlider
>>>>>>> 444f61285cf23e5cd1a698db2026bff8a6846fc6
)
from qfluentwidgets import PrimaryPushButton, InfoBar, InfoBarPosition

from app.ui.widgets.blueprint_viewer import BlueprintViewer
<<<<<<< HEAD
from app.ui.wifi_input_dialog import WiFiInputDialog
from PySide6.QtWidgets import QApplication, QStackedWidget
from PySide6.QtWidgets import QLabel, QTextEdit
from PySide6.QtWidgets import QGraphicsDropShadowEffect
=======
from app.core.scanner import WifiScanner
from PySide6.QtWidgets import QApplication, QStackedWidget
from PySide6.QtWidgets import QLabel, QTextEdit
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtCore import QTimer
>>>>>>> 444f61285cf23e5cd1a698db2026bff8a6846fc6
from PySide6.QtGui import QIcon, QColor
from PySide6.QtCore import QSize
from pathlib import Path
from PySide6.QtWidgets import QToolButton



class ScanPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Data storage for scan points: [(x, y, rssi), ...]
        self.scan_points = []
        self.blueprint_path = None

        self._scan_ui()

    def _scan_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        #====================================================
        # Header section        
        #====================================================

        # Header container with a narrow height
        header = QWidget(self)
        header.setObjectName("headerContainer")
        header.setFixedHeight(36)  # very narrow
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(8, 4, 8, 4)
        header_layout.setSpacing(6)

        # Glassy look with top/bottom borders
        header.setStyleSheet("""
        #headerContainer {
            background: rgba(30, 36, 42, 140);  /* glassy translucent */
            border-top: 1px solid rgba(120, 200, 255, 160);
            border-bottom: 1px solid rgba(120, 200, 255, 160);
        }
        #headerContainer:hover {
            background: rgba(36, 42, 48, 170);
            border-top: 1px solid rgba(120, 200, 255, 220);
            border-bottom: 1px solid rgba(120, 200, 255, 220);
        }
        """)

        # Subtle shadow for depth
        shadow = QGraphicsDropShadowEffect(header)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 3)
        shadow.setColor(QColor(80, 140, 200, 160))
        header.setGraphicsEffect(shadow)

        # Back button on the left
        self.back_btn = PrimaryPushButton("Back", header)
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

        # Add header to the top (non-expanding)
        main_layout.addWidget(header, 0)

        #====================================================
        # Image viewer section
        #====================================================

        # Image viewer at the top (expanding) with left/right borders
        viewer_container = QWidget(self)
        viewer_container.setObjectName("viewerContainer")
        viewer_container.setStyleSheet("""
        #viewerContainer {
            border-left: 1px solid rgba(120, 200, 255, 160);
            border-right: 1px solid rgba(120, 200, 255, 160);
             
            border-top-left-radius: 20px;
            border-top-right-radius: 20px ;
            background: transparent;
        }
        """)
        vc_layout = QVBoxLayout(viewer_container)
        vc_layout.setContentsMargins(0, 0, 0, 0)
        vc_layout.setSpacing(0)

        self.viewer = BlueprintViewer(viewer_container)
        # Receive clicks (gridX, gridY, imgX, imgY)
        self.viewer.pointClicked.connect(self._on_point_clicked)
        vc_layout.addWidget(self.viewer)

        main_layout.addWidget(viewer_container, 1)

        #====================================================
        # Control panel section 
        #====================================================
        # Bottom control panel container  
        control_panel = QWidget(self)
        control_panel.setObjectName("controlPanel")
        cp_layout = QVBoxLayout(control_panel)
        # Slightly reduce padding and spacing to lower overall height
        cp_layout.setContentsMargins(12, 12, 12, 12)
        cp_layout.setSpacing(8)
        # Limit the height a little
        control_panel.setMaximumHeight(200)

        # Simple styling with hover effect on border/background
        control_panel.setStyleSheet("""
        #controlPanel {
            background: rgba(20, 24, 28, 160);
            border: 1px solid rgba(120, 200, 255, 60);
            border-radius: 12px;
        }
        #controlPanel:hover {
            background: rgba(24, 28, 34, 175);
            border: 1px solid rgba(120, 200, 255, 180);
        }
        QLabel {
            color: #d7eaff;
        }
        QTextEdit {
            background: rgba(30, 36, 42, 170);
            border: 1px solid rgba(120, 200, 255, 40);
            border-radius: 8px;
            color: #cfe7ff;
        }
        """)

        # Content row
        # Row for control panel content (keep compact to avoid overflow)
        content_row = QHBoxLayout()
        content_row.setContentsMargins(0, 0, 0, 0)
        content_row.setSpacing(8)
        content_row.setAlignment(Qt.AlignmentFlag.AlignTop)

        middle_col = QVBoxLayout()
        middle_col.setContentsMargins(0, 0, 0, 0)
        middle_col.setSpacing(6)



<<<<<<< HEAD
        # Left: vertical heatmap color scale (in a fixed-width panel)
        left_panel = QWidget(control_panel)
        left_panel.setObjectName("leftPanel")
        left_panel.setFixedWidth(60)  # narrower now that grid slider is removed
=======
        # Left: vertical grid scale + vertical slider (in a fixed-width panel to avoid overlap)
        left_panel = QWidget(control_panel)
        left_panel.setObjectName("leftPanel")
        left_panel.setFixedWidth(100)  # wider to fit numeric labels
>>>>>>> 444f61285cf23e5cd1a698db2026bff8a6846fc6
        left_panel_layout = QVBoxLayout(left_panel)
        left_panel_layout.setContentsMargins(0, 0, 0, 0)
        left_panel_layout.setSpacing(6)

<<<<<<< HEAD
=======
        # Move the vertical heatmap color scale to the left side of the horizontal slider row
        def _reposition_color_scale():
            try:
                color_scale_container = self.findChild(QWidget, "colorScaleContainer")
                if not color_scale_container:
                    return
                # Get the slider row layout (first item of self.slider's QVBoxLayout)
                sp_layout = getattr(self.slider, "layout", lambda: None)()
                if not sp_layout or sp_layout.count() == 0:
                    return
                slider_row_item = sp_layout.itemAt(0)
                slider_row = slider_row_item.layout() if slider_row_item else None
                if not slider_row:
                    return

                # Remove color_scale_container from its current parent layout
                parent_layout = color_scale_container.parentWidget().layout() if color_scale_container.parentWidget() else None
                if parent_layout:
                    for i in range(parent_layout.count()):
                        item = parent_layout.itemAt(i)
                        if item and item.widget() is color_scale_container:
                            parent_layout.takeAt(i)
                            break

                color_scale_container.setParent(self.slider)
                slider_row.insertWidget(0, color_scale_container, 0, Qt.AlignmentFlag.AlignTop)
            except Exception:
                pass

        QTimer.singleShot(0, _reposition_color_scale)
>>>>>>> 444f61285cf23e5cd1a698db2026bff8a6846fc6
        color_scale_container = QWidget(left_panel)
        color_scale_container.setObjectName("colorScaleContainer")
        color_scale_layout = QVBoxLayout(color_scale_container)
        color_scale_layout.setContentsMargins(0, 0, 0, 0)
        color_scale_layout.setSpacing(4)

        high_lbl = QLabel("High", color_scale_container)
        high_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        high_lbl.setStyleSheet("color: #d7eaff; font-size: 10px;")
        color_scale_layout.addWidget(high_lbl, 0)

        colorbar = QLabel(color_scale_container)
        colorbar.setFixedSize(20, 150)
        colorbar.setStyleSheet("""
            QLabel#colorbar {
            border: 1px solid rgba(120, 200, 255, 120);
            border-radius: 6px;
            background: qlineargradient(x1:0.5, y1:0, x2:0.5, y2:1,
                stop:0 #ff0000,       /* high (hot) */
                stop:0.25 #ff7f00,
                stop:0.5 #ffff00,
                stop:0.75 #00ff00,
                stop:1 #0000ff        /* low (cold) */
            );
            }
        """)
        colorbar.setObjectName("colorbar")
        color_scale_layout.addWidget(colorbar, 0, Qt.AlignmentFlag.AlignTop)

        low_lbl = QLabel("Low", color_scale_container)
        low_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        low_lbl.setStyleSheet("color: #d7eaff; font-size: 10px;")
        color_scale_layout.addWidget(low_lbl, 0)

<<<<<<< HEAD
        # add to the left panel
        left_panel_layout.addWidget(color_scale_container, 0, Qt.AlignmentFlag.AlignTop)
=======
        # add to the left panel (placed near the slider area)
        left_panel_layout.addWidget(color_scale_container, 0, Qt.AlignmentFlag.AlignTop)


        

        # A compact container holding: [labels | slider] and a bottom caption "Grid"
        self.slider = QWidget(left_panel)  # container widget (keeps external addWidget(self.slider) intact)
        slider_panel_layout = QVBoxLayout(self.slider)
        slider_panel_layout.setContentsMargins(0, 0, 0, 0)
        slider_panel_layout.setSpacing(4)

        # Row: labels (left) + real slider (right)
        slider_row = QHBoxLayout()
        slider_row.setContentsMargins(0, 0, 0, 0)
        slider_row.setSpacing(6)

        # Numeric labels on the left (0..200 step 25), arranged top->bottom to align with the slider
        labels_col = QVBoxLayout()
        labels_col.setContentsMargins(0, 0, 0, 0)
        labels_col.setSpacing(0)

        # Build marks from 200 (top) down to 0 (bottom) to match vertical slider
        marks = list(range(200, -1, -25))
        for i, val in enumerate(marks):
            lbl = QLabel(str(val), self.slider)
            lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            lbl.setStyleSheet("color: #cfe7ff; font-size: 10px;")
            labels_col.addWidget(lbl, 0)
            if i != len(marks) - 1:
                labels_col.addStretch(1)  # distribute labels evenly

        slider_row.addLayout(labels_col, 0)

        # The actual slider controlling grid size
        self.grid_slider = QSlider(Qt.Orientation.Vertical, self.slider)
        self.grid_slider.setMinimum(0)
        self.grid_slider.setMaximum(200)           # 0..200 as requested
        self.grid_slider.setSingleStep(5)
        self.grid_slider.setPageStep(25)
        # Try to initialize from viewer's current grid size if available
        try:
            current_grid = int(getattr(self.viewer, "_grid_px", 100))
        except Exception:
            current_grid = 100
        self.grid_slider.setValue(max(self.grid_slider.minimum(), min(self.grid_slider.maximum(), current_grid)))
        self.grid_slider.setFixedSize(26, 150)     # a little taller
        self.grid_slider.setTickPosition(QSlider.TickPosition.TicksLeft)
        self.grid_slider.setTickInterval(25)
        self.grid_slider.setStyleSheet("""
            QSlider::groove:vertical {
            border: 1px solid #bbb;
            background: #2a2f35;
            width: 8px;
            border-radius: 4px;
            }
            QSlider::sub-page:vertical {
            background: #4b5563;
            border: 1px solid #3b82f6;
            width: 8px;
            border-radius: 4px;
            }
            QSlider::add-page:vertical {
            background: #2a2f35;
            border: 1px solid #777;
            width: 8px;
            border-radius: 4px;
            }
            QSlider::handle:vertical {
            background: #4da6ff;
            border: 1px solid #2980b9;
            width: 18px;
            height: 18px;
            margin: 0;
            border-radius: 9px;
            }
        """)
        slider_row.addWidget(self.grid_slider, 0, Qt.AlignmentFlag.AlignTop)

        slider_panel_layout.addLayout(slider_row, 0)

        # Bottom caption "Grid"
        grid_caption = QLabel("Grid/px", self.slider)
        grid_caption.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        grid_caption.setStyleSheet("color: #d7eaff; font-size: 11px;")
        slider_panel_layout.addWidget(grid_caption, 0, Qt.AlignmentFlag.AlignTop)

        # When the slider changes, update BlueprintViewer grid size
        def _apply_grid_size(val: int):
            v = int(val)
            try:
                # Prefer public API set_grid_size; fallback to alias set_grid_px; else mutate attr
                setter = getattr(self.viewer, "set_grid_size", None)
                if not callable(setter):
                    setter = getattr(self.viewer, "set_grid_px", None)
                if callable(setter):
                    setter(v)
                else:
                    setattr(self.viewer, "_grid_px", v)
                    upd = getattr(self.viewer, "update", None)
                    if callable(upd):
                        upd()
            except Exception:
                pass

        self.grid_slider.valueChanged.connect(_apply_grid_size)
        left_panel_layout.addWidget(self.slider, 0, Qt.AlignmentFlag.AlignTop)
>>>>>>> 444f61285cf23e5cd1a698db2026bff8a6846fc6
        left_panel_layout.addStretch(1)

        # Add the left fixed panel to the content row
        content_row.addWidget(left_panel, 0, Qt.AlignmentFlag.AlignTop)

        # Middle: colorbar + status text (kept for layout compatibility, hidden)
        middle_col = QVBoxLayout()
        middle_col.setContentsMargins(0, 0, 0, 0)
        middle_col.setSpacing(6)

        self.colorbar_label = QLabel(control_panel)
        self.colorbar_label.setVisible(False)  # hidden, vertical bar shown on the left
        

        self.colorbar_label.setMinimumSize(200, 30)
        self.colorbar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
 
        self.colorbar_label.setStyleSheet("""
            QLabel {
            border-radius: 6px;
            border: 1px solid rgba(120, 200, 255, 120);
            background: qlineargradient(x1:0, y1:0.5, x2:1, y2:0.5,
                stop:0 #001122,
                stop:0.2 #21d4fd,
                stop:0.5 #b721ff,
                stop:0.8 #21d4fd,
                stop:1 #001122);
            }
        """)
        middle_col.addWidget(self.colorbar_label, 0, Qt.AlignmentFlag.AlignTop)

        self.status_text = QTextEdit(control_panel)
        self.status_text.setReadOnly(True)
        self.status_text.setPlaceholderText("Click on the blueprint to see point details here.")
        self.status_text.setMinimumSize(300, 100)
        middle_col.addWidget(self.status_text, 0, Qt.AlignmentFlag.AlignTop)

        content_row.addLayout(middle_col, 1)



       
        # Right: buttons column
        right_col = QVBoxLayout()
        right_col.setContentsMargins(0, 0, 0, 0)
        right_col.setSpacing(10)

        # resolve icons from app/resources/icon relative to this file
        def load_icon(filename: str) -> QIcon:
            # resources/icon folder is sibling of ui folder
            res_dir = Path(__file__).resolve().parent.parent / "resources" / "icon"
            p = res_dir / filename
            if p.exists():
                pix = QPixmap(str(p))
                if not pix.isNull():
                    return QIcon(pix)
            return QIcon()  # empty, no crash


        # Upload button (icon above text, bigger icon, taller button)
        self.upload_btn = QToolButton(control_panel)
        self.upload_btn.setObjectName("uploadBtn")
        self.upload_btn.setText(" Upload Blueprint ")
        self.upload_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.upload_btn.setIcon(load_icon("load.gif"))
        self.upload_btn.setIconSize(QSize(40, 40))  # bigger icon
        self.upload_btn.setFixedHeight(80)  # taller button
        self.upload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        right_col.addWidget(self.upload_btn, 0, Qt.AlignmentFlag.AlignTop)

        # Generate button (icon above text, bigger icon, taller button)
        self.generate_btn = QToolButton(control_panel)
        self.generate_btn.setObjectName("generateBtn")
        self.generate_btn.setText("Generate Heatmap")
        self.generate_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.generate_btn.setIcon(load_icon("blog.gif"))
        self.generate_btn.setIconSize(QSize(40, 40))  # bigger icon
        self.generate_btn.setFixedHeight(80)  # taller button
        self.generate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        right_col.addWidget(self.generate_btn, 0, Qt.AlignmentFlag.AlignTop)

        # subtle glow/shadow
        for btn in (self.upload_btn, self.generate_btn):
            eff = QGraphicsDropShadowEffect(btn)
            eff.setBlurRadius(16)
            eff.setOffset(0, 2)
            eff.setColor(QColor(120, 200, 255, 160))
            btn.setGraphicsEffect(eff)

        # shiny hover styles
        control_panel.setStyleSheet(control_panel.styleSheet() + """
        #uploadBtn, #generateBtn {
            border: 1px solid rgba(120, 200, 255, 120);
            border-radius: 8px;
            color: #d7eaff;
            padding: 8px 14px; /* slightly more padding for taller buttons */
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(30, 36, 42, 220),
            stop:0.5 rgba(24, 30, 36, 220),
            stop:1 rgba(20, 26, 32, 220)
            );
        }
        #uploadBtn:hover, #generateBtn:hover {
            border: 1px solid rgba(120, 200, 255, 220);
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 rgba(21, 212, 253, 180),
            stop:1 rgba(183, 33, 255, 180)
            );
        }
        #uploadBtn:pressed, #generateBtn:pressed {
            background: rgba(21, 212, 253, 140);
        }
        """)

        # Wire buttons
        self.upload_btn.clicked.connect(self._on_upload_clicked)
        self.generate_btn.clicked.connect(self._on_generate_heatmap)

        right_col.addStretch(1)
        content_row.addStretch(1)
        content_row.addLayout(right_col, 0)

        # Note: status updates are handled in _on_point_clicked

        cp_layout.addLayout(content_row)
        cp_layout.addStretch(1)

        # Add control panel at the bottom
        main_layout.addWidget(control_panel, 0)


    #====================================================
    #button action sections 
    #====================================================



    #button to upload image and load into viewer

    def _on_upload_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select an image",
            "",
            "Images (*.svg *.png *.jpg *.jpeg *.bmp *.gif *.webp)"
        )
        if not file_path:
            return

        pix = QPixmap(file_path)
        if pix.isNull():
            InfoBar.error(
                title="Failed to load image",
                content="Unsupported format or corrupted file.",
                position=InfoBarPosition.TOP,
                parent=self
            )
            return

        self.blueprint_path = file_path
        self.viewer.set_pixmap(pix)

        # Clear previous scan points when new blueprint is loaded
        self.scan_points.clear()
        self.viewer.clear_markers()

        InfoBar.success(
            title="Blueprint Loaded",
            content=f"Successfully loaded: {Path(file_path).name}",
            position=InfoBarPosition.TOP,
            parent=self
        )

    # Callback when a point is clicked in the viewer


<<<<<<< HEAD
    def _on_point_clicked(self, ix: float, iy: float):
        """Show dialog to choose between auto-scan or manual RSSI input."""
        # Show the dialog
        dialog = WiFiInputDialog(self, ix, iy)
        result = dialog.exec()

        if result != WiFiInputDialog.DialogCode.Accepted:
            # User cancelled - remove the marker
            if self.viewer._markers:
                self.viewer._markers.pop()
                self.viewer.update()
            return

        # Get the results from the dialog
        wifi_info = dialog.wifi_info
        rssi_value = dialog.rssi_value

        # Build a concise message
=======
    def _on_point_clicked(self, gx: int, gy: int, ix: float, iy: float):
        # Fetch WiFi scan details and display along with coordinates
        wifi_info = None
        try:
            wifi_info = WifiScanner.scan()
 
        except Exception as e:
            wifi_info = {"error": str(e)}

        # Build a concise message
        rssi_value = None
>>>>>>> 444f61285cf23e5cd1a698db2026bff8a6846fc6
        if wifi_info and isinstance(wifi_info, dict):
            ssid = wifi_info.get("ssid")
            bssid = wifi_info.get("bssid")
            signal = wifi_info.get("signal")
            rssi = wifi_info.get("rssi")
<<<<<<< HEAD
=======
            rssi_value = rssi  # Store for data collection
>>>>>>> 444f61285cf23e5cd1a698db2026bff8a6846fc6
            channel = wifi_info.get("channel")
            radio = wifi_info.get("radio")
            band = wifi_info.get("band")

            wifi_text = (
                f"SSID: {ssid or 'N/A'} | BSSID: {bssid or 'N/A'} | "
                f"Signal: {signal if signal is not None else 'N/A'}% "
                f"(RSSI: {rssi if rssi is not None else 'N/A'}) | "
                f"Channel: {channel or 'N/A'} | Radio: {radio or 'N/A'} | Band: {band or 'N/A'}"
            )
        else:
            wifi_text = "WiFi info unavailable"

        # Store the scan point data (x, y, rssi)
        if rssi_value is not None:
            self.scan_points.append((ix, iy, rssi_value))
            print(f"Stored scan point: ({ix:.1f}, {iy:.1f}, {rssi_value})")
        else:
            # If no rssi, still allow manual input or placeholder
            print(f"Warning: No RSSI value for point ({ix:.1f}, {iy:.1f})")
<<<<<<< HEAD
            # Remove the marker if no valid data
            if self.viewer._markers:
                self.viewer._markers.pop()
                self.viewer.update()
            return
=======

>>>>>>> 444f61285cf23e5cd1a698db2026bff8a6846fc6

        # Update status panel for persistent view
        self.status_text.setPlainText(
            f"Last point:\n"
<<<<<<< HEAD
            f"  Pixel coordinates -> ({ix:.1f}, {iy:.1f})\n\n"
            f"WiFi:\n  {wifi_text}\n\n"
=======
            f"  Grid -> ({gx}, {gy})\n"
            f"  Image px -> ({ix:.1f}, {iy:.1f})\n\n"
            f"WiFi:\n  {wifi_text}\n\n"
            f"Grid size: {self.viewer._grid_px}px\n"
>>>>>>> 444f61285cf23e5cd1a698db2026bff8a6846fc6
            f"Total points collected: {len(self.scan_points)}"
        )

        # Also print to terminal for debugging
        print(
<<<<<<< HEAD
            f"Clicked at pixel=({ix:.1f},{iy:.1f}); {wifi_text}"
=======
            f"Clicked grid=({gx},{gy}) image=({ix:.1f},{iy:.1f}); {wifi_text}"
>>>>>>> 444f61285cf23e5cd1a698db2026bff8a6846fc6
        )

    def _on_generate_heatmap(self):
        """Generate heatmap from collected scan points and blend with blueprint."""
        # Validate we have data
        if not self.scan_points:
            InfoBar.warning(
                title="No Data",
                content="Please scan some WiFi points first by clicking on the blueprint.",
                position=InfoBarPosition.TOP,
                parent=self
            )
            return

        if not self.blueprint_path:
            InfoBar.warning(
                title="No Blueprint",
                content="Please upload a blueprint image first.",
                position=InfoBarPosition.TOP,
                parent=self
            )
            return

        try:
            import cv2
            import numpy as np
            from app.core.heatmap_engine import generate_heatmap
            from app.core.image_blender import blend

            # Load blueprint as OpenCV image
            blueprint_bgr = cv2.imread(self.blueprint_path)
            if blueprint_bgr is None:
                InfoBar.error(
                    title="Error",
                    content="Failed to load blueprint image.",
                    position=InfoBarPosition.TOP,
                    parent=self
                )
                return

            height, width = blueprint_bgr.shape[:2]

            # Generate heatmap using collected points
            print(f"Generating heatmap from {len(self.scan_points)} points...")
            print(f"Blueprint size: {width}x{height}")

            heatmap_bgr = generate_heatmap(
                points=self.scan_points,
                width=width,
                height=height,
                power=2
            )

            # Blend heatmap with blueprint
            blended = blend(blueprint_bgr, heatmap_bgr, alpha=0.6)

            # Save the result
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = Path(self.blueprint_path).parent / "heatmaps"
            output_dir.mkdir(exist_ok=True)

            output_path = output_dir / f"heatmap_{timestamp}.png"
            cv2.imwrite(str(output_path), blended)

            # Also save scan points data
            data_path = output_dir / f"scan_data_{timestamp}.json"
            import json
            with open(data_path, 'w') as f:
                json.dump({
                    'blueprint': str(self.blueprint_path),
                    'timestamp': timestamp,
<<<<<<< HEAD
                    'points': [(float(x), float(y), float(rssi)) for x, y, rssi in self.scan_points]
=======
                    'points': [(float(x), float(y), float(rssi)) for x, y, rssi in self.scan_points],
                    'grid_size': self.viewer._grid_px
>>>>>>> 444f61285cf23e5cd1a698db2026bff8a6846fc6
                }, f, indent=2)

            InfoBar.success(
                title="Heatmap Generated",
                content=f"Saved to: {output_path.name}",
                position=InfoBarPosition.TOP,
                parent=self,
                duration=5000
            )

            print(f"Heatmap saved to: {output_path}")
            print(f"Scan data saved to: {data_path}")

            # Display the result in the viewer
            result_pixmap = QPixmap(str(output_path))
            if not result_pixmap.isNull():
                self.viewer.set_pixmap(result_pixmap)
                self.viewer.clear_markers()  # Clear markers since we're now showing the result

        except Exception as e:
            InfoBar.error(
                title="Generation Failed",
                content=f"Error: {str(e)}",
                position=InfoBarPosition.TOP,
                parent=self,
                duration=5000
            )
            print(f"Heatmap generation error: {e}")
            import traceback
            traceback.print_exc()

