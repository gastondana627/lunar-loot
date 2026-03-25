## Lunar Loot - Production Version with Full Polish
## Created for Chroma Awards 2025
## Tools: Google MediaPipe, Freepik, Adobe
## Production Ready - v2.0

import cv2
import mediapipe as mp
import numpy as np
import random
import os
import streamlit as st
import time
import base64
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Lunar Loot - AI Game",
    page_icon="🌑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Game constants
LEVEL_TIME_LIMIT = 30
GAME_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKGROUND_IMAGE_DIR = os.path.join(GAME_ROOT_DIR, "backgrounds", "New_Background_Rotation_1")

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Helper functions
def load_background_image(level):
    """Load background image for level"""
    bg_path = os.path.join(BACKGROUND_IMAGE_DIR, f"{level}.png")
    if os.path.exists(bg_path):
        try:
            img = Image.open(bg_path)
            return img
        except:
            pass
    return None

def load_logo():
    """Load game logo"""
    logo_path = os.path.join(GAME_ROOT_DIR, "ui_assets", "branding", "Lunar_Loot_Logo.png")
    if os.path.exists(logo_path):
        try:
            with open(logo_path, 'rb') as f:
                return base64.b64encode(f.read()).decode()
        except:
            pass
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
if 'background_image' not in st.session_state:
    st.session_state.background_image = None

def reset_level():
    """Reset level with new moonrocks and background"""
    st.session_state.moonrocks = []
    num_rocks = 5 + st.session_state.level
    for _ in range(num_rocks):
        st.session_state.moonrocks.append({
            'x': random.randint(50, 590),
            'y': random.randint(50, 430),
            'collected': False
        })
    st.session_state.start_time = time.time()
    st.session_state.background_image = load_background_image(st.session_state.level)

