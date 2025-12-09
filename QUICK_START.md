# 🚀 WiFi Strength Scanner - Quick Reference

## Installation (One-time setup)
```powershell
pip install -r requirements.txt
```

## Run Application
```powershell
python main.py
```

## Usage (5 Steps)
1. **Click "Scan Blueprint"** button
2. **Click "Upload Blueprint"** → Select your floor plan image
3. **Click on the image** 10-15 times at different locations
4. **Click "Generate Heatmap"**
5. **Check `heatmaps/` folder** for results

## What Gets Saved
- `heatmap_YYYYMMDD_HHMMSS.png` - Visual heatmap
- `scan_data_YYYYMMDD_HHMMSS.json` - Raw data

## Color Meaning
🔴 **Red** = Strong signal (-30 to -50 dBm) - Excellent  
🟡 **Yellow** = Good signal (-50 to -60 dBm) - Very Good  
🟢 **Green** = Medium signal (-60 to -70 dBm) - Good  
🔵 **Blue** = Weak signal (-70 to -90 dBm) - Fair/Weak  
⚫ **Dark** = Very weak (-90 to -100 dBm) - Poor

## Tips
- ✅ Scan 15-20 points for best results
- ✅ Include corners and edges
- ✅ Distribute points evenly
- ✅ Stay at same height while scanning
- ✅ Use high-resolution blueprints

## Troubleshooting
**No WiFi detected?**
→ Connect to WiFi first, run as Administrator

**Weird heatmap?**
→ Scan more points, distribute evenly

**Can't find output?**
→ Look in same folder as blueprint in `heatmaps/` subfolder

## Test Core Functionality
```powershell
python test_core.py
```

## Customize Settings
Edit `config.py`:
- `DEFAULT_GRID_SIZE` - Grid resolution (default: 100)
- `DEFAULT_IDW_POWER` - Smoothing (default: 2)  
- `DEFAULT_BLEND_ALPHA` - Transparency (default: 0.6)

## Files You'll Use
- `main.py` - Start application
- `test_core.py` - Test without GUI
- `config.py` - Settings
- `README.md` - Full documentation
- `GUIDE.md` - Detailed instructions
- `FIXES_APPLIED.md` - What was fixed

---

**Made by**: Saqlain • Farhan • Tamim • Govt  
**Platform**: Windows 10/11  
**Python**: 3.8+

