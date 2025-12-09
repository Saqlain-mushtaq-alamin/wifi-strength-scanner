import json
import os
from datetime import datetime


class DataStore:
    PROJECT_FILE = "project.json"
    POINTS_FILE = "points.json"

    def __init__(self, project_path):
        self.project_path = project_path
        self.project_file = os.path.join(project_path, self.PROJECT_FILE)
        self.points_file = os.path.join(project_path, self.POINTS_FILE)

        self._ensure_project_folder()
        self._ensure_json_files()

    def _ensure_project_folder(self):
        os.makedirs(self.project_path, exist_ok=True)

    def _ensure_json_files(self):
        if not os.path.exists(self.project_file):
            self.save_project_info({
                "name": "Untitled Project",
                "created": datetime.now().isoformat(),
                "blueprint": None,
                "grid_size": 100
            })

        if not os.path.exists(self.points_file):
            self.save_points([])

    # ---------------- Project Metadata ----------------

    def save_project_info(self, data: dict):
        with open(self.project_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_project_info(self) -> dict:
        try:
            with open(self.project_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    # ---------------- Scan Points ----------------

    def save_points(self, points: list):
        """
        Save minimal point format:
        [
            [x, y, rssi],
            ...
        ]
        """
        with open(self.points_file, "w", encoding="utf-8") as f:
            json.dump(points, f, indent=4)

    def load_points(self) -> list:
        """Return minimal format: list of lists."""
        try:
            with open(self.points_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def add_point(self, x: float, y: float, rssi: int):
        points = self.load_points()
        points.append([x, y, rssi])
        self.save_points(points)
