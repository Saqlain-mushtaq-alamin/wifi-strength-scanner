# 📁 WiFi Scanner Save Locations Guide

## New Organized File Structure

All WiFi Scanner data is now saved in a dedicated folder in your Documents directory for easy access and backup.

---

## 📍 Main Save Location

```
C:\Users\{YourName}\Documents\WiFiScanner\
```

This folder is automatically created when you generate your first heatmap.

---

## 📂 Folder Structure

```
Documents/
└── WiFiScanner/
    ├── Saved_Scans/           # All your heatmap scans
    │   ├── 20251210_143045/   # Individual scan folder (timestamp)
    │   │   ├── heatmap_20251210_143045.png      # Generated heatmap image
    │   │   ├── scan_data_20251210_143045.json   # Scan point data
    │   │   └── blueprint.png                     # Copy of original blueprint
    │   │
    │   ├── 20251210_150230/   # Another scan
    │   │   ├── heatmap_20251210_150230.png
    │   │   ├── scan_data_20251210_150230.json
    │   │   └── blueprint.png
    │   │
    │   └── ...
    │
    ├── Blueprints/            # Your uploaded blueprints (future)
    └── Exports/               # Exported reports (future)
```

---

## 📊 Scan Folder Contents

Each scan folder contains:

### 1. **Heatmap Image** (`heatmap_YYYYMMDD_HHMMSS.png`)
- The final WiFi strength visualization
- Blueprint with color-coded heatmap overlay
- Ready to share or print

### 2. **Scan Data** (`scan_data_YYYYMMDD_HHMMSS.json`)
- All scan point coordinates and RSSI values
- Metadata: timestamp, number of points, blueprint dimensions
- Can be re-analyzed or exported to other formats

**Example JSON structure:**
```json
{
  "blueprint": "path/to/blueprint.png",
  "original_blueprint": "path/to/original.jpg",
  "timestamp": "20251210_143045",
  "generated_at": "2025-12-10T14:30:45.123456",
  "num_points": 78,
  "blueprint_dimensions": {
    "width": 800,
    "height": 1200
  },
  "points": [
    [235.62, 466.31, -77.0],  // [x, y, rssi]
    [352.20, 751.82, -77.0],
    ...
  ]
}
```

### 3. **Blueprint Copy** (`blueprint.png`)
- Original blueprint used for this scan
- Ensures you can always regenerate the heatmap
- Useful if original blueprint is moved/deleted

---

## 🔄 Migration from Old Location

If you have existing scans in the old location (`app/resources/blueprint/heatmaps/`), they will be **automatically migrated** to the new location when you:

1. Open the History tab for the first time
2. Generate a new heatmap

**Old scans remain in original location** (not deleted) so you have a backup.

---

## 🎯 Benefits of New Structure

### ✅ Easy Access
- Open directly from File Explorer
- No need to navigate through app folders
- Quick sharing with colleagues

### ✅ Easy Backup
- Simply copy `WiFiScanner` folder to backup drive
- Sync with cloud storage (OneDrive, Dropbox, etc.)
- Transfer to another computer easily

### ✅ Organization
- Each scan in its own folder
- Chronologically sorted by timestamp
- All related files kept together

### ✅ Portability
- Export to USB drive
- Email specific scans
- Archive old scans to separate folder

---

## 🔍 Finding Your Scans

### Method 1: Through the App
1. Open WiFi Scanner
2. Click "History" tab
3. Click any scan to preview
4. Footer shows folder location

### Method 2: File Explorer
1. Open File Explorer
2. Navigate to: `Documents\WiFiScanner\Saved_Scans\`
3. Folders sorted newest to oldest
4. Double-click any PNG to view

### Method 3: Quick Access
Create a shortcut:
1. Right-click `Saved_Scans` folder
2. "Send to" → "Desktop (create shortcut)"
3. Pin to Quick Access in File Explorer

---

## 🗑️ Deleting Scans

### Through the App (Future Feature)
- Right-click scan in History tab
- Select "Delete"
- Confirmation dialog appears

### Manually
1. Open `Documents\WiFiScanner\Saved_Scans\`
2. Delete the entire scan folder (e.g., `20251210_143045/`)
3. Refresh History tab in app

---

## 💾 Backup Recommendations

### Daily Users
- Enable OneDrive/Google Drive sync on `WiFiScanner` folder
- Automatic cloud backup

### Professional Use
- Weekly backup to external drive
- Archive old scans monthly
- Keep critical scans in separate "Important" folder

### Archive Strategy
```
WiFiScanner/
├── Saved_Scans/           # Recent scans (last 30 days)
└── Archive/
    ├── 2025_December/     # Older scans organized by month
    ├── 2025_November/
    └── ...
```

---

## 🔐 Privacy & Security

### Local Storage
- All data stored locally on your computer
- No cloud upload unless you enable it
- Full control over your data

### Sensitive Locations
If scanning sensitive areas:
1. Use strong Windows password
2. Enable BitLocker encryption
3. Regularly delete old scans
4. Consider encrypting the WiFiScanner folder

---

## 🛠️ Troubleshooting

### "Cannot find saved scans"
- Check: `C:\Users\{YourName}\Documents\WiFiScanner\Saved_Scans\`
- Generate a test heatmap to create the folder
- Verify you have write permissions to Documents folder

### "Migration failed"
- Old scans remain in: `app\resources\blueprint\heatmaps\`
- Manually copy folders to new location
- Rename to timestamp format: `YYYYMMDD_HHMMSS`

### "Folder access denied"
- Run app as administrator
- Check Documents folder permissions
- Try alternative location (see settings)

---

## 🚀 Future Enhancements

Coming soon:
- Custom save location in settings
- Auto-archive old scans
- Cloud sync integration
- Bulk export to ZIP
- Scan comparison across folders
- Search by date range or location

---

## 📞 Support

For questions or issues:
1. Check this guide
2. View console output for error messages
3. Check folder permissions
4. Verify disk space available

---

## 📝 Version History

- **v2.0** (Dec 10, 2025) - New organized save structure
- **v1.0** - Original app-embedded storage

---

**Happy Scanning! 📶**

