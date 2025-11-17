## Lunar Loot - AI-Powered Hand Tracking Game
## Created for Chroma Awards 2025
## Tools: Google MediaPipe, ElevenLabs, Freepik

import cv2
import mediapipe as mp
import numpy as np
import random
import os
import streamlit as st
import time
import base64

# Page configuration
st.set_page_config(
    page_title="Lunar Loot - AI Game",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for sophisticated space-themed UI
st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Color Palette - Space Theme */
    :root {
        --deep-space: #0a0e27;
        --nebula-purple: #6366f1;
        --cosmic-blue: #3b82f6;
        --star-white: #f8fafc;
        --moon-glow: #fbbf24;
        --mars-red: #ef4444;
    }
    
    /* Video container */
    [data-testid="stImage"] {
        border-radius: 8px;
        box-shadow: 0 20px 60px rgba(99, 102, 241, 0.3),
                    0 0 40px rgba(59, 130, 246, 0.2);
        overflow: hidden;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    
    /* Primary buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 14px 36px;
        font-size: 16px;
        font-weight: 600;
        letter-spacing: 0.5px;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.6);
        background: linear-gradient(135deg, #7c3aed 0%, #6366f1 100%);
    }
    
    /* Typography */
    h1 {
        color: #f8fafc !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
        text-shadow: 0 2px 20px rgba(99, 102, 241, 0.5);
    }
    
    h2, h3 {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8);
    }
    
    /* Info boxes */
    .stAlert {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 8px;
        backdrop-filter: blur(12px);
        color: #e2e8f0;
    }
    
    /* Text input */
    .stTextInput > div > div > input {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.4);
        border-radius: 8px;
        color: #f8fafc;
        padding: 12px 16px;
        font-size: 16px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.4);
        color: #e2e8f0;
    }
    
    .stDownloadButton > button:hover {
        background: rgba(99, 102, 241, 0.2);
        border-color: #6366f1;
    }
    
    /* Success/Warning messages */
    .stSuccess {
        background: rgba(34, 197, 94, 0.1);
        border-left: 4px solid #22c55e;
    }
    
    .stWarning {
        background: rgba(251, 191, 36, 0.1);
        border-left: 4px solid #fbbf24;
    }
    </style>
