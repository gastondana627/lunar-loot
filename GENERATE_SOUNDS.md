# 🎙️ Generate All Sound Effects

## Quick Start

### Option 1: Using ElevenLabs API (Recommended)

1. **Set your API key:**
   ```bash
   export ELEVENLABS_API_KEY="your_api_key_here"
   ```

2. **Run the generation script:**
   ```bash
   python elevenlabs_setup.py
   ```

3. **Wait 5-10 minutes** for all 23 sounds to generate

4. **Verify files:**
   ```bash
   ls -la sounds/
   ```

### Option 2: Using ElevenLabs Website (Manual)

1. Go to [elevenlabs.io/speech-synthesis](https://elevenlabs.io/speech-synthesis)
2. Select voice: **Rachel** (recommended)
3. Copy each prompt below, generate, and download
4. Save files to `sounds/` directory with exact names

---

## All 23 Sound Prompts

### Level Announcements (14 files)

| File Name | Prompt |
|-----------|--------|
| `level_01_earth.mp3` | Level one! Welcome to Earth orbit. Let's collect some moonrocks! |
| `level_02_halley.mp3` | Level two! Halley's Comet approaches. Watch out for the cosmic debris! |
| `level_03_mars.mp3` | Level three! The red planet Mars. Time to explore the rusty surface! |
| `level_04_mercury.mp3` | Level four! Mercury's scorching surface. Stay cool and collect those rocks! |
| `level_05_moon.mp3` | Level five! Our Moon! One small step for you, one giant leap for your score! |
| `level_06_oumuamua.mp3` | Level six! The mysterious Oumuamua. An interstellar visitor from beyond! |
| `level_07_planetx.mp3` | Level seven! The legendary Planet X. Venture into the unknown! |
| `level_08_saturn.mp3` | Level eight! Saturn and its beautiful rings. Navigate the cosmic jewelry! |
| `level_09_spaceship.mp3` | Level nine! Aboard the spaceship. Collect moonrocks in zero gravity! |
| `level_10_uranus.mp3` | Level ten! Uranus, the sideways planet. Almost there, keep going! |
| `level_11_venus.mp3` | Level eleven! Venus, the morning star. Final level, give it your all! |
| `level_12_atlas.mp3` | Level twelve! Comet 3I/ATLAS, an interstellar wanderer. Chase the cosmic visitor! |
| `level_13_ceres.mp3` | Level thirteen! Ceres, queen of the asteroid belt. Navigate the rocky realm! |
| `level_14_makemake.mp3` | Level fourteen! Makemake, the distant dwarf planet. Journey to the edge of our solar system! |

### Game Events (9 files)

| File Name | Prompt |
|-----------|--------|
| `welcome.mp3` | Welcome to Lunar Loot! Use your hand to collect the moonrocks. Good luck! |
| `collect_1.mp3` | Collected! |
| `collect_2.mp3` | Nice catch! |
| `collect_3.mp3` | Got it! |
| `level_complete.mp3` | Level complete! Excellent work! Get ready for the next challenge! |
| `time_warning_10.mp3` | Ten seconds remaining! Hurry! |
| `time_warning_5.mp3` | Five seconds left! |
| `game_over.mp3` | Game over! Thanks for playing Lunar Loot! |
| `high_score.mp3` | New high score! You're a moonrock master! |
| `countdown.mp3` | Three, two, one, go! |

---

## Current Status

✅ **Sound system integrated** - Game will use fallback sounds until ElevenLabs files are generated
✅ **23 sound effects defined** - All prompts ready in elevenlabs_setup.py
⏳ **Waiting for generation** - Run the script above to create custom AI voices

---

## Testing Sounds

After generating, test a sound file:
```bash
# macOS
afplay sounds/collect_1.mp3

# Linux
aplay sounds/collect_1.mp3

# Or open in browser
open sounds/collect_1.mp3
```

---

## Notes

- **Voice**: Rachel (clear, friendly, energetic)
- **Model**: eleven_monolingual_v1
- **Total files**: 23 MP3 files
- **Estimated size**: ~2-3 MB total
- **Fallback**: Game uses free online sounds if files don't exist
- **Deployment**: Upload `sounds/` folder to Streamlit Cloud

---

## Troubleshooting

**"No API key found"**
- Set environment variable: `export ELEVENLABS_API_KEY="sk_..."`
- Or edit elevenlabs_setup.py and add key directly

**"Module not found: elevenlabs"**
- Install: `pip install elevenlabs`

**"Sounds not playing in game"**
- Check files exist: `ls sounds/`
- Check file names match exactly (case-sensitive)
- Browser may block autoplay - check console for errors

---

Ready to generate? Run: `python elevenlabs_setup.py`
