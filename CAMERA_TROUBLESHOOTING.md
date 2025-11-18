# 📷 Camera Access Troubleshooting Guide

## For Players Having Camera Issues

If you see "Camera access required" message, follow these steps:

---

## ✅ Quick Fix (Most Common)

### Chrome / Brave / Edge:
1. Look for the **camera icon** 🎥 or **lock icon** 🔒 in the address bar (left side)
2. Click it
3. Find "Camera" and change to **"Allow"**
4. **Refresh the page** (F5 or Cmd+R)

### Safari:
1. Go to **Safari menu** → **Settings** → **Websites**
2. Click **"Camera"** in the left sidebar
3. Find the Streamlit app URL
4. Change dropdown to **"Allow"**
5. **Refresh the page**

### Firefox:
1. Click the **camera icon** in the address bar
2. Select **"Allow"**
3. **Refresh the page**

---

## 🔍 Still Not Working?

### Check System Permissions (Mac):
1. **System Settings** → **Privacy & Security** → **Camera**
2. Make sure your browser (Chrome/Safari/Firefox) is **checked**
3. Restart your browser

### Check System Permissions (Windows):
1. **Settings** → **Privacy** → **Camera**
2. Make sure "Allow apps to access your camera" is **ON**
3. Make sure your browser is allowed
4. Restart your browser

---

## 🚨 Reset Site Permissions

If camera was previously blocked:

### Chrome:
1. Go to: `chrome://settings/content/camera`
2. Look in the **"Block"** section
3. Find the Streamlit URL and click the **trash icon**
4. Revisit the game - it will ask for permission again

### Safari:
1. Safari → Settings → Websites → Camera
2. Remove the Streamlit URL from the list
3. Revisit the game

### Firefox:
1. Click the lock icon in address bar
2. Click "Clear cookies and site data"
3. Revisit the game

---

## 💡 Pro Tips

### Test Your Camera First:
Visit **webcamtest.com** to verify your camera works in your browser

### Use Chrome:
Chrome has the best WebRTC support for camera access

### Desktop Only:
This game requires a desktop/laptop with webcam - mobile is not supported

### Privacy Note:
All hand tracking happens in your browser. No video is recorded or transmitted to any server.

---

## 🎮 Alternative: Run Locally

If browser permissions are still problematic:

1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Run: `streamlit run catching_moonrocks.py`
4. Open: `http://localhost:8501`
5. Camera permissions work better on localhost!

---

## 📧 Still Having Issues?

If none of these work:
- Check if another app is using your camera (Zoom, Teams, etc.)
- Try a different browser
- Restart your computer
- Check if your camera has a physical privacy shutter

---

**Created for Chroma Awards 2025**  
**Lunar Loot - AI Hand Tracking Game**