""", unsafe_allow_html=True)

# --- Constants ---
NUM_MOONROCKS = 6
LEVEL_TIME_LIMIT = 30  # Seconds
ANIMATION_DURATION = 5  # Seconds

# --- Find the root directory of the game ---
GAME_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKGROUND_IMAGE_DIR = os.path.join(GAME_ROOT_DIR, "backgrounds", "New_Background_Rotation_1")
ANIMATION_DIR = os.path.join(GAME_ROOT_DIR, "animations")

# --- Helper Functions ---
def play_sound_effect(sound_type="collect"):
    """Play a sound effect using HTML5 audio"""
    sounds = {
        "collect": "https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3",
        "level_complete": "https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3",
        "game_over": "https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3"
    }
    
    if sound_type in sounds:
        return f'<audio autoplay><source src="{sounds[sound_type]}" type="audio/mpeg"></audio>'
    return ""

def get_background_images(directory):
    """Returns a list of paths to background images in the specified directory."""
    try:
        image_files = [os.path.join(directory, f) for f in os.listdir(directory)
                       if f.endswith(('.jpg', '.jpeg', '.png')) and not f.startswith('.')]
        return sorted(image_files)  # Sort for consistent order
    except FileNotFoundError:
        st.error(f"Directory '{directory}' not found. Make sure it exists and contains background images.")
        return []

def select_background_image(image_files):
    """Selects a random background image from the list."""
    if not image_files:
        return None  # Return None if no images are available
    return random.choice(image_files)

def generate_moonrocks(width, height, num_rocks=NUM_MOONROCKS):
    return [(random.randint(50, width - 50), random.randint(50, height - 50)) for _ in range(num_rocks)]

def reset_level():
    """Resets the level, generates moonrocks, and selects a new background image."""
    st.session_state.moonrocks = []
    st.session_state.moonrocks = generate_moonrocks(st.session_state.video_width, st.session_state.video_height)

    # Select and set new background image
    image_files = get_background_images(BACKGROUND_IMAGE_DIR)  # Pass directory
    if image_files:
        st.session_state.background_image = select_background_image(image_files)
    else:
        st.session_state.background_image = None

def display_start_screen():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<h1 style="font-size: 3.5rem; margin-bottom: 0;">Lunar Loot</h1>', unsafe_allow_html=True)
        st.markdown("### Collect cosmic moonrocks before time runs out")
        st.write("")
        
        # Spacetag entry
        spacetag = st.text_input("Enter your Spacetag", 
                                 value=st.session_state.get('spacetag', ''),
                                 max_chars=20,
                                 placeholder="AstroHunter42",
                                 help="Your pilot callsign for the leaderboard")
        if spacetag:
            st.session_state.spacetag = spacetag
        
        st.write("")
        st.markdown("**Mission Objectives:**")
        st.write("• Use your index finger to touch the moonrocks")
        st.write("• Collect all rocks before time runs out")
        st.write("• Progress through levels with new space environments")
        st.write("• Earn bonus points for speed and combos")
        st.write("")
        st.info("⚠️ Camera Required: This game uses your webcam for hand tracking. Please grant camera permissions when prompted by your browser.")
        st.write("")
        st.markdown("**Browser Compatibility:**")
        st.write("• Chrome (Recommended)")
        st.write("• Firefox")
        st.write("• Edge")
        st.write("")
        
        if st.button("Launch Mission", type="primary"):
            if not st.session_state.get('spacetag'):
                st.warning("Please enter a Spacetag to begin")
            else:
                # Before game starts, set the defaults
                st.session_state.score = 0
                st.session_state.level = 1
                st.session_state.combo = 0
                st.session_state.last_collect_time = 0
                st.session_state.selfie_frame = None
                reset_level()  # Generate initial run
                st.session_state.game_state = 'level_start'  # Transition to the level Start Screen
                st.rerun()
        
        st.write("")
        st.write("---")
        st.markdown("**AI Technology Stack:**")
        st.write("• Google MediaPipe — Hand Tracking")
        st.write("• ElevenLabs — Sound Effects")
        st.write("• Freepik — Space Assets")
        st.write("")
        st.markdown("*Created for [Chroma Awards 2025](https://www.chromaawards.com)*")
    
    with col2:
        st.markdown("### Hand Gesture Controls")
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.8); padding: 24px; border-radius: 8px; 
                    border: 1px solid rgba(99, 102, 241, 0.3); backdrop-filter: blur(12px);">
            <h3 style="color: #e2e8f0; font-size: 1.25rem; margin-bottom: 16px;">Control System</h3>
            <p style="font-size: 16px; color: #cbd5e1; line-height: 1.8;">
                <strong style="color: #f8fafc;">Step 1:</strong> Show your hand to the camera<br>
                <strong style="color: #f8fafc;">Step 2:</strong> Point with your index finger<br>
                <strong style="color: #f8fafc;">Step 3:</strong> Touch moonrocks to collect
            </p>
            <div style="background: rgba(99, 102, 241, 0.15); padding: 16px; border-radius: 6px; 
                        margin-top: 16px; border-left: 3px solid #6366f1;">
                <p style="font-size: 14px; margin: 0; color: #e2e8f0;"><strong>Pro Tips</strong></p>
                <p style="font-size: 13px; color: #cbd5e1; margin: 8px 0 0 0; line-height: 1.6;">
                    • Maintain hand visibility in frame<br>
                    • Ensure adequate ambient lighting<br>
                    • Use smooth, deliberate movements
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Visual demo placeholder
        st.markdown("""
        <div style="background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%); 
                    padding: 60px 20px; border-radius: 8px; text-align: center; margin-top: 20px;
                    border: 1px solid rgba(255, 255, 255, 0.1);">
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                <path d="M9 11l3 3L22 4"></path>
                <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"></path>
            </svg>
            <p style="font-size: 20px; color: white; margin: 16px 0 8px 0; font-weight: 600;">Point & Collect</p>
            <p style="font-size: 14px; color: rgba(255,255,255,0.9); margin: 0;">Real-time AI hand tracking</p>
        </div>
        """, unsafe_allow_html=True)

def display_end_screen():
    from enhanced_features import save_high_score, load_high_scores
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<h1 style="font-size: 2.5rem;">Mission Complete</h1>', unsafe_allow_html=True)
        st.write("")
        st.markdown(f"### Pilot: {st.session_state.spacetag}")
        st.markdown(f"### Final Score: {st.session_state.score}")
        st.markdown(f"### Level Reached: {st.session_state.level}")
        st.write("")
        
        # Save high score
        save_high_score(st.session_state.spacetag, st.session_state.score, st.session_state.level)
        
        # Score feedback
        if st.session_state.score >= 100:
            st.success("LEGENDARY PERFORMANCE — Lunar Loot Master")
        elif st.session_state.score >= 50:
            st.success("EXCELLENT WORK — Outstanding piloting skills")
        elif st.session_state.score >= 30:
            st.info("SOLID PERFORMANCE — Room for improvement")
        else:
            st.info("TRAINING COMPLETE — Practice makes perfect")
        
        st.write("")
        if st.button("New Mission", type="primary"):
            # Reset the game
            st.session_state.score = 0
            st.session_state.level = 1
            st.session_state.combo = 0
            st.session_state.selfie_frame = None
            st.session_state.game_state = 'start'
            st.rerun()
        
        st.write("")
        st.write("---")
        st.markdown("**Share Your Achievement**")
        
        # Social share buttons
        tweet_text = f"I scored {st.session_state.score} points in Lunar Loot! Can you beat my score?"
        st.markdown(f"""
        <a href="https://twitter.com/intent/tweet?text={tweet_text.replace(' ', '%20')}&hashtags=LunarLoot,ChromaAwards" 
           target="_blank" style="text-decoration: none;">
            <button style="background: #1DA1F2; color: white; border: 1px solid rgba(255,255,255,0.2); 
                           padding: 12px 24px; border-radius: 8px; cursor: pointer; font-size: 14px;
                           font-weight: 600; transition: all 0.3s;">
                Share on Twitter
            </button>
        </a>
        """, unsafe_allow_html=True)
    
    with col2:
        # Display space selfie if available
        if st.session_state.get('selfie_frame') is not None:
            st.markdown("### Mission Snapshot")
            st.image(st.session_state.selfie_frame, use_container_width=True)
            
            # Download button
            import cv2
            _, buffer = cv2.imencode('.jpg', st.session_state.selfie_frame)
            st.download_button(
                label="Download Image",
                data=buffer.tobytes(),
                file_name=f"lunar_loot_{st.session_state.spacetag}.jpg",
                mime="image/jpeg"
            )
        
        # Leaderboard
        st.write("")
        st.markdown("### Top Pilots")
        scores = load_high_scores()
        if scores:
            medals = ["1st", "2nd", "3rd"]
            for i, entry in enumerate(scores[:10], 1):
                rank = medals[i-1] if i <= 3 else f"{i}th"
                is_current = entry['spacetag'] == st.session_state.spacetag and entry['score'] == st.session_state.score
                highlight = "**" if is_current else ""
                st.write(f"{rank} — {highlight}{entry['spacetag']}{highlight} — {entry['score']} pts (Level {entry['level']})")
        else:
            st.info("Leaderboard empty — Be the first pilot")
    
    st.write("")
    st.write("---")
    st.markdown("🏆 *Submitted to [Chroma Awards 2025](https://www.chromaawards.com)*")


def display_level_transition_animation():
    """Displays a level transition animation using HTML5 video tag with autoplay."""
    
    # Enhanced level complete screen
    st.markdown("""
        <style>
        .level-complete {
            text-align: center;
            padding: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            margin: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="level-complete">', unsafe_allow_html=True)
        st.title("Level Complete")
        st.markdown(f"### Level {st.session_state.level}")
        st.markdown(f"**Current Score: {st.session_state.score}**")
        
        if st.session_state.combo > 0:
            st.success(f"Maximum Combo: x{st.session_state.combo + 1}")
        
        st.write("")
        st.write("Preparing next sector...")
        st.markdown('</div>', unsafe_allow_html=True)

    if 'animation_bytes' in st.session_state:
        video_html = f"""
        <div style="text-align: center; margin: 20px 0;">
            <video width="400" height="300" autoplay muted loop style="border-radius: 15px;">
                <source src="data:video/mp4;base64,{st.session_state.animation_bytes.decode()}" type="video/mp4">
            </video>
        </div>
        """
        st.markdown(video_html, unsafe_allow_html=True)

    time.sleep(3)  # Shorter wait time

    st.session_state.level += 1  # Increment level counter
    st.session_state.combo = 0  # Reset combo for new level
    st.session_state.game_state = 'level_start'  # Go to the level Start Screen
    reset_level()
    st.rerun()


def display_level_start_screen():
    """Displays the level start screen with the background and 'Begin Game' button."""
    if 'background_image_bytes' in st.session_state and st.session_state.background_image_bytes is not None:
        full_screen_background(st.session_state.background_image_bytes)
    
    # Add simple background music
    st.markdown("""
        <audio autoplay loop volume="0.3">
            <source src="https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3" type="audio/mpeg">
        </audio>
    """, unsafe_allow_html=True)

    # Enhanced level start screen
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="background: rgba(0,0,0,0.8); padding: 40px; border-radius: 20px; 
                        text-align: center; backdrop-filter: blur(10px);">
        """, unsafe_allow_html=True)
        
        st.title(f"Level {st.session_state.level}")
        
        # Get background name for display
        if st.session_state.background_image:
            bg_name = os.path.basename(st.session_state.background_image).replace('_1.png', '').replace('_', ' ')
            st.markdown(f"### Sector: {bg_name}")
        
        st.write("")
        st.markdown(f"**Current Score: {st.session_state.score}**")
        st.markdown(f"**Pilot: {st.session_state.spacetag}**")
        st.write("")
        st.info("Tip: Collect moonrocks quickly to build combo multipliers")
        st.write("")
        
        if st.button("Begin Mission", type="primary", use_container_width=True):
            st.session_state.game_state = 'playing'  # Now start the level
            st.session_state.start_time = time.time()  # Resets time
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)


# --- Streamlit Full Screen Background Component ---
def full_screen_background(image_bytes):
    """Displays an image as a full-screen background with consistent overlay."""
    st.markdown(
        f"""
        <style>
        .fullScreen {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url(data:image/jpg;base64,{image_bytes.decode()});
            background-size: cover;
            background-position: center;
            z-index: -1;
        }}
        
        /* Consistent dark overlay for better text readability */
        .fullScreen::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.4);
            z-index: 1;
        }}
        
        /* Ensure content is above overlay */
        .stApp > header,
        .stApp [data-testid="stMainBlockContainer"] {{
            position: relative;
            z-index: 2;
        }}
        
        /* Better text contrast */
        .stMarkdown, .stTitle, .stWrite {{
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        }}
        </style>
        <div class="fullScreen" />
        """,
        unsafe_allow_html=True,
    )


def convert_image_to_bytes(image_path):
    """Convert image to bytes for embedding in CSS."""
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            return encoded_string
    except FileNotFoundError:
        st.error(f"Background image '{image_path}' not found.")
        return None


# --- Initialize Streamlit Session State ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'start'  # 'start', 'playing', 'level_transition', 'end', 'level_start'
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0
if 'moonrocks' not in st.session_state:
    st.session_state.moonrocks = []
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'background_image' not in st.session_state:
    st.session_state.background_image = None
if 'video_width' not in st.session_state:
    st.session_state.video_width = 0
if 'video_height' not in st.session_state:
    st.session_state.video_height = 0
if 'background_image_bytes' not in st.session_state:
    st.session_state.background_image_bytes = None
# New features
if 'spacetag' not in st.session_state:
    st.session_state.spacetag = ""
if 'combo' not in st.session_state:
    st.session_state.combo = 0
if 'last_collect_time' not in st.session_state:
    st.session_state.last_collect_time = 0
if 'selfie_frame' not in st.session_state:
    st.session_state.selfie_frame = None
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0

#Added encoding
if 'animation_bytes' not in st.session_state:
    try:
        with open(os.path.join(ANIMATION_DIR, 'rocketship1.mp4'), 'rb') as video_file:
            encoded_string = base64.b64encode(video_file.read())
            st.session_state.animation_bytes = encoded_string
    except FileNotFoundError:
        st.error("Animation file not found. Check your directory")

# --- Camera Setup & Initialization ---
if 'cap' not in st.session_state and st.session_state.game_state == 'playing':
    if 'OPENCV_AVFOUNDATION_SKIP_AUTH' not in os.environ:
        print("Warning: OPENCV_AVFOUNDATION_SKIP_AUTH not set. Camera auth may fail.")

    st.session_state.cap = cv2.VideoCapture(0)
    if not st.session_state.cap.isOpened():
        st.error("Camera access required. Please grant camera permissions in your browser and refresh the page.")
        st.info("Note: This game requires a webcam to play. Make sure your browser has camera permissions enabled.")
        st.stop()  # Stop execution

    st.session_state.video_width = int(st.session_state.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    st.session_state.video_height = int(st.session_state.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if st.session_state.video_width == 0 or st.session_state.video_width == 0:
        st.session_state.video_width, st.session_state.video_height = 640, 480

    reset_level()  # Generate initial run

# --- Load Moonrock Image ---
moonrock_img = cv2.imread("moonrock.png", cv2.IMREAD_UNCHANGED)
if moonrock_img is None:
    st.error("Could not load moonrock.png. Ensure it exists.")
    st.stop()
moonrock_size = 50
moonrock_img = cv2.resize(moonrock_img, (moonrock_size, moonrock_size), interpolation=cv2.INTER_AREA)

# --- Mediapipe Setup ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# --- Image Overlay Function ---
def overlay_image(frame, img, x, y):
    h, w, _ = img.shape
    alpha_channel = img[:, :, 3] / 255.0  # Normalize alpha
    for i in range(h):
        for j in range(w):
            if alpha_channel[i, j] > 0:
                frame[y + i, x + j] = (alpha_channel[i, j] * img[i, j][:3] +
                                        (1 - alpha_channel[i, j]) * frame[y + i, x + j]).astype(frame.dtype)

# --- Main Game Loop ---
image_placeholder = st.empty()  # Placeholder for the video feed

if st.session_state.game_state == 'start':
    display_start_screen()
elif st.session_state.game_state == 'level_transition':
    display_level_transition_animation()
elif st.session_state.game_state == 'level_start':
    if st.session_state.background_image:
        background_image_bytes = convert_image_to_bytes(st.session_state.background_image)
        if background_image_bytes:
            st.session_state.background_image_bytes = background_image_bytes
    display_level_start_screen()  # Displays initial scene

elif st.session_state.game_state == 'playing':
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils
    # Add the full screen background image behind everything
    if st.session_state.background_image:
        background_image_bytes = convert_image_to_bytes(st.session_state.background_image)
        if background_image_bytes:
            st.session_state.background_image_bytes = background_image_bytes
            full_screen_background(st.session_state.background_image_bytes)
    
    # Add info about the dynamic overlay
    st.markdown("""
        <div style="position: fixed; bottom: 10px; right: 10px; 
                    background: rgba(15, 23, 42, 0.9); 
                    padding: 12px 16px; border-radius: 8px; font-size: 12px; z-index: 1000;
                    border: 1px solid rgba(99, 102, 241, 0.3);
                    backdrop-filter: blur(12px);
                    color: #cbd5e1;">
            Background overlay intensifies with collection progress
        </div>
    """, unsafe_allow_html=True)

    while st.session_state.cap.isOpened() and st.session_state.game_state == 'playing':  # keep the main loop here

        ret, frame = st.session_state.cap.read()
        if not ret:
            st.warning("End of stream or error reading frame.")
            st.session_state.game_state = 'end'
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        # Time Handling
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = max(0, LEVEL_TIME_LIMIT - elapsed_time)
        if remaining_time == 0:
            st.session_state.game_state = 'end'
            break

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                fx, fy = int(index_finger.x * st.session_state.video_width), int(index_finger.y * st.session_state.video_height)  # Capture video width and height from session state
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Collection logic with combo system
                for rock in list(st.session_state.moonrocks):  # Iterate over a copy
                    rx, ry = rock
                    if abs(fx - rx) < 30 and abs(fy - ry) < 30:
                        st.session_state.moonrocks.remove(rock)
                        
                        # Combo system
                        current_time = time.time()
                        time_since_last = current_time - st.session_state.last_collect_time
                        
                        if time_since_last < 2.0 and st.session_state.last_collect_time > 0:  # Within 2 seconds = combo
                            st.session_state.combo += 1
                        else:
                            st.session_state.combo = 0
                        
                        # Calculate points
                        base_points = 10
                        combo_bonus = st.session_state.combo * 5
                        total_points = base_points + combo_bonus
                        
                        st.session_state.score += total_points
                        st.session_state.last_collect_time = current_time
                        
                        if not st.session_state.moonrocks:  # Level Complete
                            # Capture selfie frame
                            from enhanced_features import create_space_selfie
                            st.session_state.selfie_frame = create_space_selfie(
                                frame, st.session_state.score, st.session_state.level, st.session_state.spacetag
                            )
                            
                            # Time bonus
                            time_bonus = int(remaining_time * 2)
                            st.session_state.score += time_bonus
                            
                            st.session_state.game_state = 'level_transition'  # Go to level transition
                            st.rerun()
                            break  # VERY IMPORTANT BREAK THE GAME OR IT WONT GET STUCK

        # Add semi-transparent background overlay that changes with collection progress
        if st.session_state.background_image:
            # Calculate transparency based on moonrocks collected
            total_rocks = NUM_MOONROCKS
            collected = total_rocks - len(st.session_state.moonrocks)
            # Start at 25% opacity, increase to 60% as you collect more
            overlay_alpha = 0.25 + (collected / total_rocks) * 0.35
            
            # Load and resize background for overlay
            try:
                bg_overlay = cv2.imread(st.session_state.background_image, cv2.IMREAD_COLOR)
                if bg_overlay is not None:
                    bg_overlay = cv2.resize(bg_overlay, (frame.shape[1], frame.shape[0]))
                    # Blend background with frame
                    frame = cv2.addWeighted(frame, 1 - overlay_alpha, bg_overlay, overlay_alpha, 0)
            except:
                pass  # If background fails to load, continue without overlay
        
        # Drawing moonrocks
        for rx, ry in st.session_state.moonrocks:
            overlay_image(frame, moonrock_img, rx, ry)

        # Enhanced HUD with better styling
        cv2.putText(frame, f"{st.session_state.spacetag}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"Score: {st.session_state.score}", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"Time: {int(remaining_time)}", (10, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"Level: {st.session_state.level}", (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"Rocks: {len(st.session_state.moonrocks)}", (10, 190),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Show combo if active
        if st.session_state.combo > 0:
            cv2.putText(frame, f"COMBO x{st.session_state.combo + 1}!", (10, 230),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 100), 2, cv2.LINE_AA)

        image_placeholder.image(frame, channels="BGR", caption="Lunar Loot", use_container_width=True)

    # Game Over Handling if loop breaks
    if st.session_state.game_state == 'end':
        display_end_screen()

# --- Release Resources ---
# Relocate this part to avoid repeated camera releases. Put after the main game loop.
if st.session_state.game_state != 'playing' and 'cap' in st.session_state:
    st.session_state.cap.release()
    del st.session_state['cap']  # Remove cap from session state
    print("Camera released (if it was open).")