# Custom CSS - Full polish
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
    
    [data-testid="stImage"] {
        border-radius: 8px;
        box-shadow: 0 20px 60px rgba(99, 102, 241, 0.3);
        border: 1px solid rgba(99, 102, 241, 0.3);
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
                        <video width="100%" height="50" autoplay loop muted playsinline 
                               style="display: block; object-fit: cover;">
                            <source src="data:video/mp4;base64,{footer_video_bytes}" type="video/mp4">
                        </video>
                    </div>
                </a>
            """, unsafe_allow_html=True)
    except:
        pass

# Title Screen
if st.session_state.game_state == 'title':
    logo_bytes = load_logo()
    if logo_bytes:
        st.markdown(f"""
            <div style="text-align: center; padding: 50px;">
                <img src="data:image/png;base64,{logo_bytes}" style="max-width: 500px; width: 80%;">
                <p style="font-size: 1.5rem; color: #cbd5e1; margin-top: 20px;">
                    AI-Powered Hand Tracking Game
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 50px;">
                <h1 style="font-size: 4rem; color: #6366f1; text-shadow: 0 0 20px rgba(99, 102, 241, 0.8);">
                    🌙 LUNAR LOOT 🌙
                </h1>
                <p style="font-size: 1.5rem; color: #cbd5e1;">AI-Powered Hand Tracking Game</p>
            </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="background: rgba(99, 102, 241, 0.15); padding: 15px; border-radius: 8px; 
                        border: 1px solid rgba(99, 102, 241, 0.4); margin-bottom: 20px;">
                <p style="color: #fbbf24; font-size: 14px; margin: 0; text-align: center;">
                    📷 <strong>Webcam Required</strong> - Camera access needed for hand tracking
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("▶ BEGIN GAME", type="primary", use_container_width=True):
            st.session_state.game_state = 'start'
            st.rerun()
        
        st.write("")
        
        if st.button("ℹ️ ABOUT", use_container_width=True):
            st.session_state.game_state = 'about'
            st.rerun()
        
        st.markdown("""
            <div style="margin-top: 30px; padding: 20px; background: rgba(99, 102, 241, 0.1); 
                        border-radius: 10px; border: 1px solid rgba(99, 102, 241, 0.3);">
                <p style="color: #6366f1; font-size: 14px; margin: 5px 0;">POWERED BY</p>
                <p style="color: #f8fafc; font-size: 12px; margin: 5px 0;">
                    Google MediaPipe • Freepik • Adobe
                </p>
            </div>
        """, unsafe_allow_html=True)

# About Screen
elif st.session_state.game_state == 'about':
    st.markdown("<h1 style='text-align: center; color: #6366f1;'>ABOUT LUNAR LOOT</h1>", 
                unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
            <div style="background: rgba(10, 14, 39, 0.9); padding: 40px; border-radius: 12px; 
                        border: 1px solid rgba(99, 102, 241, 0.4);">
                <h3 style="color: #f8fafc;">🎮 The Game</h3>
                <p style="color: #cbd5e1; line-height: 1.8;">
                    Lunar Loot is an AI-powered hand-tracking game where you collect cosmic moonrocks 
                    using only your hand gestures. No controllers needed!
                </p>
                
                <h3 style="color: #f8fafc; margin-top: 25px;">🎯 How to Play</h3>
                <p style="color: #cbd5e1; line-height: 1.8;">
                    • Show your hand to the camera<br>
                    • Point with your index finger<br>
                    • Touch moonrocks to collect them<br>
                    • Collect all rocks before time runs out
                </p>
                
                <h3 style="color: #f8fafc; margin-top: 25px;">🎁 Easter Eggs</h3>
                <p style="color: #cbd5e1; line-height: 1.8;">
                    • ✌️ Peace sign: +50 points<br>
                    • 👍 Thumbs up: +100 points + Chroma shoutout!
                </p>
                
                <h3 style="color: #f8fafc; margin-top: 25px;">🤖 AI Technology</h3>
                <p style="color: #cbd5e1; line-height: 1.8;">
                    • <strong>Google MediaPipe:</strong> Real-time hand tracking<br>
                    • <strong>Freepik AI:</strong> Space-themed visuals<br>
                    • <strong>Adobe:</strong> Editing and polish
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("← BACK TO MENU", use_container_width=True):
            st.session_state.game_state = 'title'
            st.rerun()

# Start Screen  
elif st.session_state.game_state == 'start':
    st.markdown("<h1 style='text-align: center; color: #6366f1;'>🚀 MISSION BRIEFING</h1>", 
                unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<p style="color: #e2e8f0; font-weight: 600; margin-bottom: 8px;">Enter your Spacetag</p>', 
                    unsafe_allow_html=True)
        spacetag = st.text_input("Spacetag", 
                                 value=st.session_state.spacetag,
                                 placeholder="AstroHunter42",
                                 label_visibility="collapsed")
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
                    • Find hidden gesture bonuses!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 LAUNCH MISSION", type="primary", use_container_width=True):
            reset_level()
            st.session_state.game_state = 'playing'
            st.rerun()

# Playing State
elif st.session_state.game_state == 'playing':
    st.markdown(f"""
        <h1 style='text-align: center; color: #6366f1;'>
            LEVEL {st.session_state.level} | SCORE: {st.session_state.score}
        </h1>
    """, unsafe_allow_html=True)
    
    # Time remaining
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, LEVEL_TIME_LIMIT - elapsed)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Camera input
        camera_image = st.camera_input("Show your hand to play", key="camera")
        
        if camera_image:
            # Process frame
            image = Image.open(camera_image)
            frame = np.array(image)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = cv2.flip(frame, 1)
            
            # Apply background if available
            if st.session_state.background_image:
                try:
                    bg = st.session_state.background_image.resize((frame.shape[1], frame.shape[0]))
                    bg_array = np.array(bg)
                    if bg_array.shape[2] == 4:  # RGBA
                        bg_array = cv2.cvtColor(bg_array, cv2.COLOR_RGBA2BGR)
                    # Blend: 30% camera, 70% background
                    frame = cv2.addWeighted(frame, 0.3, bg_array, 0.7, 0)
                except:
                    pass
            
            # MediaPipe processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
                result = hands.process(rgb_frame)
                
                # Draw moonrocks
                for rock in st.session_state.moonrocks:
                    if not rock['collected']:
                        cv2.circle(frame, (rock['x'], rock['y']), 25, (200, 200, 200), -1)
                        cv2.circle(frame, (rock['x'], rock['y']), 25, (99, 102, 241), 2)
                
                # Hand tracking
                if result.multi_hand_landmarks:
                    for hand_landmarks in result.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        
                        # Get index finger tip
                        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                        h, w, _ = frame.shape
                        finger_x = int(index_tip.x * w)
                        finger_y = int(index_tip.y * h)
                        
                        cv2.circle(frame, (finger_x, finger_y), 15, (34, 197, 94), -1)
                        
                        # Check collisions
                        for rock in st.session_state.moonrocks:
                            if not rock['collected']:
                                dist = np.sqrt((finger_x - rock['x'])**2 + (finger_y - rock['y'])**2)
                                if dist < 40:
                                    rock['collected'] = True
                                    st.session_state.score += 10
                        
                        # Easter egg detection
                        index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
                        middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                        middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
                        ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
                        ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
                        pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                        pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
                        
                        # Peace sign detection
                        index_extended = index_tip.y < index_pip.y
                        middle_extended = middle_tip.y < middle_pip.y
                        ring_curled = ring_tip.y > ring_mcp.y
                        pinky_curled = pinky_tip.y > pinky_mcp.y
                        
                        current_time = time.time()
                        if (index_extended and middle_extended and ring_curled and pinky_curled and
                            current_time - st.session_state.peace_last_trigger > 5.0):
                            st.session_state.score += 50
                            st.session_state.peace_last_trigger = current_time
                            cv2.putText(frame, "PEACE! +50", (w//2 - 100, h//2), 
                                      cv2.FONT_HERSHEY_DUPLEX, 2, (34, 197, 94), 3)
                
                # Draw score and time
                cv2.putText(frame, f"Score: {st.session_state.score}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, f"Time: {int(remaining)}s", (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Display processed frame
            st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), use_container_width=True)
    
    with col2:
        st.metric("Time Remaining", f"{int(remaining)}s")
        st.metric("Rocks Left", sum(1 for r in st.session_state.moonrocks if not r['collected']))
        st.metric("Level", st.session_state.level)
        
        if st.button("⏸️ PAUSE", use_container_width=True):
            st.session_state.game_state = 'title'
            st.rerun()
    
    # Check win/lose
    if remaining <= 0:
        if all(r['collected'] for r in st.session_state.moonrocks):
            st.session_state.level += 1
            st.success(f"🎉 Level {st.session_state.level - 1} Complete!")
            time.sleep(2)
            reset_level()
            st.rerun()
        else:
            st.session_state.game_state = 'end'
            st.rerun()
    elif all(r['collected'] for r in st.session_state.moonrocks):
        st.session_state.level += 1
        st.success(f"🎉 Level {st.session_state.level - 1} Complete!")
        time.sleep(2)
        reset_level()
        st.rerun()
    
    # Auto-refresh for timer
    time.sleep(0.1)
    st.rerun()

# End Screen
elif st.session_state.game_state == 'end':
    st.markdown(f"""
        <div style="text-align: center; padding: 50px;">
            <h1 style="font-size: 3rem; color: #6366f1;">MISSION COMPLETE!</h1>
            <h2 style="color: #cbd5e1;">Final Score: {st.session_state.score}</h2>
            <h3 style="color: #cbd5e1;">Levels Completed: {st.session_state.level - 1}</h3>
            <p style="color: #cbd5e1; margin-top: 20px;">Pilot: {st.session_state.spacetag or 'Anonymous'}</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 PLAY AGAIN", type="primary", use_container_width=True):
            st.session_state.score = 0
            st.session_state.level = 1
            st.session_state.game_state = 'title'
            st.rerun()
