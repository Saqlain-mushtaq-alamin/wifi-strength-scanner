from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget, QFileDialog, QVBoxLayout, QHBoxLayout
)
from qfluentwidgets import PrimaryPushButton, InfoBar, InfoBarPosition

from app.ui.widgets.blueprint_viewer import BlueprintViewer
from PySide6.QtWidgets import QApplication, QStackedWidget


class ScanPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._scan_ui()

    def _scan_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

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
                # If this page is inside a QStackedWidget, switch to the first page
                parent = self.parent()
                while parent is not None:
                    if isinstance(parent, QStackedWidget):
                        parent.setCurrentIndex(0)
                        return
                    parent = parent.parent()
                # Fallback: open main window
                try:
                    from importlib import import_module
                    try:
                        MainWindow = getattr(import_module("app.ui.main_windw"), "MainWindow")  # as requested
                    except Exception:
                        try:
                            MainWindow = getattr(import_module("app.ui.main_window"), "MainWindow")  # fallback name
                        except Exception:
                            MainWindow = None
                except Exception:
                    MainWindow = None
                if MainWindow is not None:
                    app = QApplication.instance()
                    mw = None
                    if isinstance(app, QApplication):
                        mw = next((w for w in app.topLevelWidgets() if isinstance(w, MainWindow)), None)
                    if mw is None:
                        mw = MainWindow()
                        mw.show()
                    win = self.window()
                    if win is not mw and hasattr(win, "close"):
                        win.close()
            except Exception as e:
                print(f"Back navigation failed: {e}")

        self.back_btn.clicked.connect(_go_back)
        header_layout.addWidget(self.back_btn, 0, Qt.AlignmentFlag.AlignLeft)
        header_layout.addStretch(1)

        # Add header to the top (non-expanding)
        main_layout.addWidget(header, 0)

        # Image viewer at the top (expanding)
        self.viewer = BlueprintViewer(self)
        # Receive clicks (gridX, gridY, imgX, imgY)
        self.viewer.pointClicked.connect(self._on_point_clicked)
        main_layout.addWidget(self.viewer, 1)

        # Bottom control panel container
        control_panel = QWidget(self)
        control_panel.setObjectName("controlPanel")
        cp_layout = QVBoxLayout(control_panel)
        cp_layout.setContentsMargins(12, 12, 12, 12)
        cp_layout.setSpacing(8)

        # Top row inside control panel: upload button aligned to the right
        row = QHBoxLayout()
        row.setSpacing(8)
        row.addStretch(1)

        self.upload_btn = PrimaryPushButton("Upload Image", control_panel)
        self.upload_btn.clicked.connect(self._on_upload_clicked)
        row.addWidget(self.upload_btn, 0, Qt.AlignmentFlag.AlignRight)

        cp_layout.addLayout(row)
        cp_layout.addStretch(1)

        # Add control panel at the bottom (non-expanding)
        main_layout.addWidget(control_panel, 0)

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