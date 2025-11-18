# 🎁 Easter Eggs Guide - Lunar Loot

## How to Trigger Easter Eggs

### ❤️ Heart Gesture - +50 Points

**Requirements:**
- Must be **during gameplay** (collecting moonrocks)
- Show **BOTH hands** to camera
- Hands must be clearly visible

**How to do it:**
1. Hold both hands up in front of camera
2. Bring your **thumbs together** (like making a heart shape)
3. Keep thumbs within ~20% of screen distance
4. Hold for a moment

**What you'll see:**
- Giant ❤️ emoji pops up in center
- "+50 BONUS!" message at top
- Pink glow effect
- Score increases by 50
- Sound effect plays

**Visual indicator:**
- Pink circles appear on your thumbs
- Pink line connects them when close enough

**Troubleshooting:**
- Make sure both hands are in frame
- Bring thumbs closer together
- Hold steady for 1 second
- Can only trigger once per separation

---

### 👍 Chroma Awards Thumbs Up - +100 Points

**Requirements:**
- Must be **during gameplay**
- Show **one hand** to camera

**How to do it:**
1. Make a thumbs up gesture
2. Thumb pointing UP
3. Other fingers curled down
4. Hold for a moment

**What you'll see:**
- "CHROMA AWARDS" text with gradient
- "👍 +100 BONUS!" message
- "Thanks for the support!" subtitle
- Blue/purple glow effect
- Score increases by 100
- Sound effect plays

**Troubleshooting:**
- Make sure thumb is clearly pointing UP
- Curl other fingers down
- Hold steady for 1 second
- Can only trigger once per gesture

---

## Testing Tips

1. **Good lighting** - Make sure camera can see your hands clearly
2. **Steady hands** - Hold gesture for 1-2 seconds
3. **Clear background** - Avoid busy backgrounds that confuse tracking
4. **Distance** - Keep hands at comfortable distance from camera (arm's length)

---

## Technical Details

### Heart Gesture Detection:
- Detects when `len(result.multi_hand_landmarks) == 2`
- Calculates Euclidean distance between thumb tips
- Triggers when distance < 0.2 (normalized screen coordinates)
- Resets when distance > 0.25

### Thumbs Up Detection:
- Checks if thumb tip Y < thumb IP Y (thumb pointing up)
- Checks if index finger tip Y > index MCP Y (fingers curled)
- Triggers once per gesture cycle

---

## Why Easter Eggs Might Not Work

1. **Not in gameplay** - Only works while collecting moonrocks, not on menu
2. **Poor lighting** - Camera can't detect hands properly
3. **Too fast** - Need to hold gesture for ~1 second
4. **Already triggered** - Each gesture can only trigger once per cycle
5. **Hand not detected** - Make sure MediaPipe sees your hand (green skeleton should appear)

---

## Demo Video Ideas

For submission, consider recording:
1. Normal gameplay
2. Heart gesture trigger
3. Thumbs up trigger
4. Show the visual effects clearly

This demonstrates the AI hand tracking innovation!

---

**Created for Chroma Awards 2025**
