from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QFileDialog, QLabel,
    QVBoxLayout, QHBoxLayout, QSizePolicy
)
from qfluentwidgets import PrimaryPushButton, InfoBar, InfoBarPosition


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Image Viewer - PySide6 + QFluentWidgets")
        self._pixmap: QPixmap | None = None

        self._setup_ui()

    def _setup_ui(self):
        central = QWidget(self)
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Top bar with upload button
        top_bar = QHBoxLayout()
        top_bar.setSpacing(8)

        self.upload_btn = PrimaryPushButton("Upload Image", self)
        self.upload_btn.clicked.connect(self._on_upload_clicked)

        top_bar.addWidget(self.upload_btn, 0, Qt.AlignmentFlag.AlignLeft)
        top_bar.addStretch(1)

        # Image display area
        self.image_label = QLabel(self)
        self.image_label.setText("No image loaded")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Prevent QLabel's pixmap sizeHint from expanding the window
        self.image_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.image_label.setMinimumSize(1, 1)
        self.image_label.setStyleSheet(
            "QLabel { background: rgba(120,120,120,0.08); "
            "border: 1px dashed rgba(120,120,120,0.35); }"
        )

        main_layout.addLayout(top_bar)
        main_layout.addWidget(self.image_label, 1)

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

        self._pixmap = pix
        self._update_scaled_pixmap()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_scaled_pixmap()

    def _update_scaled_pixmap(self):
        if not self._pixmap:
            return

        available_size = self.image_label.size()
        if available_size.width() < 2 or available_size.height() < 2:
            return

        scaled = self._pixmap.scaled(
            available_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled)
