
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QAbstractItemView

class HeatmapList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.heatmaps_list()

    def heatmaps_list(self):
        layout = QVBoxLayout()

        self.heatmap_list_widget = QListWidget()
        self.heatmap_list_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.heatmap_list_widget.itemClicked.connect(self.on_heatmap_selected)

        layout.addWidget(self.heatmap_list_widget)
        self.setLayout(layout)
