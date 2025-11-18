## Lunar Loot - AI-Powered Hand Tracking Game
## Created for Chroma Awards 2025
## Tools: Google MediaPipe, Freepik, Adobe
## 
## NOTE: For best experience, run locally with: streamlit run catching_moonrocks_ultimate.py
## This cloud version has limited camera functionality due to browser restrictions

import cv2
import mediapipe as mp
import numpy as np
import random
import os
import streamlit as st
import time
import base64
from PIL import Image
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Lunar Loot - AI Game",
    page_icon="🌑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Game constants
LEVEL_TIME_LIMIT = 30
NUM_MOONROCKS = 5
GAME_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKGROUND_IMAGE_DIR = os.path.join(GAME_ROOT_DIR, "backgrounds", "New_Background_Rotation_1")

# Game configuration - no WebRTC needed

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Sector names
SECTOR_NAMES = {
    1: "Mercury", 2: "Mars", 3: "Venus", 4: "Moon", 5: "Saturn",
    6: "Jupiter", 7: "Neptune", 8: "Uranus", 9: "Pluto", 10: "Asteroid Belt",
    11: "Comet", 12: "Nebula", 13: "Black Hole", 14: "Spaceship"
}

# Helper functions
def get_background_images(directory):
    try:
        image_files = [os.path.join(directory, f) for f in os.listdir(directory)
                       if f.endswith(('.jpg', '.jpeg', '.png')) and not f.startswith('.')]
        return sorted(image_files)
    except:
        return []

def load_logo():
    logo_path = os.path.join(GAME_ROOT_DIR, "ui_assets", "branding", "Lunar_Loot_Logo.png")
    if os.path.exists(logo_path):
        try:
            with open(logo_path, 'rb') as f:
                return base64.b64encode(f.read()).decode()
        except:
            pass
    return None

def convert_image_to_bytes(image_path):
    try:
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read())
    except:
        return None

# Session state initialization
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'title'
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'moonrocks' not in st.session_state:
    st.session_state.moonrocks = []
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'spacetag' not in st.session_state:
    st.session_state.spacetag = ''
if 'peace_last_trigger' not in st.session_state:
    st.session_state.peace_last_trigger = 0
if 'chroma_last_trigger' not in st.session_state:
    st.session_state.chroma_last_trigger = 0
if 'combo' not in st.session_state:
    st.session_state.combo = 0
if 'last_collect_time' not in st.session_state:
    st.session_state.last_collect_time = 0
if 'background_image_bytes' not in st.session_state:
    st.session_state.background_image_bytes = None
if 'background_image' not in st.session_state:
    st.session_state.background_image = None

def reset_level():
    """Reset level with new moonrocks and background"""
    st.session_state.moonrocks = []
    num_rocks = NUM_MOONROCKS + st.session_state.level
    for _ in range(num_rocks):
        st.session_state.moonrocks.append({
            'x': random.randint(50, 590),
            'y': random.randint(50, 430),
            'collected': False
        })
    st.session_state.start_time = time.time()
    st.session_state.combo = 0
    st.session_state.last_collect_time = 0
    
    # Load background
    bg_files = get_background_images(BACKGROUND_IMAGE_DIR)
    if bg_files and st.session_state.level <= len(bg_files):
        st.session_state.background_image_bytes = convert_image_to_bytes(bg_files[st.session_state.level - 1])
        try:
            from PIL import Image
            st.session_state.background_image = Image.open(bg_files[st.session_state.level - 1])
        except:
            st.session_state.background_image = None

def full_screen_background(image_bytes):
    if image_bytes:
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url(data:image/jpg;base64,{image_bytes.decode()});
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>
        """, unsafe_allow_html=True)

# No video processor needed for camera_input approach

# Custom CSS - FULL POLISH
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;900&display=swap');
    html, body, [class*="css"], * {
        font-family: 'Orbitron', sans-serif !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
    }
    </style>
""", unsafe_allow_html=True)

