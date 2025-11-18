## Lunar Loot - WebRTC Version for Production
## Created for Chroma Awards 2025
## Tools: Google MediaPipe, Freepik, Adobe

import cv2
import mediapipe as mp
import numpy as np
import random
import os
import streamlit as st
import time
import base64
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av
import queue
import threading

# Page configuration
st.set_page_config(
    page_title="Lunar Loot - AI Game",
    page_icon="🌑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# WebRTC Configuration
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Game constants
LEVEL_TIME_LIMIT = 30
GAME_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Session state initialization
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'title'
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'moonrocks' not in st.session_state:
    st.session_state.moonrocks = []
if 'spacetag' not in st.session_state:
    st.session_state.spacetag = ''
if 'video_width' not in st.session_state:
    st.session_state.video_width = 640
if 'video_height' not in st.session_state:
    st.session_state.video_height = 480
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'peace_last_trigger' not in st.session_state:
    st.session_state.peace_last_trigger = 0
if 'chroma_last_trigger' not in st.session_state:
    st.session_state.chroma_last_trigger = 0

# Shared data queue for game state
if 'result_queue' not in st.session_state:
    st.session_state.result_queue = queue.Queue()

def reset_level():
    """Reset level with new moonrocks"""
    st.session_state.moonrocks = []
    num_rocks = 5 + st.session_state.level
    for _ in range(num_rocks):
        st.session_state.moonrocks.append({
            'x': random.randint(50, st.session_state.video_width - 50),
            'y': random.randint(50, st.session_state.video_height - 50),
            'collected': False
        })
    st.session_state.start_time = time.time()

# Video processor class for WebRTC
class VideoProcessor:
    def __init__(self):
        self.hands = mp_hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Flip for mirror effect
        img = cv2.flip(img, 1)
        
        # Process with MediaPipe
        rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb_frame)
        
        # Game logic only if playing
        if st.session_state.game_state == 'playing':
            # Draw moonrocks
            for rock in st.session_state.moonrocks:
                if not rock['collected']:
                    cv2.circle(img, (rock['x'], rock['y']), 25, (200, 200, 200), -1)
            
            # Hand tracking
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    # Draw hand landmarks
                    mp_drawing.draw_landmarks(
                        img, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )
                    
                    # Get index finger tip
                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    h, w, _ = img.shape
                    finger_x = int(index_tip.x * w)
                    finger_y = int(index_tip.y * h)
                    
                    # Draw finger position
                    cv2.circle(img, (finger_x, finger_y), 15, (0, 255, 0), -1)
                    
                    # Check collision with moonrocks
                    for rock in st.session_state.moonrocks:
                        if not rock['collected']:
                            dist = np.sqrt((finger_x - rock['x'])**2 + (finger_y - rock['y'])**2)
                            if dist < 40:
                                rock['collected'] = True
                                st.session_state.score += 10
                    
                    # Easter egg detection
                    index_tip_l = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
                    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
                    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
                    ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
                    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
                    
                    # Peace sign detection
                    index_extended = index_tip_l.y < index_pip.y
                    middle_extended = middle_tip.y < middle_pip.y
                    ring_curled = ring_tip.y > ring_mcp.y
                    pinky_curled = pinky_tip.y > pinky_mcp.y
                    
                    current_time = time.time()
                    if (index_extended and middle_extended and ring_curled and pinky_curled and
                        current_time - st.session_state.peace_last_trigger > 5.0):
                        st.session_state.score += 50
                        st.session_state.peace_last_trigger = current_time
                        cv2.putText(img, "PEACE! +50", (50, 100), 
                                  cv2.FONT_HERSHEY_DUPLEX, 2, (34, 197, 94), 3)
            
            # Draw score and time
            elapsed = time.time() - st.session_state.start_time
            remaining = max(0, LEVEL_TIME_LIMIT - elapsed)
            
            cv2.putText(img, f"Score: {st.session_state.score}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(img, f"Time: {int(remaining)}s", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(img, f"Level: {st.session_state.level}", (10, 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Check win condition
            all_collected = all(rock['collected'] for rock in st.session_state.moonrocks)
            if all_collected:
                st.session_state.level += 1
                st.session_state.result_queue.put('level_complete')
            elif remaining <= 0:
                st.session_state.result_queue.put('level_failed')
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Custom CSS
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
    </style>
""", unsafe_allow_html=True)

# Title Screen
if st.session_state.game_state == 'title':
    st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <h1 style="font-size: 4rem; color: #6366f1; text-shadow: 0 0 20px rgba(99, 102, 241, 0.8);">
                🌙 LUNAR LOOT 🌙
            </h1>
            <p style="font-size: 1.5rem; color: #cbd5e1;">
                AI-Powered Hand Tracking Game
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("📷 **Webcam Required** - Click 'Allow' when prompted for camera access")
        
        if st.button("▶ BEGIN GAME", type="primary", use_container_width=True):
            st.session_state.game_state = 'start'
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
            ### 🎯 Mission Objectives:
            - Use your index finger to touch moonrocks
            - Collect all rocks before time runs out
            - Hidden gestures unlock bonus points
            - ✌️ Peace sign = +50 points
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
    
    # WebRTC streamer
    webrtc_ctx = webrtc_streamer(
        key="lunar-loot",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        video_processor_factory=VideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )
    
    # Check for game state changes
    try:
        result = st.session_state.result_queue.get_nowait()
        if result == 'level_complete':
            st.success(f"🎉 Level {st.session_state.level - 1} Complete!")
            reset_level()
            time.sleep(1)
            st.rerun()
        elif result == 'level_failed':
            st.error("⏰ Time's up!")
            st.session_state.game_state = 'end'
            st.rerun()
    except queue.Empty:
        pass
    
    if st.button("⏸️ PAUSE", use_container_width=True):
        st.session_state.game_state = 'title'
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
