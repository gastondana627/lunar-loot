# WebRTC Rewrite Plan

## Goal: Make production work while keeping EXACT same look/feel

## What Stays THE SAME:
✅ All UI (title, level start, complete screens)
✅ All game mechanics (moonrocks, scoring, combos)
✅ All visuals (backgrounds, logos, fonts)
✅ All features (easter eggs, levels, leaderboard)
✅ All polish (animations, overlays, effects)

## What Changes:
❌ Remove: `cv2.VideoCapture(0)` loop
✅ Add: WebRTC video processor callback
✅ Add: Proper state management for WebRTC

## Implementation:
1. Create VideoProcessor class with game logic
2. Use webrtc_streamer for camera
3. Keep all existing screens/UI
4. Test locally first
5. Deploy to production

## Testing Checklist:
- [ ] Title screen looks identical
- [ ] Level start screen works
- [ ] Gameplay shows moonrocks
- [ ] Hand tracking works
- [ ] Scoring works
- [ ] Combos work
- [ ] Easter eggs work
- [ ] Level complete works
- [ ] All backgrounds show

## Timeline: 30-45 minutes
