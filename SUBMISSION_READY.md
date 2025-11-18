# Lunar Loot - Submission Ready

## ✅ What's Working

### Core Gameplay
- ✅ Hand tracking with MediaPipe
- ✅ Moonrock collection mechanics
- ✅ Level progression (1-10+)
- ✅ Score system with combo multipliers
- ✅ Time-based challenges (30 seconds per level)
- ✅ Retry failed levels
- ✅ Leaderboard system

### UI/UX
- ✅ Professional space-themed design
- ✅ Custom logo and branding
- ✅ Responsive HUD with real-time stats
- ✅ Dynamic backgrounds per level
- ✅ Spacetag (username) system
- ✅ Mission snapshot (selfie) feature
- ✅ Chroma Awards footer integration

### Technical
- ✅ Camera initialization and error handling
- ✅ Session state management
- ✅ Memory optimizations for deployment
- ✅ Browser compatibility checks
- ✅ Mobile detection with warning

## ⚠️ Known Limitations

### Audio
- ❌ Real-time sound effects don't work (Streamlit limitation with game loops)
- ❌ Background music doesn't autoplay (browser restrictions)
- **Reason:** Streamlit's `while True` loop blocks HTML rendering
- **Impact:** Game is fully playable, just silent

### Workarounds Attempted
- HTML5 audio tags
- JavaScript Audio API
- Web Audio API beeps
- components.html() approach
- **Result:** None work reliably in Streamlit's game loop architecture

## 📦 Submission Package

### Files to Include
```
catching_moonrocks.py          # Main game file
enhanced_features.py           # Leaderboard & selfie features
requirements.txt               # Dependencies
moonrock.png                   # Game asset
backgrounds/                   # Space backgrounds (14 images)
ui_assets/branding/           # Logo
README.md                      # Project documentation
```

### Dependencies
```
streamlit==1.42.2
opencv-python==4.10.0.84
mediapipe==0.10.14
numpy==1.26.4
Pillow==10.4.0
```

## 🎯 Submission Highlights

### AI Tools Used
1. **Google MediaPipe** - Real-time hand tracking and gesture recognition
2. **Freepik AI** - Space-themed backgrounds and UI assets
3. **ElevenLabs** - Audio generation (files included, playback limited by Streamlit)

### Innovation
- Real-time hand gesture control in browser
- No controllers needed - just your hand
- Progressive difficulty with combo system
- Space exploration theme with dynamic backgrounds

### Technical Achievement
- Overcame Streamlit's limitations for real-time video processing
- Implemented efficient game loop with camera handling
- Memory-optimized for cloud deployment
- Professional UI/UX design

## 🚀 Deployment

### Streamlit Cloud
- App URL: [Your deployed URL]
- Status: Ready for deployment
- Requirements: Webcam access required

### Local Testing
```bash
streamlit run catching_moonrocks.py
```

## 📝 Submission Notes

**What to mention in submission:**
1. Game is fully functional with hand tracking
2. Audio was attempted but Streamlit's architecture doesn't support real-time game audio
3. Focus on innovative hand gesture controls and professional design
4. All AI tools properly credited (MediaPipe, Freepik, ElevenLabs)

**Strengths to highlight:**
- Unique hand-tracking gameplay
- No external controllers needed
- Professional space-themed design
- Progressive difficulty system
- Leaderboard and social features

## 🎮 How to Play

1. **Grant camera access** when prompted
2. **Enter your Spacetag** (pilot name)
3. **Show your hand** to the camera
4. **Point with index finger** to touch moonrocks
5. **Collect all rocks** before time runs out
6. **Progress through levels** with new backgrounds

## 🏆 Scoring

- **Base points:** 10 per moonrock
- **Combo bonus:** +5 points per combo level
- **Time bonus:** 2 points per second remaining
- **High score:** Saved to leaderboard

## ✨ Final Status

**Game is submission-ready!** 

The core experience is complete and polished. Audio would be a nice addition but isn't critical to gameplay. The hand tracking innovation and professional execution are the main highlights.

---

**Created for Chroma Awards 2025**
**AI Tools: Google MediaPipe, ElevenLabs, Freepik**
