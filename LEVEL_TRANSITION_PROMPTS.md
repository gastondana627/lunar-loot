# 🚀 Level Transition Animation Prompts

## Purpose
Create engaging animations to display between levels while the next sector loads.

---

## Animation 1: Rocket Ship Launch

**Visual Prompt (Freepik/Dreamina/FAL):**
```
Animated rocket ship launching through space. Sleek futuristic spacecraft with 
glowing blue engines leaving a trail of stardust. Accelerating through a field 
of stars and distant galaxies. Smooth, dynamic motion. Cinematic space travel 
animation. 4K quality, 5-second loop. Sense of speed and adventure.
```

**Technical Specs:**
- Format: MP4 video
- Duration: 5 seconds
- Resolution: 1920x1080 or 1280x720
- Loop: Seamless
- File name: `rocketship1.mp4`

---

## Animation 2: Warp Speed Stars

**Visual Prompt (Freepik/Dreamina/FAL):**
```
Hyperspace jump animation. Stars stretching into lines as spacecraft enters 
warp speed. Blue and white light trails. Tunnel effect through space-time. 
Dynamic, fast-paced motion. Sci-fi aesthetic. 4K quality, 5-second loop. 
Sense of traveling faster than light.
```

**Technical Specs:**
- Format: MP4 video
- Duration: 5 seconds
- Resolution: 1920x1080 or 1280x720
- Loop: Seamless
- File name: `warp_speed.mp4`

---

## Animation 3: Planet Flyby

**Visual Prompt (Freepik/Dreamina/FAL):**
```
Animated flyby of a beautiful planet. Camera swooping past a colorful alien 
world with swirling clouds and glowing atmosphere. Stars in background. Smooth, 
cinematic camera movement. Photorealistic space scene. 4K quality, 5-second 
loop. Sense of exploration and discovery.
```

**Technical Specs:**
- Format: MP4 video
- Duration: 5 seconds
- Resolution: 1920x1080 or 1280x720
- Loop: Seamless
- File name: `planet_flyby.mp3`

---

## Animation 4: Asteroid Field

**Visual Prompt (Freepik/Dreamina/FAL):**
```
Animated journey through an asteroid field. Camera weaving between floating 
space rocks. Dramatic lighting from distant sun. Dynamic motion with depth. 
Cinematic space scene. 4K quality, 5-second loop. Sense of navigating through 
obstacles.
```

**Technical Specs:**
- Format: MP4 video
- Duration: 5 seconds
- Resolution: 1920x1080 or 1280x720
- Loop: Seamless
- File name: `asteroid_field.mp4`

---

## Animation 5: Nebula Zoom

**Visual Prompt (Freepik/Dreamina/FAL):**
```
Animated zoom through a colorful nebula. Purple, blue, and pink cosmic clouds. 
Stars forming in the gas. Camera moving forward through the nebula. Ethereal, 
beautiful space scene. 4K quality, 5-second loop. Sense of wonder and cosmic 
beauty.
```

**Technical Specs:**
- Format: MP4 video
- Duration: 5-seconds
- Resolution: 1920x1080 or 1280x720
- Loop: Seamless
- File name: `nebula_zoom.mp4`

---

## Current Animation

The game currently uses `rocketship1.mp4` located in `animations/` folder.

---

## How to Add New Animations

### Step 1: Generate Animation
Use one of the prompts above with:
- **Freepik AI Video** (recommended)
- **Runway ML**
- **Pika Labs**
- **Any AI video generator**

### Step 2: Save File
```bash
# Save to animations folder
animations/
├── rocketship1.mp4      # Current
├── warp_speed.mp4       # New
├── planet_flyby.mp4     # New
└── asteroid_field.mp4   # New
```

### Step 3: Update Code (Optional)
To randomly select animations:

```python
# In catching_moonrocks.py
import random

animation_files = [
    "rocketship1.mp4",
    "warp_speed.mp4", 
    "planet_flyby.mp4",
    "asteroid_field.mp4"
]

# Select random animation
selected = random.choice(animation_files)
animation_path = os.path.join(ANIMATION_DIR, selected)
```

---

## Alternative: Static Loading Screen

If animations are too large, use a static image with CSS animation:

**Visual Prompt:**
```
Futuristic loading screen design. Circular progress indicator with glowing 
blue ring. "LOADING NEXT SECTOR" text in modern sci-fi font. Dark space 
background with subtle stars. Minimalist, clean design. 4K quality. 
Professional game UI aesthetic.
```

**CSS Animation:**
```css
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading-spinner {
    animation: spin 2s linear infinite;
}
```

---

## File Size Considerations

For Streamlit Cloud deployment:

- **Recommended:** 1-3 MB per animation
- **Maximum:** 5 MB per animation
- **Compression:** Use H.264 codec, medium quality
- **Resolution:** 1280x720 is sufficient (smaller than 1920x1080)

### Compress Video:
```bash
# Using ffmpeg
ffmpeg -i input.mp4 -vcodec h264 -crf 28 -preset medium output.mp4
```

---

## Current Status

✅ **rocketship1.mp4** - Working in level transitions
⏳ **Additional animations** - Optional enhancement
🎮 **Game works fine** - With or without animations

---

Ready to generate? Use the prompts above with your favorite AI video tool!