# Chroma Awards footer
chroma_footer_path = os.path.join(GAME_ROOT_DIR, "backgrounds", "Main_Menu", "Footer_Chroma_Awards.mp4")
if os.path.exists(chroma_footer_path):
    try:
        with open(chroma_footer_path, 'rb') as video_file:
            footer_video_bytes = base64.b64encode(video_file.read()).decode()
            st.markdown(f"""
                <a href="https://www.chromaawards.com" target="_blank" style="text-decoration: none;">
                    <div style="position: fixed; bottom: 0; left: 0; width: 100%; z-index: 9998; 
                                background: rgba(0,0,0,0.9); box-shadow: 0 -4px 12px rgba(0,0,0,0.5);">
                        <video width="100%" height="50" autoplay loop muted playsinline>
                            <source src="data:video/mp4;base64,{footer_video_bytes}" type="video/mp4">
                        </video>
                    </div>
                </a>
            """, unsafe_allow_html=True)
    except:
        pass

# Music button
components.html("""
    <div style="position: fixed; bottom: 60px; left: 10px; z-index: 10000;">
        <button id="musicBtn" style="
            background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%);
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%; width: 50px; height: 50px;
            cursor: pointer; font-size: 20px;">🎵</button>
    </div>
    <audio id="bgMusic" loop>
        <source src="https://assets.mixkit.co/active_storage/sfx/2745/2745-preview.mp3" type="audio/mpeg">
    </audio>
    <script>
        var music = document.getElementById('bgMusic');
        var btn = document.getElementById('musicBtn');
        var playing = false;
        btn.onclick = function() {
            if (playing) { music.pause(); btn.innerHTML = '🔇'; playing = false; }
            else { music.volume = 0.3; music.play(); btn.innerHTML = '🎵'; playing = true; }
        };
    </script>
""", height=0)

# ==================== GAME STATES ====================

