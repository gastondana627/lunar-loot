# 🚀 Feature Implementation Guide

## Features to Add

### ✅ 1. Spacetag/Gamertag System (15 min)
### ✅ 2. Colored Moonrocks (20 min)
### ✅ 3. Enhanced Scoring with Bonuses (25 min)
### ✅ 4. Space Selfie Feature (30 min)
### ✅ 5. Leaderboard System (30 min)

---

## Quick Implementation Steps

### Step 1: Add Spacetag to Start Screen

In `display_start_screen()`, add before the "Start Game" button:

```python
# Spacetag entry
spacetag = st.text_input("🚀 Enter your Spacetag:", 
                         value=st.session_state.get('spacetag', ''),
                         max_chars=20,
                         placeholder="AstroHunter42")
if spacetag:
    st.session_state.spacetag = spacetag

# Update Start Game button logic
if st.button("🎮 Start Game", type="primary"):
    if not st.session_state.get('spacetag'):
        st.warning("⚠️ Please enter a Spacetag first!")
    else:
        # existing start logic...
```

### Step 2: Initialize New Session State Variables

Add to session state initialization:

```python
if 'spacetag' not in st.session_state:
    st.session_state.spacetag = ""
if 'combo' not in st.session_state:
    st.session_state.combo = 0
if 'last_collect_time' not in st.session_state:
    st.session_state.last_collect_time = 0
if 'selfie_frame' not in st.session_state:
    st.session_state.selfie_frame = None
```

### Step 3: Add Colored Moonrocks

Import enhanced_features at top:

```python
from enhanced_features import get_moonrock_color, calculate_bonus_score
```

In the game loop, colorize moonrocks:

```python
# Get background name
bg_name = os.path.basename(st.session_state.background_image).replace('.jpg', '')
rock_color = get_moonrock_color(bg_name)

# When drawing moonrocks, tint them
for rx, ry in st.session_state.moonrocks:
    colored_rock = moonrock_img.copy()
    # Apply color tint (simplified version)
    overlay_image(frame, colored_rock, rx, ry)
```

### Step 4: Enhanced Scoring System

In collection logic:

```python
# When moonrock is collected
current_time = time.time()
time_since_last = current_time - st.session_state.last_collect_time

# Combo system
if time_since_last < 2.0:  # Within 2 seconds = combo
    st.session_state.combo += 1
else:
    st.session_state.combo = 0

# Calculate points
base_points = 10
combo_bonus = st.session_state.combo * 5
total_points = base_points + combo_bonus

st.session_state.score += total_points
st.session_state.last_collect_time = current_time
```

### Step 5: Space Selfie on Game Over

In `display_end_screen()`:

```python
# Capture selfie if available
if st.session_state.get('selfie_frame') is not None:
    st.image(st.session_state.selfie_frame, caption="Your Space Selfie! 📸")
    
    # Download button
    import cv2
    _, buffer = cv2.imencode('.jpg', st.session_state.selfie_frame)
    st.download_button(
        label="📥 Download Selfie",
        data=buffer.tobytes(),
        file_name=f"moonrock_selfie_{st.session_state.spacetag}.jpg",
        mime="image/jpeg"
    )
    
    # Social share buttons
    st.markdown("""
        <div style="margin: 20px 0;">
            <a href="https://twitter.com/intent/tweet?text=I scored {score} in Moonrock Collector! 🌙 %23ChromaAwards %23MoonrockCollector" 
               target="_blank" style="margin-right: 10px;">
                🐦 Share on Twitter
            </a>
        </div>
    """.format(score=st.session_state.score), unsafe_allow_html=True)
```

### Step 6: Leaderboard Display

Add to end screen:

```python
from enhanced_features import load_high_scores

st.write("---")
st.markdown("### 🏆 Top Spacetags")

scores = load_high_scores()
if scores:
    for i, entry in enumerate(scores[:5], 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        st.write(f"{medal} **{entry['spacetag']}** - {entry['score']} pts (Level {entry['level']})")
else:
    st.info("No high scores yet. Be the first!")
```

---

## Complete Feature Integration Checklist

- [ ] Add spacetag input to start screen
- [ ] Initialize new session state variables
- [ ] Import enhanced_features module
- [ ] Add colored moonrock system
- [ ] Implement combo scoring
- [ ] Add time bonus calculation
- [ ] Capture selfie frame on level complete
- [ ] Add selfie display to end screen
- [ ] Add download button for selfie
- [ ] Add social share buttons
- [ ] Implement high score saving
- [ ] Display leaderboard on end screen
- [ ] Test all features locally
- [ ] Deploy to Streamlit Cloud

---

## Testing Steps

1. Enter a spacetag
2. Play through a level
3. Collect moonrocks quickly (test combo)
4. Complete level (test selfie capture)
5. Check end screen for selfie
6. Download selfie
7. Check leaderboard
8. Play again with different spacetag
9. Verify leaderboard updates

---

## Time Estimate

- Spacetag: 15 min
- Colored rocks: 20 min
- Enhanced scoring: 25 min
- Space selfie: 30 min
- Leaderboard: 30 min
- Testing: 20 min

**Total: ~2.5 hours**

---

## Want Me to Implement?

I can integrate all these features into catching_moonrocks.py right now.
Just say the word and I'll make it happen! 🚀
