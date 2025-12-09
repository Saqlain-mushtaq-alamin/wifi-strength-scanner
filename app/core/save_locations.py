"""
Utility module for managing WiFi Scanner save locations and folder structure.
"""
from pathlib import Path
import os


class SaveLocations:
    """Centralized management of save locations for WiFi Scanner."""

    @staticmethod
    def get_user_documents_folder() -> Path:
        """Get the user's Documents folder in a cross-platform way."""
        if os.name == 'nt':  # Windows
            return Path.home() / "Documents"
        else:  # macOS/Linux
            return Path.home() / "Documents"

    @staticmethod
    def get_app_data_folder() -> Path:
        """Get the main WiFiScanner folder in user's Documents."""
        base = SaveLocations.get_user_documents_folder()
        app_folder = base / "WiFiScanner"
        app_folder.mkdir(parents=True, exist_ok=True)
        return app_folder

    @staticmethod
    def get_saved_scans_folder() -> Path:
        """Get the Saved_Scans folder where all heatmaps are stored."""
        scans_folder = SaveLocations.get_app_data_folder() / "Saved_Scans"
        scans_folder.mkdir(parents=True, exist_ok=True)
        return scans_folder

    @staticmethod
    def get_blueprints_folder() -> Path:
        """Get the Blueprints folder where uploaded blueprints are stored."""
        blueprints_folder = SaveLocations.get_app_data_folder() / "Blueprints"
        blueprints_folder.mkdir(parents=True, exist_ok=True)
        return blueprints_folder

    @staticmethod
    def get_exports_folder() -> Path:
        """Get the Exports folder for exported reports/data."""
        exports_folder = SaveLocations.get_app_data_folder() / "Exports"
        exports_folder.mkdir(parents=True, exist_ok=True)
        return exports_folder

    @staticmethod
    def create_scan_folder(scan_name: str) -> Path:
        """
        Create a folder for a specific scan session.

        Args:
            scan_name: Name/timestamp for this scan (e.g., "20251210_143045")

        Returns:
            Path to the created scan folder
        """
        scan_folder = SaveLocations.get_saved_scans_folder() / scan_name
        scan_folder.mkdir(parents=True, exist_ok=True)
        return scan_folder

    @staticmethod
    def get_scan_heatmap_path(scan_name: str) -> Path:
        """Get the path for the heatmap image of a scan."""
        scan_folder = SaveLocations.create_scan_folder(scan_name)
        return scan_folder / f"heatmap_{scan_name}.png"

    @staticmethod
    def get_scan_data_path(scan_name: str) -> Path:
        """Get the path for the JSON data of a scan."""
        scan_folder = SaveLocations.create_scan_folder(scan_name)
        return scan_folder / f"scan_data_{scan_name}.json"

    @staticmethod
    def get_scan_blueprint_path(scan_name: str) -> Path:
        """Get the path for the blueprint copy in the scan folder."""
        scan_folder = SaveLocations.create_scan_folder(scan_name)
        return scan_folder / "blueprint.png"

    @staticmethod
    def list_all_scans() -> list[Path]:
        """
        List all scan folders in Saved_Scans directory.

        Returns:
            List of Path objects for each scan folder, sorted newest first
        """
        scans_folder = SaveLocations.get_saved_scans_folder()
        scan_folders = [f for f in scans_folder.iterdir() if f.is_dir()]
        # Sort by name (which is timestamp) in reverse order (newest first)
        return sorted(scan_folders, reverse=True)

    @staticmethod
    def migrate_old_scans():
        """
        Migrate scans from old location (app/resources/blueprint/heatmaps)
        to new location (Documents/WiFiScanner/Saved_Scans).
        """
        # Find old heatmaps directory
        old_dir = Path(__file__).parent.parent / "resources" / "blueprint" / "heatmaps"

        if not old_dir.exists():
            return

        # Find all old heatmap files
        old_heatmaps = list(old_dir.glob("heatmap_*.png"))

        if not old_heatmaps:
            return

        print(f"Found {len(old_heatmaps)} old scans to migrate...")

        for old_heatmap in old_heatmaps:
            # Extract timestamp from filename
            timestamp = old_heatmap.stem.replace("heatmap_", "")

            # Create new scan folder
            new_folder = SaveLocations.create_scan_folder(timestamp)

            # Copy heatmap
            new_heatmap = new_folder / f"heatmap_{timestamp}.png"
            if not new_heatmap.exists():
                import shutil
                shutil.copy2(old_heatmap, new_heatmap)
                print(f"Migrated heatmap: {timestamp}")

            # Copy JSON data if exists
            old_json = old_dir / f"scan_data_{timestamp}.json"
            if old_json.exists():
                new_json = new_folder / f"scan_data_{timestamp}.json"
                if not new_json.exists():
                    import shutil
                    shutil.copy2(old_json, new_json)
                    print(f"Migrated data: {timestamp}")

        print("Migration complete!")
        print(f"Old scans are still in: {old_dir}")
        print(f"New location: {SaveLocations.get_saved_scans_folder()}")

