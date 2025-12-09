from __future__ import annotations

from typing import List
from PySide6.QtCore import Qt, QPointF, QRectF, Signal
from PySide6.QtGui import QPainter, QPixmap, QPen, QColor
from PySide6.QtWidgets import QWidget


class BlueprintViewer(QWidget):
    # Emits: gridX, gridY, imageX, imageY (float)
    pointClicked = Signal(int, int, float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap: QPixmap | None = None
        self._markers: List[QPointF] = []

        # Grid resolution (pixels per cell) — tune this to your needs:
        # e.g., 50 or 100
        #self._grid_px: int = 100  # <<< adjust grid size here

        self.setMouseTracking(False)
        self.setMinimumSize(100, 100)

    # Public API
    def set_pixmap(self, pix: QPixmap | None):
        self._pixmap = pix if (pix and not pix.isNull()) else None
        self._markers.clear()
        self.update()

    def set_grid_size(self, px: int):
        if px > 0:
            self._grid_px = px
            self.update()
            print(f"BlueprintViewer: grid size set to {px} px")

    # Backward-compatible alias used by some callers
    def set_grid_px(self, px: int):
        self.set_grid_size(px)

    def clear_markers(self):
        self._markers.clear()
        self.update()

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
        if event.button() == Qt.MouseButton.LeftButton and self._pixmap:
            img_pt = self._widget_to_image(event.position())
            if img_pt is not None:
                # Convert to grid cell
                gx = int(img_pt.x() // self._grid_px)
                gy = int(img_pt.y() // self._grid_px)

                # Store marker in image coordinates
                self._markers.append(img_pt)
                self.update()

                # Emit clicked signal
                self.pointClicked.emit(gx, gy, float(img_pt.x()), float(img_pt.y()))
        super().mousePressEvent(event)

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
                for pt in self._markers:
                    wx = rect.x() + pt.x() * sx
                    wy = rect.y() + pt.y() * sx
                    r = 5
                    painter.drawEllipse(QPointF(wx, wy), r, r)
        else:
            # Optional: draw a placeholder background
            pass