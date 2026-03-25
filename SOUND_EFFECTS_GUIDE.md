# 🔊 Sound Effects Integration Guide

## Sound Effects Needed for Moonrock Collector

### Core Game Sounds (Priority)
1. **Moonrock Collection** - When player touches a moonrock
   - Type: Positive chime/ping sound
   - Frequency: Multiple times per level
   - Mood: Rewarding, satisfying

2. **Level Complete** - When all moonrocks collected
   - Type: Victory fanfare/success sound
   - Frequency: Once per level
   - Mood: Triumphant, exciting

3. **Level Start** - When "Begin Game" is clicked
   - Type: Countdown beep or "Go!" sound
   - Frequency: Once per level
   - Mood: Energetic, motivating

4. **Time Warning** - When 10 seconds remain
   - Type: Urgent beeping or ticking
   - Frequency: Once per level (if time runs low)
   - Mood: Tense, urgent

5. **Game Over** - When time runs out
   - Type: Descending tone or "game over" sound
   - Frequency: Once per game session
   - Mood: Disappointing but not harsh

### Optional Enhancement Sounds
6. **Background Music** - Ambient space music during gameplay
7. **Hand Detection** - Subtle sound when hand enters frame
8. **Rocket Animation** - Whoosh/engine sound during level transition
9. **Menu Hover** - Subtle click/hover sounds on buttons

## ElevenLabs Integration Options

### Option 1: Text-to-Speech Sound Effects (Recommended)
Use ElevenLabs to generate voice-based sound effects:

```python
# Examples of text prompts for ElevenLabs:
"Ding! Moonrock collected!"
"Level complete! Well done!"
"Three, two, one, go!"
"Ten seconds remaining!"
"Game over! Try again!"
```

**Pros:**
- Unique, AI-generated audio
- Clear sponsor integration
- Can be customized easily
- Adds personality to game

**Cons:**
- Requires API key
- May sound less "game-like"
- API calls cost money (small amount)

### Option 2: ElevenLabs Sound Effects API
If ElevenLabs has a sound effects API (check their docs):
- Generate actual game sound effects
- More traditional game audio
- Still counts as AI-generated

### Option 3: Hybrid Approach (Best for Competition)
- Use ElevenLabs for voice announcements ("Level 2!", "Great job!")
- Use free sound effects for quick feedback (pings, beeps)
- Mention both in submission

## Implementation Steps

### Step 1: Get ElevenLabs API Key
1. Go to https://elevenlabs.io
2. Sign up for free account
3. Get API key from dashboard
4. Free tier: 10,000 characters/month

### Step 2: Generate Sound Files
```python
from elevenlabs import generate, save

# Generate collection sound
audio = generate(
    text="Moonrock collected!",
    voice="Rachel",  # Or choose another voice
    model="eleven_monolingual_v1"
)
save(audio, "sounds/collect.mp3")

# Generate level complete
audio = generate(
    text="Level complete! Amazing work!",
    voice="Rachel",
    model="eleven_monolingual_v1"
)
save(audio, "sounds/level_complete.mp3")

# Generate countdown
audio = generate(
    text="Three, two, one, go!",
    voice="Rachel",
    model="eleven_monolingual_v1"
)
save(audio, "sounds/countdown.mp3")
```

### Step 3: Add to Game
```python
def play_sound(sound_file):
    """Play a sound effect in Streamlit"""
    with open(sound_file, "rb") as f:
        audio_bytes = f.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()
        st.markdown(
            f'<audio autoplay><source src="data:audio/mp3;base64,{audio_b64}"></audio>',
            unsafe_allow_html=True
        )

# In game loop when moonrock collected:
play_sound("sounds/collect.mp3")
```

## Free Sound Effects (Backup/Supplement)

If ElevenLabs doesn't work out, use these free sources:
- **Mixkit** - https://mixkit.co/free-sound-effects/game/
- **Freesound** - https://freesound.org (CC0 license)
- **Zapsplat** - https://www.zapsplat.com/sound-effect-categories/

## Recommended Sound Effect URLs (Currently in Code)

```python
sounds = {
    "collect": "https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3",
    "level_complete": "https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3",
    "game_over": "https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3"
}
```

## Competition Strategy

### For Maximum Sponsor Points:
1. **Primary Audio**: ElevenLabs voice announcements
   - "Welcome to Moonrock Collector!"
   - "Level [number] starting!"
   - "Moonrock collected!" (or just "Collected!")
   - "Level complete!"
   - "Game over! Final score: [score]"

2. **Secondary Audio**: Free sound effects for quick feedback
   - Ping sounds for collections
   - Beeps for countdown
   - Background music

3. **Documentation**: 
   - Clearly state in README: "Voice announcements powered by ElevenLabs AI"
   - Show ElevenLabs logo on start screen
   - Mention in submission description

## Testing Checklist

- [ ] Sound plays on moonrock collection
- [ ] Sound plays on level complete
- [ ] Sound plays on game over
- [ ] Background music loops properly
- [ ] Sounds don't overlap awkwardly
- [ ] Volume levels are balanced
- [ ] Works in Chrome/Firefox
- [ ] Works on Streamlit Cloud deployment

## Time Estimate

- **ElevenLabs Setup**: 15-20 minutes
- **Generate 5-7 sound files**: 10-15 minutes
- **Integrate into game**: 20-30 minutes
- **Testing**: 15-20 minutes
- **Total**: 1-1.5 hours

## Next Steps

1. Sign up for ElevenLabs (if not already)
2. Generate voice announcements
3. Save to `sounds/` directory
4. Update game code to use generated sounds
5. Test locally
6. Deploy to Streamlit Cloud
7. Update README with ElevenLabs credit

---

**Pro Tip**: Even if you only add 2-3 ElevenLabs voice announcements, it's enough to show AI integration. Don't overthink it - judges just need to see you used the tool meaningfully!
