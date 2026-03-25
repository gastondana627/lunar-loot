# 🎨 UI Image Generation Prompts - Lunar Loot

## Concept
Generate custom UI elements as images using AI (Freepik/Dreamina/FAL), then integrate them as visual components in the game. This creates a unique, cohesive aesthetic that matches the space theme.

---

## Button Designs

### 1. Primary Action Button (Launch Mission / Begin Mission)
```
A futuristic space-themed button with holographic appearance. Glowing blue-purple gradient 
with subtle scan lines. Metallic border with soft glow. Text reads "LAUNCH MISSION" in 
bold sans-serif font. Sci-fi UI element, clean and professional. 4K, PNG with transparency.
Style: NASA control panel, modern spacecraft interface.
Dimensions: 400x100px
```

### 2. Secondary Button (New Mission / Download)
```
Sleek space UI button with dark background and cyan accent border. Minimalist design with 
subtle glow effect. Text in clean sans-serif font. Professional spacecraft control aesthetic.
Transparent background, PNG format. 4K quality.
Dimensions: 350x90px
```

### 3. Social Share Button
```
Modern Twitter-style button with space theme integration. Dark blue background with subtle 
star field texture. White text "SHARE ON TWITTER". Rounded corners, professional finish.
PNG with transparency, 4K.
Dimensions: 300x80px
```

---

## HUD Elements

### 4. Score Display Panel
```
Futuristic heads-up display (HUD) panel for score tracking. Semi-transparent dark panel 
with glowing cyan borders. Digital-style numbers. Looks like spacecraft cockpit display.
Includes labels: "SCORE", "TIME", "LEVEL", "COMBO". Clean, readable, professional.
PNG with transparency, 4K.
Dimensions: 300x400px (vertical panel)
```

### 5. Combo Multiplier Badge
```
Glowing achievement badge with "COMBO x3" text. Bright green/cyan glow effect. 
Hexagonal or circular shape. Looks like power-up indicator in sci-fi game.
Animated glow optional. PNG with transparency, 4K.
Dimensions: 200x200px
```

### 6. Level Complete Banner
```
Celebratory banner with "LEVEL COMPLETE" text. Holographic blue-purple gradient.
Futuristic design with geometric patterns. Professional, not cartoonish.
Spacecraft mission success aesthetic. PNG with transparency, 4K.
Dimensions: 800x200px (horizontal banner)
```

---

## Input Fields

### 7. Spacetag Input Box
```
Futuristic text input field with dark background and glowing cyan border.
Placeholder text "Enter Spacetag". Looks like spacecraft terminal input.
Subtle scan line effect. Professional sci-fi UI. PNG with transparency, 4K.
Dimensions: 500x80px
```

---

## Information Panels

### 8. Mission Briefing Panel
```
Large information panel with semi-transparent dark background. Glowing blue border.
Contains mission objectives list. Looks like spacecraft briefing screen.
Clean typography, professional layout. PNG with transparency, 4K.
Dimensions: 600x400px
```

### 9. Leaderboard Display
```
Futuristic leaderboard panel with "TOP PILOTS" header. Dark background with 
cyan/purple accents. Rows for top 10 scores. Looks like spacecraft ranking system.
Professional, clean design. PNG with transparency, 4K.
Dimensions: 500x600px
```

### 10. Pro Tips Box
```
Small info box with lightbulb icon and tips text. Dark background with subtle glow.
Looks like helpful hint in spacecraft training simulator. Clean, minimal design.
PNG with transparency, 4K.
Dimensions: 400x150px
```

---

## Background Overlays

### 11. Start Screen Background Overlay
```
Semi-transparent dark overlay for start screen. Subtle star field texture.
Gradient from deep space blue to purple. Professional, atmospheric.
PNG with transparency (50% opacity), 4K.
Dimensions: 1920x1080px (full screen)
```

### 12. Game Over Screen Overlay
```
Dramatic space-themed overlay for end screen. Deep blue-purple gradient with 
subtle nebula effect. Professional, cinematic. PNG with transparency, 4K.
Dimensions: 1920x1080px (full screen)
```

---

## Icons & Badges

### 13. Hand Tracking Icon
```
Simple icon showing hand with pointing finger. Glowing cyan outline on dark background.
Minimalist, professional design. Looks like spacecraft control symbol.
PNG with transparency, 4K.
Dimensions: 150x150px
```

### 14. Camera Required Icon
```
Camera icon with checkmark. Glowing blue outline. Professional, clean design.
Spacecraft UI aesthetic. PNG with transparency, 4K.
Dimensions: 150x150px
```

### 15. Achievement Medals (1st, 2nd, 3rd)
```
Three futuristic medal/badge designs for leaderboard rankings.
1st: Gold/yellow glow with "1" 
2nd: Silver/white glow with "2"
3rd: Bronze/orange glow with "3"
Hexagonal or circular shape. Professional, not cartoonish.
PNG with transparency, 4K.
Dimensions: 100x100px each
```

---

## Logo & Branding

### 16. Lunar Loot Logo
```
Professional game logo with "LUNAR LOOT" text. Futuristic sans-serif font.
Crescent moon icon integrated. Blue-purple gradient with subtle glow.
Looks like space mission patch or spacecraft logo. Clean, memorable design.
PNG with transparency, 4K.
Dimensions: 600x200px (horizontal)
```

### 17. Chroma Awards Badge
```
Small badge with "Created for Chroma Awards 2025" text. Professional design
with trophy or award icon. Subtle, not distracting. PNG with transparency, 4K.
Dimensions: 300x100px
```

---

## Implementation Strategy

### Phase 1: Critical UI (1-2 hours)
1. Primary button (Launch Mission)
2. Score HUD panel
3. Spacetag input field
4. Logo

### Phase 2: Enhanced UI (2-3 hours)
5. Level complete banner
6. Leaderboard panel
7. Mission briefing panel
8. Combo badge

### Phase 3: Polish (1-2 hours)
9. Icons and badges
10. Background overlays
11. Social buttons
12. Achievement medals

---

## AI Tools to Use

### Freepik (Recommended)
- Go to freepik.com/ai/image-generator
- Use prompts above
- Download as PNG with transparency
- High quality, professional results

### Dreamina
- Good for futuristic UI elements
- Supports transparency
- Fast generation

### FAL
- API-based generation
- Good for batch creation
- Consistent style

---

## File Organization

```
ui_assets/
├── buttons/
│   ├── primary_button.png
│   ├── secondary_button.png
│   └── social_button.png
├── panels/
│   ├── score_hud.png
│   ├── leaderboard.png
│   └── mission_brief.png
├── icons/
│   ├── hand_tracking.png
│   ├── camera.png
│   └── medals/
│       ├── first.png
│       ├── second.png
│       └── third.png
├── overlays/
│   ├── start_screen.png
│   └── game_over.png
└── branding/
    ├── logo.png
    └── chroma_badge.png
```

---

## Integration Code Example

```python
# Load UI image
button_img = Image.open("ui_assets/buttons/primary_button.png")

# Display as clickable button
if st.button("", key="launch", use_container_width=False):
    # Button action
    launch_game()

# Overlay button image
st.image(button_img, use_container_width=False)
```

---

## Next Steps

1. Generate 3-5 critical UI elements first
2. Test integration in game
3. Generate remaining elements
4. Replace CSS-based UI with image-based UI
5. Deploy and test

**Want me to help integrate image-based UI once you generate the assets?**
