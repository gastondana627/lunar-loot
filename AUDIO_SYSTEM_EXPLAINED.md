# 🔊 Audio System - Complete Explanation

## Two Types of Audio

### 1. 🎵 Sound Effects (Always Available)
**What:** Short beeps, clicks, and game sounds  
**Source:** Free online sound effects from Mixkit  
**Status:** ✅ Working now (no generation needed)  
**Used for:**
- Collecting moonrocks (3 variations)
- Level complete notification
- Time warnings (10s, 5s)
- Game over
- High score achievement

**How it works:**
```javascript
// Browser plays sound from URL
<audio autoplay>
  <source src="https://assets.mixkit.co/.../sound.mp3">
</audio>
```

---

### 2. 🎙️ AI Voice Announcements (Optional Enhancement)
**What:** Human-like voice saying level names and instructions  
**Source:** ElevenLabs AI voice generation  
**Status:** ⏳ Not generated yet (optional upgrade)  
**Used for:**
- Level announcements: "Level one! Welcome to Earth orbit..."
- Welcome message: "Welcome to Lunar Loot! Use your hand..."
- Encouragement: "Nice catch!", "Got it!"

**How it works:**
```python
# If you generate with ElevenLabs:
python elevenlabs_setup.py

# Creates files like:
sounds/level_01_earth.mp3  # "Level one! Welcome to Earth orbit..."
sounds/collect_1.mp3       # "Collected!"
sounds/welcome.mp3         # "Welcome to Lunar Loot..."
```

---

## Current Audio Status

| Sound Type | Status | Source |
|------------|--------|--------|
| Moonrock collection | ✅ Working | Mixkit (free) |
| Level complete | ✅ Working | Mixkit (free) |
| Time warnings | ✅ Working | Mixkit (free) |
| Game over | ✅ Working | Mixkit (free) |
| High score | ✅ Working | Mixkit (free) |
| **AI Voice Announcements** | ⏳ Optional | ElevenLabs (needs generation) |

---

## Why You Might Not Hear Sounds

### 1. Browser Autoplay Policy
Modern browsers block autoplay audio until user interacts with page.

**Solution:** Click anywhere on the page first, then sounds will work.

### 2. Browser Console Errors
Check browser console (F12) for errors like:
```
"The play() request was interrupted by a call to pause()"
"Autoplay policy prevented playback"
```

**Solution:** Sounds will work after first user interaction (clicking "Launch Mission").

### 3. Volume/Mute
Check system volume and browser tab isn't muted.

---

## Testing Sounds

### Test in Browser Console
```javascript
// Open browser console (F12) and run:
var audio = new Audio('https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3');
audio.play();
```

If this works, the sound system is fine - just needs user interaction first.

---

## Adding AI Voice Announcements (Optional)

### Step 1: Get ElevenLabs API Key
1. Sign up at [elevenlabs.io](https://elevenlabs.io)
2. Get free API key (10,000 characters/month free)
3. Copy your API key

### Step 2: Generate Voice Files
```bash
# Set API key
export ELEVENLABS_API_KEY="sk_your_key_here"

# Generate all 23 voice files
python elevenlabs_setup.py

# Wait 5-10 minutes
# Creates sounds/*.mp3 files
```

### Step 3: Test Generated Files
```bash
# Play a generated file
afplay sounds/level_01_earth.mp3  # macOS
# or
aplay sounds/level_01_earth.mp3   # Linux
```

### Step 4: Deploy
Upload the `sounds/` folder to your repository, and the game will automatically use AI voices instead of beeps!

---

## What Gets Generated

### 14 Level Announcements
```
sounds/level_01_earth.mp3      → "Level one! Welcome to Earth orbit..."
sounds/level_02_halley.mp3     → "Level two! Halley's Comet approaches..."
sounds/level_03_mars.mp3       → "Level three! The red planet Mars..."
... (11 more)
```

### 9 Game Event Voices
```
sounds/welcome.mp3             → "Welcome to Lunar Loot! Use your hand..."
sounds/collect_1.mp3           → "Collected!"
sounds/collect_2.mp3           → "Nice catch!"
sounds/collect_3.mp3           → "Got it!"
sounds/level_complete.mp3      → "Level complete! Excellent work!"
sounds/time_warning_10.mp3     → "Ten seconds remaining! Hurry!"
sounds/time_warning_5.mp3      → "Five seconds left!"
sounds/game_over.mp3           → "Game over! Thanks for playing..."
sounds/high_score.mp3          → "New high score! You're a moonrock master!"
sounds/countdown.mp3           → "Three, two, one, go!"
```

---

## Current vs Enhanced Audio

### Current (Free Sound Effects)
```
Collect moonrock → *beep*
Level complete → *success chime*
Time warning → *alert beep*
```

### With AI Voices (After Generation)
```
Collect moonrock → "Collected!" (human voice)
Level complete → "Level complete! Excellent work!" (human voice)
Level start → "Level one! Welcome to Earth orbit!" (human voice)
```

---

## Summary

✅ **Sound effects work NOW** - No generation needed  
⏳ **AI voices are OPTIONAL** - Enhance the experience  
🎮 **Game is fully playable** - With or without AI voices  
🎙️ **To add AI voices** - Run `python elevenlabs_setup.py`

---

## Troubleshooting

**"I don't hear any sounds"**
1. Click anywhere on the page first (browser autoplay policy)
2. Check browser console for errors (F12)
3. Verify volume isn't muted
4. Try in Chrome (best browser support)

**"Sounds are delayed"**
- Normal for first sound (browser loading)
- Subsequent sounds should be instant

**"Want AI voices but don't have API key"**
- Game works fine with sound effects only
- AI voices are a nice-to-have enhancement
- Can add them later without affecting gameplay

---

Ready to test? Refresh the page and click "Launch Mission" - you should hear sounds when collecting moonrocks! 🎵
