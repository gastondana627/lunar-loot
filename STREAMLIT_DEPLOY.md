# 🚀 Streamlit Cloud Deployment Guide

## Quick Deploy (5 minutes)

### Step 1: Go to Streamlit Cloud
Visit: https://share.streamlit.io

### Step 2: Sign In
- Click "Sign in" (top right)
- Use your GitHub account (gastondana627)

### Step 3: Deploy New App
1. Click "New app" button
2. Fill in the form:
   - **Repository:** `gastondana627/lunar-loot`
   - **Branch:** `main`
   - **Main file path:** `catching_moonrocks.py`
   - **App URL (optional):** `lunar-loot` (or leave blank for auto-generated)

3. Click "Deploy!"

### Step 4: Wait for Deployment
- First deployment takes 2-5 minutes
- You'll see build logs
- Wait for "Your app is live!" message

### Step 5: Get Your URL
Your app will be at one of these URLs:
- `https://lunar-loot.streamlit.app`
- `https://gastondana627-lunar-loot.streamlit.app`
- Or custom URL you chose

---

## Checking Existing Apps

### To see if you already have an app:
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Look at "Your apps" section
4. Search for "lunar-loot" or "moonrock"

### If App Already Exists:
- Click on it to view
- Click "Reboot" to restart with latest code
- Click "Settings" to change configuration

---

## Troubleshooting

### Camera Not Working?
- Streamlit Cloud uses HTTPS (required for webcam)
- Users must grant camera permissions
- Works best on Chrome/Firefox

### App Won't Start?
Check these files exist:
- ✅ `catching_moonrocks.py`
- ✅ `requirements.txt`
- ✅ `packages.txt`
- ✅ `backgrounds/New_Background_Rotation_1/` (with images)
- ✅ `animations/rocketship1.mp4`
- ✅ `moonrock.png`

### Slow Performance?
- First load is always slower (cold start)
- Subsequent loads are faster
- Hand tracking may be slower on cloud vs local

---

## After Deployment

### Test Your App:
1. Open the URL
2. Grant camera permissions
3. Enter a spacetag
4. Play through 1-2 levels
5. Check all features work

### Share Your App:
- Copy the URL
- Share on social media
- Submit to Chroma Awards

---

## Your Deployment URL

Once deployed, add it here:
```
https://_____________________.streamlit.app
```

---

**Ready to deploy? Go to https://share.streamlit.io now!**
