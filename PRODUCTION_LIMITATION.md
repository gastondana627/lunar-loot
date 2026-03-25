# Production Deployment Limitation

## ⚠️ Known Issue: Camera Access on Streamlit Cloud

### The Problem
The game currently uses OpenCV (`cv2.VideoCapture`) which runs **server-side**. This means:
- ❌ Cannot access browser cameras on Streamlit Cloud
- ❌ Browser camera permissions don't help (they're for client-side JavaScript)
- ❌ The architecture is fundamentally incompatible with cloud deployment

### Why This Happens
```
Current Architecture:
Browser → Streamlit Cloud Server → OpenCV tries to access server's camera (doesn't exist)

What's Needed:
Browser camera → WebRTC → Streamlit → Process frames
```

### The Solution: Run Locally

**The game works perfectly when run locally:**

```bash
git clone https://github.com/gastondana627/lunar-loot.git
cd lunar-loot  
pip install -r requirements.txt
streamlit run catching_moonrocks.py
```

Opens at `localhost:8501` with full camera access!

### For Competition Judges

- ✅ **Demo video** shows full gameplay
- ✅ **Local deployment** works flawlessly  
- ✅ **Source code** available for testing
- ⚠️ **Cloud deployment** has camera limitations (common for CV apps)

### Future Fix: WebRTC Implementation

To make this work on Streamlit Cloud requires:
1. Replacing `cv2.VideoCapture` with `streamlit-webrtc`
2. Refactoring game loop to use WebRTC callbacks
3. Adding STUN/TURN server configuration
4. Estimated time: 4-6 hours

This is planned for Version 2.0 (see `VERSION_2_ROADMAP.md`)

### Other CV Apps With Same Issue

This is a common limitation:
- Most Streamlit + OpenCV demos require local deployment
- WebRTC adds complexity but enables cloud deployment
- Trade-off between development speed and deployment flexibility

---

**Bottom Line:** The game is fully functional locally. Cloud deployment requires architectural changes that weren't feasible before the competition deadline.
