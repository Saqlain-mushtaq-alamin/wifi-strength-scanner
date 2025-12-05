from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget, QFileDialog, QVBoxLayout, QHBoxLayout
)
from qfluentwidgets import PrimaryPushButton, InfoBar, InfoBarPosition

from app.ui.widgets.blueprint_viewer import BlueprintViewer
from PySide6.QtWidgets import QApplication, QStackedWidget
from PySide6.QtWidgets import QLabel, QTextEdit
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QGraphicsOpacityEffect
from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon, QColor
from PySide6.QtCore import QSize
from pathlib import Path
from PySide6.QtWidgets import QToolButton



class ScanPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
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

        # Back button on the left
        self.back_btn = PrimaryPushButton("Back", header)
        self.back_btn.setFixedHeight(28)

        def _go_back():
            try:
                # Resolve MainWindow class (prefer main_windw.py, fallback to main_window.py)
                try:
                    from importlib import import_module






                    MainWindow = None
                    for mod in ("app.ui.main_windw", "app.ui.main_window"):
                        try:
                            MainWindow = getattr(import_module(mod), "MainWindow")
                            break
                        except Exception:
                            continue
                except Exception:
                    MainWindow = None

                top = self.window()

                # If we're already inside the main window, just go to the first page of the nearest QStackedWidget
                if MainWindow is not None and isinstance(top, MainWindow):
                    parent = self.parentWidget()
                    while parent is not None and not isinstance(parent, QStackedWidget):
                        parent = parent.parentWidget()
                    if isinstance(parent, QStackedWidget):
                        parent.setCurrentIndex(0)
                    return

                # Otherwise, show or create the main window and close this window
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

        # Image viewer at the top (expanding)
        self.viewer = BlueprintViewer(self)
        # Receive clicks (gridX, gridY, imgX, imgY)
        self.viewer.pointClicked.connect(self._on_point_clicked)
        main_layout.addWidget(self.viewer, 1)

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
        content_row = QHBoxLayout()
        content_row.setContentsMargins(0, 0, 0, 0)
        content_row.setSpacing(10)

        # Left: Image preview
        self.preview_label = QLabel(control_panel)
        self.preview_label.setMinimumSize(200, 150)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setText("Image preview")
        self.preview_label.setStyleSheet("""
        QLabel {
            border-radius: 8px;
            background: rgba(60, 80, 100, 80);
            border: 1px solid rgba(120, 200, 255, 60);
        }
        """)
        content_row.addWidget(self.preview_label, 0, Qt.AlignmentFlag.AlignLeft)

        # Middle: colorbar + status text (no animation)
        middle_col = QVBoxLayout()
        middle_col.setContentsMargins(0, 0, 0, 0)
        middle_col.setSpacing(6)

        self.colorbar_label = QLabel(control_panel)
        self.colorbar_label.setMinimumSize(200, 30)
        self.colorbar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.colorbar_label.setText("Signal strength scale")
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
        self.generate_btn.clicked.connect(self._on_upload_clicked)  # TODO: replace with real handler

        right_col.addStretch(1)
        content_row.addStretch(1)
        content_row.addLayout(right_col, 0)

        # Update status_text whenever a point is clicked
        def _update_status(gx: int, gy: int, ix: float, iy: float):
            self.status_text.setPlainText(
            f"Last point:\n"
            f"  Grid -> ({gx}, {gy})\n"
            f"  Image px -> ({ix:.1f}, {iy:.1f})"
            )
        self.viewer.pointClicked.connect(_update_status)

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
            "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp)"
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

        self.viewer.set_pixmap(pix)

    # Callback when a point is clicked in the viewer


    def _on_point_clicked(self, gx: int, gy: int, ix: float, iy: float):
        # Show a small toast with the coordinates
        InfoBar.success(
            title="Point added",
            content=f"Grid: ({gx}, {gy}) | Image px: ({ix:.1f}, {iy:.1f})",
            position=InfoBarPosition.TOP_RIGHT,
            parent=self
        )
        # Also print to terminal if you want
        print(f"Clicked grid=({gx},{gy}) image=({ix:.1f},{iy:.1f})")