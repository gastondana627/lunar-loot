# 🚀 Quick Start Guide

## Local Testing (2 minutes)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
streamlit run catching_moonrocks.py
```

Open http://localhost:8501 and grant camera permissions when prompted.

## Deploy to Streamlit Cloud (5 minutes)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Moonrock Collector game"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/moonrock-collector.git
git push -u origin main
```

### Step 2: Deploy
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Main file: `catching_moonrocks.py`
6. Click "Deploy"

### Step 3: Get Your URL
Your game will be live at: `https://YOUR-APP-NAME.streamlit.app`

## Submit to Chroma Awards

1. Copy your Streamlit Cloud URL
2. Go to Chroma Awards submission page
3. Category: **Experimental / Open**
4. Paste your URL
5. Add description (see CHROMA_SUBMISSION.md)
6. Submit!

## Troubleshooting

**Camera not working?**
- Grant camera permissions in browser
- Try Chrome or Firefox
- Check System Preferences > Security & Privacy > Camera

**App won't start?**
- Check all files are committed to GitHub
- Verify requirements.txt is present
- Check Streamlit Cloud logs for errors

**Hand tracking not detecting?**
- Ensure good lighting
- Keep hand in frame
- Try moving closer to camera
- Use index finger to point at moonrocks

## Next Steps

- [ ] Test game thoroughly
- [ ] Add Chroma Awards logo (download from competition site)
- [ ] Share on social media with #ChromaAwards
- [ ] Submit before deadline!

---

**Need help?** Check DEPLOYMENT.md and CHROMA_SUBMISSION.md for detailed guides.
