## Lunar Loot - Camera Input Version for Production
## Created for Chroma Awards 2025
## Tools: Google MediaPipe, Freepik, Adobe

import cv2
import mediapipe as mp
import numpy as np
import random
import streamlit as st
import time
from PIL import Image

# Page config
st.set_page_config(page_title="Lunar Loot", page_icon="🌙", layout="wide")

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Game constants
LEVEL_TIME_LIMIT = 30

# Session state
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

def reset_level():
    """Reset level with new moonrocks"""
    st.session_state.moonrocks = []
    num_rocks = 5 + st.session_state.level
    for _ in range(num_rocks):
        st.session_state.moonrocks.append({
            'x': random.randint(50, 590),
            'y': random.randint(50, 430),
            'collected': False
        })
    st.session_state.start_time = time.time()

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Orbitron', sans-serif !important;
    }
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    </style>
""", unsafe_allow_html=True)

# Title Screen
if st.session_state.game_state == 'title':
    st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <h1 style="font-size: 4rem; color: #6366f1;">🌙 LUNAR LOOT 🌙</h1>
            <p style="font-size: 1.5rem; color: #cbd5e1;">AI-Powered Hand Tracking Game</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("📷 **Camera Required** - This game uses your webcam for hand tracking")
        
        if st.button("▶ BEGIN GAME", type="primary", use_container_width=True):
            st.session_state.game_state = 'start'
            st.rerun()
        
        st.markdown("""
            <div style="margin-top: 30px; padding: 20px; background: rgba(99, 102, 241, 0.1); 
                        border-radius: 10px;">
                <p style="color: #6366f1; font-size: 14px;">POWERED BY</p>
                <p style="color: #f8fafc; font-size: 12px;">
                    Google MediaPipe • Freepik • Adobe
                </p>
            </div>
        """, unsafe_allow_html=True)

# Start Screen
elif st.session_state.game_state == 'start':
    st.markdown("<h1 style='text-align: center; color: #6366f1;'>🚀 MISSION BRIEFING</h1>", 
                unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        spacetag = st.text_input("Enter your Spacetag", 
                                 value=st.session_state.spacetag,
                                 placeholder="AstroHunter42")
        if spacetag:
            st.session_state.spacetag = spacetag
        
        st.markdown("""
            ### 🎯 How to Play:
            - Point your index finger at moonrocks to collect them
            - Collect all rocks before time runs out
            - ✌️ Peace sign = +50 bonus points
            - 👍 Thumbs up = +100 bonus points
        """)
        
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
            
            # MediaPipe processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
                result = hands.process(rgb_frame)
                
                # Draw moonrocks
                for rock in st.session_state.moonrocks:
                    if not rock['collected']:
                        cv2.circle(frame, (rock['x'], rock['y']), 25, (200, 200, 200), -1)
                
                # Hand tracking
                if result.multi_hand_landmarks:
                    for hand_landmarks in result.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        
                        # Get index finger tip
                        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                        h, w, _ = frame.shape
                        finger_x = int(index_tip.x * w)
                        finger_y = int(index_tip.y * h)
                        
                        cv2.circle(frame, (finger_x, finger_y), 15, (0, 255, 0), -1)
                        
                        # Check collisions
                        for rock in st.session_state.moonrocks:
                            if not rock['collected']:
                                dist = np.sqrt((finger_x - rock['x'])**2 + (finger_y - rock['y'])**2)
                                if dist < 40:
                                    rock['collected'] = True
                                    st.session_state.score += 10
                
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
        
        if st.button("⏸️ PAUSE"):
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
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 PLAY AGAIN", type="primary", use_container_width=True):
            st.session_state.score = 0
            st.session_state.level = 1
            st.session_state.game_state = 'title'
            st.rerun()
