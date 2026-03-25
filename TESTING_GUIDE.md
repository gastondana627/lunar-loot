# 🧪 Testing Guide - Lunar Loot

## ✅ All Features Implemented!

**Localhost running at:** http://localhost:8501

---

## 🎯 Features to Test

### 1. Spacetag System ✅
- [ ] Enter a spacetag on start screen
- [ ] Try to start without spacetag (should show warning)
- [ ] Spacetag appears in game HUD (top left)
- [ ] Spacetag shows on end screen
- [ ] Spacetag appears in leaderboard

### 2. Enhanced Scoring ✅
- [ ] Collect moonrock = 10 points (base)
- [ ] Collect 2 rocks within 2 seconds = combo bonus
- [ ] Combo counter shows in HUD
- [ ] Time bonus added at level complete
- [ ] Score increases properly

### 3. Combo System ✅
- [ ] "COMBO x2!" appears when collecting quickly
- [ ] Combo resets if you wait >2 seconds
- [ ] Combo bonus adds to score (+5 per combo level)
- [ ] Visual feedback in green text

### 4. Space Selfie ✅
- [ ] Webcam frame captured on level complete
- [ ] Selfie shows on game over screen
- [ ] Overlay includes: spacetag, score, level, hashtags
- [ ] Download button works
- [ ] Downloaded file named correctly

### 5. Leaderboard ✅
- [ ] Top 10 scores displayed
- [ ] Shows: spacetag, score, level
- [ ] Medals for top 3 (🥇🥈🥉)
- [ ] Current player highlighted
- [ ] Persists between sessions
- [ ] Sorted by score (highest first)

### 6. Social Sharing ✅
- [ ] Twitter share button appears
- [ ] Correct hashtags: #LunarLoot #ChromaAwards
- [ ] Score included in tweet text
- [ ] Opens in new tab

---

## 🐛 Known Issues to Check

- [ ] Camera permissions work
- [ ] Hand tracking responsive
- [ ] No crashes during gameplay
- [ ] Selfie captures correctly
- [ ] Leaderboard saves properly
- [ ] All text readable
- [ ] Buttons work on all screens

---

## 🎮 Full Playthrough Test

1. **Start Screen**
   - Enter spacetag: "TestPlayer"
   - Click Start Game

2. **Level 1**
   - Collect all moonrocks
   - Try to get combos
   - Watch timer

3. **Level Complete**
   - See rocket animation
   - Selfie should be captured

4. **Continue Playing**
   - Play 2-3 levels
   - Build up score

5. **Game Over**
   - Check final score
   - View selfie
   - Check leaderboard
   - Download selfie
   - Try Twitter share

6. **Play Again**
   - Different spacetag
   - Check leaderboard updates

---

## 📊 Expected Behavior

### Scoring Example:
- Collect 6 moonrocks with combos:
  - Rock 1: 10 pts (base)
  - Rock 2: 15 pts (10 + 5 combo)
  - Rock 3: 20 pts (10 + 10 combo)
  - Rock 4: 25 pts (10 + 15 combo)
  - Rock 5: 30 pts (10 + 20 combo)
  - Rock 6: 35 pts (10 + 25 combo)
  - Time bonus: 20 pts (10 seconds left)
  - **Total: 155 pts**

---

## 🚨 If You Find Bugs

Note them here and we'll fix before deployment:

**Bug 1:**
- Description:
- Steps to reproduce:
- Expected vs Actual:

**Bug 2:**
- Description:
- Steps to reproduce:
- Expected vs Actual:

---

## ✅ Ready for Production?

Once all tests pass:
- [ ] All features work
- [ ] No critical bugs
- [ ] Performance is good
- [ ] Ready to push to GitHub
- [ ] Ready to deploy to Streamlit Cloud

---

**Start testing at:** http://localhost:8501

Let me know what you find! 🚀
