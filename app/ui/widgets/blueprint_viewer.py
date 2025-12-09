from __future__ import annotations

from typing import List, Optional
from PySide6.QtCore import Qt, QPointF, QRectF, Signal
from PySide6.QtGui import QPainter, QPixmap, QPen, QColor, QAction
from PySide6.QtWidgets import QWidget, QMenu


class MarkerData:
    """Stores marker position and associated RSSI data."""
    def __init__(self, x: float, y: float, rssi: Optional[float] = None):
        self.x = x
        self.y = y
        self.rssi = rssi


class BlueprintViewer(QWidget):
    # Emits: imageX, imageY (float pixel coordinates)
    pointClicked = Signal(float, float)
    # Emits when an existing marker is clicked: marker_index
    markerClicked = Signal(int)
    # Emits when marker deletion is requested: marker_index
    markerDeleteRequested = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap: QPixmap | None = None
        self._markers: List[MarkerData] = []

        self.setMouseTracking(False)
        self.setMinimumSize(100, 100)

    # Public API
    def set_pixmap(self, pix: QPixmap | None):
        self._pixmap = pix if (pix and not pix.isNull()) else None
        self._markers.clear()
        self.update()

    def clear_markers(self):
        self._markers.clear()
        self.update()

    def add_marker(self, x: float, y: float, rssi: Optional[float] = None):
        """Add a new marker at the given position with optional RSSI."""
        self._markers.append(MarkerData(x, y, rssi))
        self.update()

    def update_marker_rssi(self, index: int, rssi: float):
        """Update the RSSI value for an existing marker."""
        if 0 <= index < len(self._markers):
            self._markers[index].rssi = rssi
            self.update()

    def get_marker_data(self, index: int) -> Optional[MarkerData]:
        """Get marker data at given index."""
        if 0 <= index < len(self._markers):
            return self._markers[index]
        return None

    # Helpers
    def _image_draw_rect(self) -> QRectF:
        if not self._pixmap:
            return QRectF()

        w, h = self.width(), self.height()
        pw, ph = self._pixmap.width(), self._pixmap.height()
        if pw == 0 or ph == 0 or w == 0 or h == 0:
            return QRectF()

        scale = min(w / pw, h / ph)
        dw, dh = pw * scale, ph * scale
        x = (w - dw) / 2.0
        y = (h - dh) / 2.0
        return QRectF(x, y, dw, dh)

    def _widget_to_image(self, pos) -> QPointF | None:
        if not self._pixmap:
            return None

        rect = self._image_draw_rect()
        if rect.isNull() or not rect.contains(pos):
            return None

        pw, ph = self._pixmap.width(), self._pixmap.height()
        sx = rect.width() / pw
        sy = rect.height() / ph  # sx == sy with KeepAspectRatio
        ix = (pos.x() - rect.x()) / sx
        iy = (pos.y() - rect.y()) / sy
        return QPointF(ix, iy)

    # Events
    def mousePressEvent(self, event):
        if self._pixmap:
            img_pt = self._widget_to_image(event.position())
            if img_pt is not None:
                # Check if clicking on an existing marker
                marker_idx = self._find_marker_at(img_pt)

                # Right-click on marker - show context menu
                if event.button() == Qt.MouseButton.RightButton and marker_idx is not None:
                    self._show_marker_context_menu(event.globalPosition().toPoint(), marker_idx)
                    return

                # Left-click handling
                if event.button() == Qt.MouseButton.LeftButton:
                    if marker_idx is not None:
                        # Clicked on existing marker - emit markerClicked signal
                        self.markerClicked.emit(marker_idx)
                    else:
                        # New point - store marker placeholder (RSSI will be added later)
                        self._markers.append(MarkerData(img_pt.x(), img_pt.y(), None))
                        self.update()

                        # Emit clicked signal with pixel coordinates
                        self.pointClicked.emit(float(img_pt.x()), float(img_pt.y()))
        super().mousePressEvent(event)

    def _find_marker_at(self, img_pt: QPointF) -> Optional[int]:
        """Find if a marker exists at the given image point. Returns marker index or None."""
        CLICK_RADIUS = 10  # pixels in image coordinates
        for idx, marker in enumerate(self._markers):
            dx = img_pt.x() - marker.x
            dy = img_pt.y() - marker.y
            dist_sq = dx * dx + dy * dy
            if dist_sq <= CLICK_RADIUS * CLICK_RADIUS:
                return idx
        return None

    def _show_marker_context_menu(self, global_pos, marker_idx: int):
        """Show context menu for marker operations."""
        menu = QMenu(self)

        marker = self._markers[marker_idx]
        rssi_text = f"{marker.rssi:.0f} dBm" if marker.rssi else "No RSSI"

        # Menu title
        title_action = QAction(f"Marker at ({marker.x:.0f}, {marker.y:.0f})", menu)
        title_action.setEnabled(False)
        menu.addAction(title_action)

        menu.addSeparator()

        # Edit action
        edit_action = QAction(f"Edit ({rssi_text})", menu)
        edit_action.triggered.connect(lambda: self.markerClicked.emit(marker_idx))
        menu.addAction(edit_action)

        # Delete action
        delete_action = QAction("Delete Marker", menu)
        delete_action.triggered.connect(lambda: self.markerDeleteRequested.emit(marker_idx))
        menu.addAction(delete_action)

        menu.exec(global_pos)

    def delete_marker(self, index: int):
        """Delete marker at given index."""
        if 0 <= index < len(self._markers):
            self._markers.pop(index)
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.RenderHint.Antialiasing
            | QPainter.RenderHint.SmoothPixmapTransform
            | QPainter.RenderHint.TextAntialiasing
        )

        # Draw pixmap scaled to fit (KeepAspectRatio), centered
        if self._pixmap and not self._pixmap.isNull():
            target = self._image_draw_rect()
            if not target.isNull():
                painter.drawPixmap(target.toRect(), self._pixmap)

                # Draw markers (small circles) at clicked points
                pw = self._pixmap.width()
                rect = target
                sx = rect.width() / pw  # uniform scale

                pen = QPen(QColor(230, 60, 60), 2)
                painter.setPen(pen)
                for marker in self._markers:
                    wx = rect.x() + marker.x * sx
                    wy = rect.y() + marker.y * sx
                    r = 5
                    painter.drawEllipse(QPointF(wx, wy), r, r)

                    # Optionally draw RSSI value near marker
                    if marker.rssi is not None:
                        painter.setPen(QColor(255, 255, 255))
                        painter.drawText(int(wx + 8), int(wy - 8), f"{marker.rssi:.0f}")
                        painter.setPen(pen)
        else:
            # Optional: draw a placeholder background
            pass