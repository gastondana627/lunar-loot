# 🚀 Lunar Loot - Version 2.0 Roadmap

## Current Version: 1.0 (Chroma Awards Submission)

**Status:** Production-ready, submitted to Chroma Awards 2025

---

## 🎯 Version 2.0 Goals

### Priority 1: Audio System Overhaul

**Problem:** Streamlit's game loop blocks audio playback
**Solution Options:**
1. **Migrate to Flask/FastAPI** - Full control over audio
2. **Use WebRTC** - Real-time audio streaming
3. **Implement WebSockets** - Separate audio channel
4. **Pre-load all sounds** - Browser cache approach

**Tasks:**
- [ ] Research best framework for real-time game audio
- [ ] Implement background music that actually loops
- [ ] Add sound effects that play reliably:
  - [ ] Moonrock collection beep
  - [ ] Level complete fanfare
  - [ ] Level failed sound
  - [ ] Time warning beeps (10s, 5s)
  - [ ] Easter egg sounds
  - [ ] Combo multiplier sounds
- [ ] Volume controls for users
- [ ] Mute button that persists

---

### Priority 2: Enhanced Easter Eggs

**Current Issues:**
- Peace sign detection sometimes false triggers
- Thumbs up needs better accuracy
- No visual feedback during cooldown

**Improvements:**
- [ ] Add cooldown timer display (e.g., "Peace Sign: 3s")
- [ ] Improve gesture detection accuracy:
  - [ ] Add confidence threshold
  - [ ] Require gesture hold for 1 second
  - [ ] Better finger position validation
- [ ] New easter eggs:
  - [ ] Open palm = Shield (blocks 1 time penalty)
  - [ ] Fist = Power-up (2x points for 10 seconds)
  - [ ] Rock-paper-scissors = Random bonus
- [ ] Easter egg achievements/badges
- [ ] Track easter egg stats in profile

---

### Priority 3: Multiplayer Mode

**Concept:** Two players compete side-by-side

