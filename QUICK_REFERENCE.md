# 🚀 Quick Reference - Copy & Paste Ready

## ElevenLabs Audio Generation (20 Files)

### Option 1: Use Python Script (FASTEST)
```bash
export ELEVENLABS_API_KEY="your_key_here"
python elevenlabs_setup.py
```
This generates all 20 files automatically in 5-10 minutes.

---

### Option 2: Use ElevenLabs Website (Manual)

Go to: https://elevenlabs.io/speech-synthesis

**Settings:**
- Voice: Rachel
- Model: Eleven Monolingual v1
- Stability: 50%
- Clarity: 75%

**Copy each prompt, generate, download, rename:**

#### Level Announcements (11 files):

1. **level_01_earth.mp3**
   ```
   Level one! Welcome to Earth orbit. Let's collect some moonrocks!
   ```

2. **level_02_halley.mp3**
   ```
   Level two! Halley's Comet approaches. Watch out for the cosmic debris!
   ```

3. **level_03_mars.mp3**
   ```
   Level three! The red planet Mars. Time to explore the rusty surface!
   ```

4. **level_04_mercury.mp3**
   ```
   Level four! Mercury's scorching surface. Stay cool and collect those rocks!
   ```

5. **level_05_moon.mp3**
   ```
   Level five! Our Moon! One small step for you, one giant leap for your score!
   ```

6. **level_06_oumuamua.mp3**
   ```
   Level six! The mysterious Oumuamua. An interstellar visitor from beyond!
   ```

7. **level_07_planetx.mp3**
   ```
   Level seven! The legendary Planet X. Venture into the unknown!
   ```

8. **level_08_saturn.mp3**
   ```
   Level eight! Saturn and its beautiful rings. Navigate the cosmic jewelry!
   ```

9. **level_09_spaceship.mp3**
   ```
   Level nine! Aboard the spaceship. Collect moonrocks in zero gravity!
   ```

10. **level_10_uranus.mp3**
    ```
    Level ten! Uranus, the sideways planet. Almost there, keep going!
    ```

11. **level_11_venus.mp3**
    ```
    Level eleven! Venus, the morning star. Final level, give it your all!
    ```

---

#### Game Events (9 files):

12. **welcome.mp3**
    ```
    Welcome to Moonrock Collector! Use your hand to collect the moonrocks. Good luck!
    ```

13. **collect_1.mp3**
    ```
    Collected!
    ```

14. **collect_2.mp3**
    ```
    Nice catch!
    ```

15. **collect_3.mp3**
    ```
    Got it!
    ```

16. **level_complete.mp3**
    ```
    Level complete! Excellent work! Get ready for the next challenge!
    ```

17. **time_warning_10.mp3**
    ```
    Ten seconds remaining! Hurry!
    ```

18. **time_warning_5.mp3**
    ```
    Five seconds left!
    ```

19. **game_over.mp3**
    ```
    Game over! Thanks for playing Moonrock Collector!
    ```

20. **high_score.mp3**
    ```
    New high score! You're a moonrock master!
    ```

---

## File Organization

Save all files to:
```
/Users/gastondana/Desktop/2025 CodeSignal/Computer Vision Moonrock Game/sounds/
```

Create the directory if it doesn't exist:
```bash
mkdir -p sounds
```

---

## Background Image Mapping

| Level | Background File | Audio File |
|-------|----------------|------------|
| 1 | Earth.jpg | level_01_earth.mp3 |
| 2 | Halleys Comet.jpg | level_02_halley.mp3 |
| 3 | Mars.jpg | level_03_mars.mp3 |
| 4 | Mercury.jpg | level_04_mercury.mp3 |
| 5 | Moon.jpg | level_05_moon.mp3 |
| 6 | Oumuamua.jpg | level_06_oumuamua.mp3 |
| 7 | Planet X.jpg | level_07_planetx.mp3 |
| 8 | Saturn.jpg | level_08_saturn.mp3 |
| 9 | SpaceShip.jpg | level_09_spaceship.mp3 |
| 10 | Uranus.jpg | level_10_uranus.mp3 |
| 11 | Venus.jpg | level_11_venus.mp3 |

---

## Testing Checklist

After generating all files:

```bash
# Check all files exist
ls -la sounds/

# Should see 20 .mp3 files
# Total size should be ~2-5 MB

# Test playing a file (macOS)
afplay sounds/welcome.mp3
```

---

## Integration Steps (After Audio is Ready)

1. ✅ Generate all 20 audio files
2. ⏳ Save to `sounds/` directory
3. ⏳ Run: `python game_audio.py` to test loading
4. ⏳ Update catching_moonrocks.py to use audio
5. ⏳ Test locally
6. ⏳ Deploy to Streamlit Cloud

---

## Time Estimates

- **API Method**: 5-10 minutes total
- **Web Method**: 15-20 minutes total
- **Integration**: 20-30 minutes
- **Testing**: 10-15 minutes
- **Total**: 45-75 minutes

---

## Pro Tips

1. **Generate in batches**: Do all level announcements first, then game events
2. **Use same voice**: Consistency is key (Rachel recommended)
3. **Test as you go**: Play each file after generating to catch issues early
4. **Keep originals**: Save the generated files before renaming
5. **Backup**: Copy to cloud storage before deploying

---

## Need Help?

If you get stuck:
1. Check AI_GENERATION_PROMPTS.md for full details
2. Check SOUND_EFFECTS_GUIDE.md for integration help
3. Run `python elevenlabs_setup.py` for automated generation

---

**Ready to generate? Start with the Python script for fastest results!**
