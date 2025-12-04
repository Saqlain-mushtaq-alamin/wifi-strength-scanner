from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget, QFileDialog, QVBoxLayout, QHBoxLayout
)
from qfluentwidgets import PrimaryPushButton, InfoBar, InfoBarPosition

from app.ui.widgets.blueprint_viewer import BlueprintViewer


class ScanPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._scan_ui()

    def _scan_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Top bar with upload button
        top_bar = QHBoxLayout()
        top_bar.setSpacing(8)

        self.upload_btn = PrimaryPushButton("Upload Image", self)
        self.upload_btn.clicked.connect(self._on_upload_clicked)

        top_bar.addWidget(self.upload_btn, 0, Qt.AlignmentFlag.AlignLeft)
        top_bar.addStretch(1)

        # Image viewer with invisible virtual grid
        self.viewer = BlueprintViewer(self)
        # Optional: tune grid resolution here or via set_grid_size()
        # self.viewer.set_grid_size(100)

        # Receive clicks (gridX, gridY, imgX, imgY)
        self.viewer.pointClicked.connect(self._on_point_clicked)

        main_layout.addLayout(top_bar)
        main_layout.addWidget(self.viewer, 1)

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