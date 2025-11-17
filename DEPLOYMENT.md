# Deployment Guide - Streamlit Cloud

## Quick Deploy to Streamlit Cloud (5 minutes)

### Prerequisites
1. GitHub account
2. Streamlit Cloud account (free at share.streamlit.io)

### Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Moonrock Collector game"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your GitHub repository
   - Main file: `catching_moonrocks.py`
   - Click "Deploy"

3. **Add ElevenLabs API Key (Optional)**
   - In Streamlit Cloud dashboard, go to app settings
   - Add secret: `ELEVENLABS_API_KEY = "your_api_key_here"`
   - This enables AI-generated sound effects

4. **Share Your Link**
   - Your app will be at: `https://YOUR_APP_NAME.streamlit.app`
   - Use this link for Chroma Awards submission

## Troubleshooting

### Camera Access Issues
- Streamlit Cloud apps require HTTPS (automatically provided)
- Users must grant camera permissions in browser
- Works best on Chrome and Firefox

### Performance
- First load may take 30-60 seconds (cold start)
- Subsequent loads are faster
- Hand tracking requires good lighting

## Competition Submission Checklist

- [ ] App deployed and accessible via browser
- [ ] No download required
- [ ] No login required
- [ ] Game completable in under 30 minutes
- [ ] README mentions Chroma Awards
- [ ] AI tools listed in description
- [ ] Single player mode available
- [ ] Created after February 1, 2025

## Alternative: Vercel Deployment

Note: Streamlit apps don't deploy directly to Vercel. Vercel is for static sites and serverless functions. Stick with Streamlit Cloud for this Python app.