# Title Screen
if st.session_state.game_state == 'title':
    main_menu_bg = os.path.join(GAME_ROOT_DIR, "backgrounds", "Main_Menu", "Main_Menu_Start_Screen_BG.png")
    if os.path.exists(main_menu_bg):
        bg_bytes = convert_image_to_bytes(main_menu_bg)
        if bg_bytes:
            full_screen_background(bg_bytes)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        logo_bytes = load_logo()
        if logo_bytes:
            st.markdown(f"""
                <div style="background: rgba(10, 14, 39, 0.85); padding: 30px; border-radius: 12px; 
                            border: 1px solid rgba(99, 102, 241, 0.3); margin-bottom: 20px; text-align: center;">
                    <img src="data:image/png;base64,{logo_bytes}" 
                         style="max-width: 100%; width: 400px; margin-bottom: 15px;">
                    <p style="font-size: 1.25rem; color: #cbd5e1; margin: 10px 0 0 0;">
                        Collect cosmic moonrocks before time runs out
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        # Important notice for cloud version
        st.warning("""
            ⚠️ **IMPORTANT:** This cloud version has limited camera functionality due to browser restrictions.
            
            **For the full real-time experience, please run locally:**
            ```bash
            git clone https://github.com/gastondana627/lunar-loot.git
            cd lunar-loot
            pip install -r requirements.txt
            streamlit run catching_moonrocks_ultimate.py
            ```
            
            Or watch the demo video to see the full gameplay!
        """)
        
        spacetag = st.text_input("Enter your Spacetag", value=st.session_state.spacetag, placeholder="AstroHunter42")
        if spacetag:
            st.session_state.spacetag = spacetag
        
        st.markdown("""
            <div style="background: rgba(10, 14, 39, 0.85); padding: 20px; border-radius: 12px; 
                        border: 1px solid rgba(99, 102, 241, 0.3); margin: 20px 0;">
                <p style="color: #f8fafc; font-weight: 600; font-size: 1.1rem; margin-bottom: 12px;">
                    Mission Objectives:
                </p>
                <p style="color: #cbd5e1; line-height: 1.8; margin: 0;">
                    • Use your index finger to touch the moonrocks<br>
                    • Collect all rocks before time runs out<br>
                    • Progress through 14 space environments<br>
                    • Find hidden gesture bonuses (peace sign, thumbs up)!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.info("📹 Camera Required: This game uses your webcam for hand tracking with Google MediaPipe AI.")
        
        if st.button("🚀 TRY CLOUD VERSION (Limited)", type="primary", use_container_width=True):
            reset_level()
            st.session_state.game_state = 'level_start'
            st.rerun()

# Level Start Screen
elif st.session_state.game_state == 'level_start':
    if st.session_state.background_image_bytes:
        full_screen_background(st.session_state.background_image_bytes)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="background: rgba(0,0,0,0.8); padding: 40px; border-radius: 20px; 
                        text-align: center; backdrop-filter: blur(10px);">
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h1 style='color: #6366f1;'>Level {st.session_state.level}</h1>", unsafe_allow_html=True)
        sector_name = SECTOR_NAMES.get(st.session_state.level, "Unknown Sector")
        st.markdown(f"<h3 style='color: #cbd5e1;'>Sector: {sector_name}</h3>", unsafe_allow_html=True)
        
        st.write("")
        st.markdown(f"**Current Score: {st.session_state.score}**")
        st.markdown(f"**Pilot: {st.session_state.spacetag or 'Anonymous'}**")
        st.write("")
        st.info("Tip: Collect moonrocks quickly to build combo multipliers")
        st.write("")
        
        if st.button("BEGIN MISSION", type="primary", use_container_width=True):
            st.session_state.game_state = 'playing'
            st.session_state.start_time = time.time()
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# Playing State - COMPLETE VERSION
elif st.session_state.game_state == 'playing':
    st.markdown(f"""
        <h1 style='text-align: center; color: #6366f1;'>
            LEVEL {st.session_state.level} | SCORE: {st.session_state.score}
        </h1>
    """, unsafe_allow_html=True)
    
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, LEVEL_TIME_LIMIT - elapsed)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.info("📸 **Cloud Mode:** Take a photo with your hand visible, then click 'BEGIN MISSION' to process. For real-time gameplay, run locally!")
        camera_image = st.camera_input("Show your hand to play", key="camera")
        
        if camera_image:
            image = Image.open(camera_image)
            frame = np.array(image)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = cv2.flip(frame, 1)
            
            # Apply background
            if st.session_state.background_image_bytes:
                try:
                    bg_data = base64.b64decode(st.session_state.background_image_bytes)
                    bg_array = np.frombuffer(bg_data, dtype=np.uint8)
                    bg_img = cv2.imdecode(bg_array, cv2.IMREAD_COLOR)
                    if bg_img is not None:
                        bg_img = cv2.resize(bg_img, (frame.shape[1], frame.shape[0]))
                        frame = cv2.addWeighted(frame, 0.3, bg_img, 0.7, 0)
                except:
                    pass
            
            # Draw moonrocks FIRST (before hand tracking)
            for rock in st.session_state.moonrocks:
                if not rock['collected']:
                    # Draw moonrock with glow effect
                    cv2.circle(frame, (rock['x'], rock['y']), 30, (255, 255, 255), -1)
                    cv2.circle(frame, (rock['x'], rock['y']), 32, (99, 102, 241), 3)
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
                result = hands.process(rgb_frame)
                
                if result.multi_hand_landmarks:
                    for hand_landmarks in result.multi_hand_landmarks:
                        # Draw hand skeleton with custom colors
                        mp_drawing.draw_landmarks(
                            frame, 
                            hand_landmarks, 
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2)
                        )
                        
                        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                        h, w, _ = frame.shape
                        finger_x = int(index_tip.x * w)
                        finger_y = int(index_tip.y * h)
                        
                        # Draw finger indicator with glow
                        cv2.circle(frame, (finger_x, finger_y), 20, (34, 197, 94), -1)
                        cv2.circle(frame, (finger_x, finger_y), 22, (255, 255, 255), 2)
                        
                        # Collision detection with combo
                        current_time = time.time()
                        for rock in st.session_state.moonrocks:
                            if not rock['collected']:
                                dist = np.sqrt((finger_x - rock['x'])**2 + (finger_y - rock['y'])**2)
                                if dist < 40:
                                    rock['collected'] = True
                                    
                                    # Combo system
                                    if current_time - st.session_state.last_collect_time < 2.0:
                                        st.session_state.combo += 1
                                    else:
                                        st.session_state.combo = 0
                                    
                                    points = 10 * (st.session_state.combo + 1)
                                    st.session_state.score += points
                                    st.session_state.last_collect_time = current_time
                        
                        # Easter eggs
                        index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
                        middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                        middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
                        ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
                        ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
                        pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                        pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
                        
                        index_extended = index_tip.y < index_pip.y
                        middle_extended = middle_tip.y < middle_pip.y
                        ring_curled = ring_tip.y > ring_mcp.y
                        pinky_curled = pinky_tip.y > pinky_mcp.y
                        
                        if (index_extended and middle_extended and ring_curled and pinky_curled and
                            current_time - st.session_state.peace_last_trigger > 5.0):
                            st.session_state.score += 50
                            st.session_state.peace_last_trigger = current_time
                            cv2.putText(frame, "PEACE! +50", (w//2 - 100, h//2), 
                                      cv2.FONT_HERSHEY_DUPLEX, 2, (34, 197, 94), 3)
                
                # Draw UI
                cv2.putText(frame, f"Score: {st.session_state.score}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, f"Time: {int(remaining)}s", (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                if st.session_state.combo > 0:
                    cv2.putText(frame, f"COMBO x{st.session_state.combo + 1}!", (10, 110),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (34, 197, 94), 2)
            
            st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), use_container_width=True)
    
    with col2:
        st.metric("Time", f"{int(remaining)}s")
        st.metric("Rocks Left", sum(1 for r in st.session_state.moonrocks if not r['collected']))
        st.metric("Combo", f"x{st.session_state.combo + 1}")
        
        if st.button("⏸️ PAUSE", use_container_width=True):
            st.session_state.game_state = 'title'
            st.rerun()
    
    # Check win/lose
    if remaining <= 0:
        if all(r['collected'] for r in st.session_state.moonrocks):
            st.session_state.game_state = 'level_complete'
            st.rerun()
        else:
            st.session_state.game_state = 'level_failed'
            st.rerun()
    elif all(r['collected'] for r in st.session_state.moonrocks):
        st.session_state.game_state = 'level_complete'
        st.rerun()
    
    time.sleep(0.1)
    st.rerun()