**Features:**
- [ ] Split-screen camera view
- [ ] Separate moonrock sets for each player
- [ ] Real-time score comparison
- [ ] Head-to-head leaderboard
- [ ] Sabotage mechanics (steal opponent's rocks)
- [ ] Co-op mode (work together for bonus)

**Technical:**
- [ ] Dual camera support
- [ ] Network synchronization
- [ ] Lobby system
- [ ] Matchmaking

---

### Priority 4: Advanced Hand Gestures

**New Gestures:**
- [ ] **Pinch** - Slow down time for 3 seconds
- [ ] **Wave** - Shuffle moonrock positions
- [ ] **Point left/right** - Move all rocks in that direction
- [ ] **Clap** - Freeze time for 2 seconds
- [ ] **Finger gun** - Shoot rocks from distance

**Implementation:**
- [ ] MediaPipe gesture recognizer model
- [ ] Custom gesture training
- [ ] Gesture tutorial mode
- [ ] Practice arena

---

### Priority 5: Power-Ups & Items

**Collectible Power-Ups:**
- [ ] **Time Freeze** - Stop timer for 5 seconds
- [ ] **Magnet** - Rocks move toward your finger
- [ ] **2x Multiplier** - Double points for 10 seconds
- [ ] **Ghost Hand** - Collect multiple rocks at once
- [ ] **Shield** - Protect from time penalty

**Implementation:**
- [ ] Power-up spawn system
- [ ] Visual effects for active power-ups
- [ ] Power-up inventory UI
- [ ] Cooldown management

---

### Priority 6: Level Design & Progression

**Current:** Infinite levels with same mechanics
**Improved:**

**Level Types:**
- [ ] **Speed Run** - Collect 10 rocks as fast as possible
- [ ] **Survival** - Rocks disappear if not collected quickly
- [ ] **Boss Level** - One giant rock that moves
- [ ] **Puzzle** - Collect rocks in specific order
- [ ] **Chaos** - Rocks move randomly

**Progression:**
- [ ] Unlock new backgrounds with achievements
- [ ] Difficulty scaling (rock speed, size, count)
- [ ] Level themes (asteroid field, moon surface, space station)
- [ ] Story mode with narrative

---

### Priority 7: Social Features

**Leaderboard Enhancements:**
- [ ] Global leaderboard (all players)
- [ ] Friends leaderboard
- [ ] Daily/weekly challenges
- [ ] Seasonal rankings
- [ ] Clan/team system

**Sharing:**
- [ ] Share mission snapshots to social media
- [ ] Replay system (record and share gameplay)
- [ ] Challenge friends directly
- [ ] Embed game on other websites

---

### Priority 8: Mobile Support

**Current:** Desktop only
**Goal:** Mobile-friendly version

**Approach:**
- [ ] Touch controls (tap to collect)
- [ ] Gyroscope controls (tilt phone)
- [ ] Simplified UI for small screens
- [ ] Mobile-optimized hand tracking
- [ ] Progressive Web App (PWA)

**Challenges:**
- Camera performance on mobile
- Battery consumption
- Screen size limitations

---

### Priority 9: Customization

**Player Customization:**
- [ ] Custom spacetag colors
- [ ] Avatar system
- [ ] Hand trail effects (rainbow, fire, stars)
- [ ] Custom moonrock skins
- [ ] Background selection
- [ ] Music selection

**Unlockables:**
- [ ] Earn through gameplay
- [ ] Achievement rewards
- [ ] Level milestones
- [ ] Easter egg discoveries

---

### Priority 10: Analytics & Optimization

**Performance:**
- [ ] Reduce memory usage further
- [ ] Optimize MediaPipe processing
- [ ] Lazy load backgrounds
- [ ] Cache management
- [ ] FPS optimization

**Analytics:**
- [ ] Track user engagement
- [ ] Heatmap of moonrock collection
- [ ] Gesture accuracy metrics
- [ ] Level completion rates
- [ ] Easter egg discovery rates

---

## 🐛 Known Bugs to Fix

### High Priority
- [ ] About screen sometimes shows HTML code (cache issue)
- [ ] Audio doesn't play reliably (Streamlit limitation)
- [ ] Camera sometimes fails to initialize on first try
- [ ] Session state occasionally resets mid-game

### Medium Priority
- [ ] HUD can block moonrocks in corner
- [ ] Combo system resets too quickly
- [ ] Level transition animation skips sometimes
- [ ] Selfie capture timing inconsistent

### Low Priority
- [ ] Music button doesn't show on some browsers
- [ ] Leaderboard doesn't sort correctly with same scores
- [ ] Background overlay calculation can lag
- [ ] Hand skeleton sometimes flickers

---

## 🎨 UI/UX Improvements

### Visual Polish
- [ ] Particle effects for moonrock collection
- [ ] Animated background (stars moving)
- [ ] Better level transition animations
- [ ] Loading screen with tips
- [ ] Tutorial overlay for first-time players

### Accessibility
- [ ] Colorblind mode
- [ ] High contrast mode
- [ ] Larger text option
- [ ] Keyboard shortcuts
- [ ] Screen reader support

---

## 🔧 Technical Debt

### Code Quality
- [ ] Refactor game loop into separate module
- [ ] Extract UI components into reusable functions
- [ ] Add type hints throughout
- [ ] Write unit tests
- [ ] Add integration tests
- [ ] Document all functions
- [ ] Create developer guide

### Architecture
- [ ] Separate game logic from rendering
- [ ] Implement proper state machine
- [ ] Use design patterns (Observer, Strategy)
- [ ] Modular gesture system
- [ ] Plugin architecture for power-ups

---

## 📱 Platform Expansion

### Desktop App
- [ ] Electron wrapper
- [ ] Native camera access
- [ ] Better performance
- [ ] Offline mode
- [ ] Auto-updates

### Console/VR
- [ ] VR headset support (Quest, PSVR)
- [ ] Hand tracking in VR
- [ ] 3D moonrock collection
- [ ] Immersive space environment

---

## 🎓 Educational Features

**Learn While Playing:**
- [ ] Space facts between levels
- [ ] Hand anatomy tutorial
- [ ] AI/ML education mode
- [ ] Coding challenges (modify game)
- [ ] STEM integration

---

## 💰 Monetization (Optional)

**If going commercial:**
- [ ] Premium skins/themes
- [ ] Ad-free version
- [ ] Tournament entry fees
- [ ] Sponsorship integration
- [ ] Merchandise

---

## 📊 Success Metrics

**Track for V2:**
- Daily active users (DAU)
- Average session length
- Level completion rate
- Easter egg discovery rate
- Retention (D1, D7, D30)
- Social shares
- User feedback score

---

## 🗓️ Estimated Timeline

**Phase 1 (1-2 months):** Audio system + Bug fixes
**Phase 2 (2-3 months):** Enhanced gestures + Power-ups
**Phase 3 (3-4 months):** Multiplayer + Social features
**Phase 4 (4-6 months):** Mobile support + Platform expansion

---

## 🎯 Quick Wins (Do First)

1. **Fix audio system** - Biggest user complaint
2. **Add tutorial** - Help new players
3. **Improve gesture accuracy** - Core mechanic
4. **Add more easter eggs** - Fun factor
5. **Mobile PWA** - Expand audience

---

## 📝 Notes from V1 Development

**What Worked:**
- MediaPipe hand tracking is solid
- Visual design is professional
- Easter eggs add fun factor
- Leaderboard drives competition
- Level progression keeps interest

**What Didn't:**
- Audio in Streamlit is impossible
- Easter egg detection needs work
- Mobile support is critical
- Need better onboarding
- Multiplayer would be huge

**Lessons Learned:**
- Streamlit great for prototyping, not for games
- Hand tracking is more reliable than expected
- Users love easter eggs and hidden features
- Visual feedback is crucial
- Performance matters more than features

---

## 🚀 Version 2.0 Vision

**Goal:** Transform Lunar Loot from a tech demo into a full-fledged game

**Key Pillars:**
1. **Reliable Audio** - Music and sound effects that work
2. **Multiplayer** - Play with friends
3. **Mobile** - Play anywhere
4. **Depth** - More content, more replayability
5. **Polish** - Professional game feel

---

**Current Version:** 1.0 - Chroma Awards Submission ✅
**Next Version:** 2.0 - Full Game Release 🎮

Good luck with the competition! 🚀
