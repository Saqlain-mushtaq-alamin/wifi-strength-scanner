import json
import os
from datetime import datetime


class DataStore:
    """
    Handles all saving and loading of project data using JSON files.

    Each project folder contains:
        - project.json   (metadata)
        - points.json    (all scan points)
    """

    PROJECT_FILE = "project.json"
    POINTS_FILE = "points.json"

    def __init__(self, project_path):
        self.project_path = project_path
        self.project_file = os.path.join(project_path, self.PROJECT_FILE)
        self.points_file = os.path.join(project_path, self.POINTS_FILE)

        # Ensure folder and json files exist
        self._ensure_project_folder()
        self._ensure_json_files()

    # ----------------------------------------------------------------------
    # Internal helpers
    # ----------------------------------------------------------------------

    def _ensure_project_folder(self):
        """Create project directory if it doesn't exist."""
        os.makedirs(self.project_path, exist_ok=True)

    def _ensure_json_files(self):
        """Create empty JSON structure if missing."""
        if not os.path.exists(self.project_file):
            self.save_project_info({
                "name": "Untitled Project",
                "created": datetime.now().isoformat(),
                "blueprint": None
            })

        if not os.path.exists(self.points_file):
            self.save_points([])

    # ----------------------------------------------------------------------
    # Project metadata
    # ----------------------------------------------------------------------

    def save_project_info(self, data: dict):
        """Save project information to project.json"""
        with open(self.project_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_project_info(self) -> dict:
        """Load project metadata (name, blueprint path, etc.)"""
        try:
            with open(self.project_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    # ----------------------------------------------------------------------
    # Scan points
    # ----------------------------------------------------------------------

    def save_points(self, points: list):
        """Save all Wi-Fi scan points to points.json"""
        with open(self.points_file, "w", encoding="utf-8") as f:
            json.dump(points, f, indent=4)

    def load_points(self) -> list:
        """Load all scan points from points.json"""
        try:
            with open(self.points_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def add_point(self, x: float, y: float, signal: int):
        """
        Append one new scan point.

        point = {
            "x": pixel_x,
            "y": pixel_y,
            "signal": wifi_strength_percent,
            "time": "2025-12-04T10:32:10"
        }
        """
        points = self.load_points()
        points.append({
            "x": x,
            "y": y,
            "signal": signal,
            "time": datetime.now().isoformat()
        })
        self.save_points(points)
