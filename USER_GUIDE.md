# Quick User Guide - New Features

## Speed Test Improvements

### How to Use Speed Test

1. Navigate to **Speed Test** tab
2. (Optional) Check **"Run 3 tests and average"** for more consistent results
3. Click **"Start Speed Test"**
4. Wait for results (shows progress messages)
5. If test gets stuck, click **"Cancel"** button

### Multi-Test Mode Benefits
- Runs 3 consecutive tests
- Averages the results
- Provides more stable measurements
- Reduces impact of network fluctuations

---

## Editing Scan Points

### Edit a Marker's RSSI Value

1. **Left-click** on any red marker circle
2. Edit dialog appears showing current position and RSSI
3. Choose your action:
   - **Auto-scan WiFi**: Re-scan at that location
   - **Manual Input**: Enter new RSSI value
4. Click **OK** to save changes

### What Gets Updated
- Visual marker on blueprint
- Stored scan data
- Status panel information

---

## Deleting Scan Points

### Delete a Marker

**Method 1: Right-Click Context Menu**
1. **Right-click** on any red marker circle
2. Context menu appears showing:
   - Marker position
   - Current RSSI value
3. Click **"Delete Marker"**
4. Confirm deletion in dialog
5. Marker removed from blueprint and data

**Method 2: Edit and Clear**
1. Left-click marker
2. Cancel dialog (removes invalid markers)

### Confirmation Safety
- Always asks for confirmation before deletion
- Shows what will be deleted (position + RSSI)
- Success notification after deletion

---

## Tips and Best Practices

### Speed Test
- Use multi-test mode for important measurements
- Cancel and retry if stuck for >30 seconds
- Ensure stable internet connection before testing
- Run at different times for comprehensive data

### Scan Point Management
- Review markers before generating heatmap
- Edit outliers or suspicious readings
- Delete accidental clicks
- Use right-click for quick deletion
- Use left-click for editing values

### General Workflow
1. Upload blueprint
2. Click to add scan points
3. Edit any mistakes immediately
4. Right-click to delete unwanted points
5. Generate heatmap when satisfied
6. Check History tab for previous scans

---

## Keyboard Shortcuts

- **Left-Click**: Add new scan point OR edit existing marker
- **Right-Click**: Show marker context menu (Edit/Delete)
- **ESC**: Cancel dialog

---

## Troubleshooting

### Speed Test Stuck
- **Solution**: Click "Cancel" button and retry
- **Prevention**: Use multi-test mode for reliability

### Can't Delete Marker
- **Check**: Right-click directly on the red circle
- **Alternative**: Left-click and cancel dialog

### Edit Dialog Not Showing
- **Check**: Click directly on existing red marker
- **Note**: Clicking empty space creates new marker

### Marker Not Updating
- **Verify**: Check status panel for confirmation
- **Check**: Look for RSSI number near marker

---

## Feature Status

✅ **Speed Test**: Working with cancel and multi-test
✅ **Marker Editing**: Left-click to edit
✅ **Marker Deletion**: Right-click context menu
✅ **Grid System**: Removed (pixel-based now)

---

## Support

For issues or questions:
1. Check console output for error messages
2. Review status text panel for last action
3. Check TEST_CHECKLIST.md for known issues
4. See FEATURES_SUMMARY.md for detailed documentation

