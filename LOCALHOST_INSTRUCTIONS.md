# 🚀 Lunar Loot - Localhost Setup Instructions

## Why Run Locally?

The **full real-time experience** of Lunar Loot requires direct webcam access that browser-based deployments cannot provide. Running locally gives you:

✅ **Real-time hand tracking** - Smooth 30+ FPS gameplay  
✅ **Instant response** - No photo-taking delays  
✅ **Full features** - All easter eggs and combos work perfectly  
✅ **Best performance** - Direct OpenCV camera access  

## Quick Start (5 minutes)

### 1. Clone the Repository
```bash
git clone https://github.com/gastondana627/lunar-loot.git
cd lunar-loot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Game
```bash
streamlit run catching_moonrocks_ultimate.py
```

### 4. Play!
- Open your browser to `http://localhost:8501`
- Allow camera access when prompted
- Enter your spacetag
- Start playing with real-time hand tracking!

## System Requirements

- **Python:** 3.9 or higher
- **Webcam:** Any USB or built-in camera
- **OS:** Windows, macOS, or Linux
- **RAM:** 4GB minimum (8GB recommended)

## Troubleshooting

### Camera Not Working?
- Make sure no other app is using your camera
- Grant camera permissions in your browser
- Try refreshing the page

### Slow Performance?
- Close other applications
- Ensure good lighting for better hand detection
- Lower video quality in browser settings if needed

### Import Errors?
```bash
pip install --upgrade -r requirements.txt
```

## What You'll Experience

### 🎮 Full Gameplay Features:
- **14 Unique Levels** - Progress through Mercury, Mars, Venus, and beyond
- **Real-time Hand Tracking** - Your hand controls the game instantly
- **Combo System** - Collect moonrocks quickly for multipliers
- **Easter Eggs** - Peace sign (+50 points), Thumbs up (+100 points)
- **Professional UI** - Space-themed backgrounds and animations
- **Progressive Difficulty** - More moonrocks and faster gameplay each level

### 🤖 AI Integration:
- **Google MediaPipe** - Real-time hand landmark detection
- **Freepik AI** - All visual assets and backgrounds
- **Adobe** - Image optimization and polish

## For Judges

This game showcases meaningful AI integration in an accessible format. The localhost version demonstrates the full technical achievement, while the cloud version serves as a preview.

**Demo Video:** [Link to your demo video]  
**GitHub:** https://github.com/gastondana627/lunar-loot  
**Cloud Preview:** https://lunar-loot.streamlit.app  

## Support

Having issues? Check the troubleshooting section or open an issue on GitHub.

---

**Built for Chroma Awards 2025** 🏆  
*Making gaming accessible through AI-powered hand tracking*
