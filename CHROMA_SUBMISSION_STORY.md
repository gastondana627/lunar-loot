# Lunar Loot - Chroma Awards 2025 Submission

## Elevator Pitch
**"Catch falling moon rocks with your bare hands using AI-powered gesture control - no controller needed!"**

---

## Inspiration

The idea for Lunar Loot came from a simple question: *What if your hands could be the controller?* 

I've always been fascinated by how AI is breaking down barriers between humans and technology. Traditional gaming requires expensive controllers, keyboards, or touchscreens - but what if we could make gaming more accessible and intuitive using just our natural gestures?

When I discovered Google MediaPipe's hand tracking capabilities, I saw an opportunity to create something genuinely innovative: a game where the barrier to entry is literally just having hands and a webcam. No downloads, no controllers, no learning curve - just wave and play.

The space theme was inspired by the wonder of exploration. Just as astronauts reach out to collect samples from distant worlds, players reach out through their webcam to catch moon rocks from across the solar system.

---

## What It Does

**Lunar Loot** is a browser-based arcade game where players catch falling moon rocks using real-time hand tracking - no physical controller required.

### Core Gameplay:
- **Hand Tracking**: Your hand position controls an on-screen basket in real-time
- **Progressive Difficulty**: 14 unique levels across different celestial locations (Earth orbit, Mars, Saturn's rings, etc.)
- **Dynamic Scoring**: Catch moon rocks for points, avoid space debris that costs you points
- **Easter Eggs**: Hidden gesture bonuses (peace sign ✌️ = +50 points, thumbs up 👍 = +100 points)
- **Leaderboard System**: Track high scores with automatic snapshots
- **Professional UI**: Title screen, about page, and polished space-themed interface

### Technical Innovation:
The game runs entirely in the browser using Streamlit and processes hand tracking at 30+ FPS with minimal latency. Players can literally start playing within seconds of opening the link.

---

## How We Built It

### AI Tools & Technologies:

1. **Google MediaPipe (Core Innovation - 50%)**
   - Real-time hand landmark detection (21 points per hand)
   - Gesture recognition for easter eggs (peace sign, thumbs up)
   - Optimized for browser-based performance
   - Custom calibration system for different hand sizes

2. **Freepik AI (Visual Design - 30%)**
   - Generated 14 unique space-themed backgrounds
   - Created professional logo and branding assets
   - Designed UI elements (buttons, icons)
   - Maintained consistent aesthetic across all levels

3. **Adobe (Polish & Production - 20%)**
   - Image editing and optimization
   - Asset refinement and color correction
   - Final production polish

### Development Stack:
- **Python 3.9+** - Core game logic
- **Streamlit** - Web framework for instant deployment
- **OpenCV** - Video processing and rendering
- **MediaPipe** - Hand tracking AI
- **NumPy** - Game physics and calculations
- **Pillow** - Image processing

### Architecture:
```
User Webcam → MediaPipe AI → Hand Coordinates → Game Logic → Visual Feedback
     ↓                                                              ↓
  Privacy-First                                            Browser Rendering
  (No Recording)                                          (Real-time 30 FPS)
```

### Development Process:
1. **Prototype** (Week 1): Basic hand tracking + falling objects
2. **Game Mechanics** (Week 2): Scoring, levels, difficulty progression
3. **AI Integration** (Week 3): Gesture recognition, easter eggs
4. **UI/UX Polish** (Week 4): Professional interface, branding, deployment

---

## Challenges We Ran Into

### 1. **Real-Time Performance**
**Problem**: Hand tracking + game rendering + video processing = potential lag  
**Solution**: Optimized MediaPipe settings, reduced video resolution strategically, implemented frame skipping for non-critical updates

### 2. **Gesture Recognition Reliability**
**Problem**: Initial heart gesture (❤️) had <30% accuracy - too frustrating  
**Solution**: Switched to more distinct gestures (peace sign, thumbs up) with custom detection algorithms and cooldown timers to prevent false positives

### 3. **Cross-Device Compatibility**
**Problem**: Different webcams, lighting conditions, and hand sizes  
**Solution**: Built adaptive calibration system that normalizes hand coordinates and adjusts sensitivity based on detection confidence

### 4. **Streamlit Audio Limitations**
**Problem**: Streamlit's architecture doesn't support traditional game audio loops  
**Solution**: Implemented web-based background music via URL streaming, documented limitations transparently

### 5. **User Experience Flow**
**Problem**: Players jumping straight into gameplay without understanding controls  
**Solution**: Created comprehensive title screen with "About" page explaining mechanics, controls, and AI tools used

### 6. **Deployment & Privacy**
**Problem**: Users concerned about webcam access  
**Solution**: All processing happens client-side in browser, no video recording or transmission, clear privacy messaging

---

## Accomplishments That We're Proud Of

✨ **Zero Barrier to Entry**: No installation, no controllers, no learning curve - just open and play

🎯 **Smooth Performance**: Achieved 30+ FPS hand tracking with <100ms latency on standard hardware

🎮 **Genuine Innovation**: Created a new way to play games that feels natural and accessible

🎨 **Professional Polish**: From title screen to easter eggs, every detail was crafted for quality

🤖 **Meaningful AI Integration**: MediaPipe isn't just a gimmick - it's the core innovation that makes the game possible

📊 **Complete Game Loop**: Leaderboards, snapshots, 14 levels, progressive difficulty - it's a full experience

🔒 **Privacy-First**: All processing happens locally, no data collection or recording

---

## What We Learned

### Technical Insights:
- **AI Performance Optimization**: Learned to balance accuracy vs. speed in real-time ML applications
- **Gesture Recognition**: Understanding the difference between "technically detectable" and "reliably playable" gestures
- **Browser-Based ML**: How to deploy sophisticated AI models in web environments without sacrificing UX

### Design Lessons:
- **Accessibility Through AI**: How AI can remove barriers rather than create complexity
- **Feedback Loops**: The importance of immediate visual feedback when using gesture controls
- **Progressive Disclosure**: Teaching mechanics through gameplay rather than lengthy tutorials

### Product Development:
- **Scope Management**: Focusing on core innovation (hand tracking) rather than feature bloat
- **User Testing**: Real users revealed issues (like unreliable gestures) that seemed fine in testing
- **Documentation**: Clear communication about AI tools used is crucial for competition submissions

---

## What's Next for Lunar Loot

### Version 2.0 Roadmap:

**Multiplayer Mode**
- Two-player split-screen with dual hand tracking
- Competitive and cooperative modes

**Advanced Gestures**
- Power-ups activated by specific hand poses
- Combo system for chaining gestures

**Mobile Support**
- Touch controls as fallback
- Mobile-optimized UI

**Accessibility Features**
- One-handed mode
- Adjustable difficulty settings
- Colorblind-friendly palettes

**Enhanced AI**
- Predictive difficulty adjustment based on player skill
- Personalized level recommendations
- AI-generated custom levels

**Community Features**
- Global leaderboards
- Replay sharing
- Custom challenge modes

---

## Built With

### Languages & Frameworks:
- Python 3.9+
- Streamlit (Web Framework)
- HTML/CSS (Custom UI Components)

### AI & Machine Learning:
- Google MediaPipe (Hand Tracking)
- OpenCV (Computer Vision)
- NumPy (Numerical Computing)

### Design & Assets:
- Freepik AI (Visual Generation)
- Adobe (Editing & Polish)
- Pillow (Image Processing)

### Deployment:
- Streamlit Cloud
- GitHub (Version Control)

### Key Libraries:
```
streamlit==1.32.0
opencv-python==4.9.0.80
mediapipe==0.10.11
numpy==1.26.4
Pillow==10.2.0
```

---

## Try It Out Links

**Live Demo**: [Your Streamlit Cloud URL]  
**Source Code**: [Your GitHub Repository URL]  
**Demo Video**: [Optional - YouTube/Loom link]

---

## Project Media Notes

### Image Gallery Requirements:
- **Format**: JPG, PNG, or GIF
- **Max Size**: 5 MB per file
- **Recommended Ratio**: 3:2 (e.g., 1200x800px, 1800x1200px)

### Suggested Screenshots:
1. **Title Screen** - Show professional branding and AI credits
2. **Gameplay** - Hand tracking in action with visible basket and moon rocks
3. **Easter Egg** - Peace sign or thumbs up gesture with score popup
4. **Level Variety** - Different backgrounds (Mars, Saturn, Moon)
5. **Leaderboard** - High scores with snapshot feature
6. **About Page** - Showing AI tools and game information

### Adobe Resize Instructions:
1. Open your screenshot in Adobe Photoshop or Photoshop Express
2. Go to **Image → Image Size**
3. Set dimensions to 3:2 ratio:
   - Width: 1800px, Height: 1200px (high quality)
   - OR Width: 1200px, Height: 800px (standard)
4. Ensure "Constrain Proportions" is checked
5. Choose "Bicubic Sharper" for reduction
6. Save as JPG with quality 80-90%

**Quick 3:2 Ratios:**
- 3000 x 2000 (ultra high-res)
- 1800 x 1200 (recommended)
- 1200 x 800 (standard)
- 900 x 600 (minimum)

---

**Created for Chroma Awards 2025**  
**Category**: Presenting Sponsor Track  
**AI Sponsors**: Google MediaPipe, Freepik, Adobe