# Level Complete
elif st.session_state.game_state == 'level_complete':
    if st.session_state.background_image_bytes:
        full_screen_background(st.session_state.background_image_bytes)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="background: rgba(10, 14, 39, 0.9); padding: 40px; border-radius: 12px; 
                        text-align: center; backdrop-filter: blur(12px);">
        """, unsafe_allow_html=True)
        
        logo_bytes = load_logo()
        if logo_bytes:
            st.markdown(f"""
                <img src="data:image/png;base64,{logo_bytes}" 
                     style="max-width: 400px; width: 70%; animation: pulse 2s ease-in-out infinite;">
            """, unsafe_allow_html=True)
        
        st.markdown(f"<h1 style='color: #22c55e; margin: 20px 0;'>★ Level {st.session_state.level} Complete!</h1>", 
                    unsafe_allow_html=True)
        st.markdown(f"<p style='color: #f8fafc; font-size: 20px;'><strong>Score:</strong> {st.session_state.score}</p>", 
                    unsafe_allow_html=True)
        
        if st.session_state.combo > 0:
            st.markdown(f"<p style='color: #22c55e; font-size: 18px;'>Maximum Combo: x{st.session_state.combo + 1}</p>", 
                        unsafe_allow_html=True)
        
        st.info("▶ Preparing next sector...")
        st.markdown("</div>", unsafe_allow_html=True)
    
    time.sleep(2)
    st.session_state.level += 1
    st.session_state.combo = 0
    reset_level()
    st.session_state.game_state = 'level_start'
    st.rerun()

# Level Failed
elif st.session_state.game_state == 'level_failed':
    st.markdown(f"""
        <div style="text-align: center; padding: 50px;">
            <h1 style="font-size: 3rem; color: #ef4444;">MISSION FAILED</h1>
            <h2 style="color: #cbd5e1;">Final Score: {st.session_state.score}</h2>
            <h3 style="color: #cbd5e1;">Levels Completed: {st.session_state.level - 1}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 TRY AGAIN", type="primary", use_container_width=True):
            st.session_state.score = 0
            st.session_state.level = 1
            st.session_state.game_state = 'title'
            st.rerun()
