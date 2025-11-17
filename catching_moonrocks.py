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

# Custom CSS for better visuals
st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Better video container */
    [data-testid="stImage"] {
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
        overflow: hidden;
    }
    
    /* Better buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 32px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 25px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Better text styling */
    h1, h2, h3 {
        color: white !important;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.9);
    }
    
    /* Info boxes */
    .stAlert {
        background: rgba(0, 0, 0, 0.6);
        border-radius: 10px;
        backdrop-filter: blur(10px);
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
        st.title("🌙 Lunar Loot")
        st.markdown("### Collect cosmic moonrocks before time runs out!")
        st.write("")
        
        # Spacetag entry
        spacetag = st.text_input("🚀 Enter your Spacetag:", 
                                 value=st.session_state.get('spacetag', ''),
                                 max_chars=20,
                                 placeholder="AstroHunter42",
                                 help="Your gamer name for the leaderboard!")
        if spacetag:
            st.session_state.spacetag = spacetag
        
        st.write("")
        st.write("**How to Play:**")
        st.write("👆 Use your index finger to touch the moonrocks")
        st.write("⏱️ Collect all rocks before time runs out")
        st.write("🚀 Progress through levels with new space backgrounds")
        st.write("⭐ Earn bonus points for speed and combos!")
        st.write("")
        st.info("💡 Make sure your webcam is enabled and you have good lighting!")
        st.write("")
        
        if st.button("🎮 Start Game", type="primary"):
            if not st.session_state.get('spacetag'):
                st.warning("⚠️ Please enter a Spacetag first!")
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
        st.markdown("**🤖 AI-Powered by:**")
        st.write("• Google MediaPipe - Hand Tracking")
        st.write("• ElevenLabs - Sound Effects")
        st.write("• Freepik - Space Assets")
        st.write("")
        st.markdown("🏆 *Created for [Chroma Awards 2025](https://www.chromaawards.com)*")
    
    with col2:
        st.markdown("### 🎯 Hand Gesture Demo")
        st.markdown("""
        <div style="background: rgba(0,0,0,0.7); padding: 20px; border-radius: 15px; text-align: center;">
            <h3 style="color: #667eea;">How to Control</h3>
            <p style="font-size: 18px;">✋ Show your hand to the camera</p>
            <p style="font-size: 18px;">👆 Point with your index finger</p>
            <p style="font-size: 18px;">🎯 Touch the moonrocks to collect them</p>
            <br>
            <div style="background: rgba(102, 126, 234, 0.3); padding: 15px; border-radius: 10px; margin: 10px 0;">
                <p style="font-size: 16px; margin: 5px;">💡 <strong>Pro Tips:</strong></p>
                <p style="font-size: 14px;">• Keep your hand in frame</p>
                <p style="font-size: 14px;">• Use good lighting</p>
                <p style="font-size: 14px;">• Move smoothly for best tracking</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Placeholder for demo video/GIF (can be replaced with actual demo)
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 80px 20px; border-radius: 15px; text-align: center; margin-top: 20px;">
            <p style="font-size: 48px; margin: 0;">👆</p>
            <p style="font-size: 24px; color: white; margin: 10px 0;">Point & Collect</p>
            <p style="font-size: 14px; color: rgba(255,255,255,0.8);">AI tracks your hand in real-time</p>
        </div>
        """, unsafe_allow_html=True)

def display_end_screen():
    from enhanced_features import save_high_score, load_high_scores
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.title("🎮 Game Over!")
        st.write("")
        st.markdown(f"### 👤 {st.session_state.spacetag}")
        st.markdown(f"### 🏆 Final Score: {st.session_state.score}")
        st.markdown(f"### 🚀 Level Reached: {st.session_state.level}")
        st.write("")
        
        # Save high score
        save_high_score(st.session_state.spacetag, st.session_state.score, st.session_state.level)
        
        # Score feedback
        if st.session_state.score >= 100:
            st.success("🌟 LEGENDARY! You're a lunar loot master!")
        elif st.session_state.score >= 50:
            st.success("⭐ Amazing! Keep up the great work!")
        elif st.session_state.score >= 30:
            st.info("👍 Good job! Try for a higher score!")
        else:
            st.info("💪 Keep practicing! You'll get better!")
        
        st.write("")
        if st.button("🔄 Play Again", type="primary"):
            # Reset the game
            st.session_state.score = 0
            st.session_state.level = 1
            st.session_state.combo = 0
            st.session_state.selfie_frame = None
            st.session_state.game_state = 'start'
            st.rerun()
        
        st.write("")
        st.write("---")
        st.markdown("**Share your score!** 🎯")
        
        # Social share buttons
        tweet_text = f"I scored {st.session_state.score} points in Lunar Loot! 🌙 Can you beat my score?"
        st.markdown(f"""
        <a href="https://twitter.com/intent/tweet?text={tweet_text.replace(' ', '%20')}&hashtags=LunarLoot,ChromaAwards" 
           target="_blank" style="text-decoration: none;">
            <button style="background: #1DA1F2; color: white; border: none; padding: 10px 20px; 
                           border-radius: 20px; cursor: pointer; font-size: 14px;">
                🐦 Share on Twitter
            </button>
        </a>
        """, unsafe_allow_html=True)
    
    with col2:
        # Display space selfie if available
        if st.session_state.get('selfie_frame') is not None:
            st.markdown("### 📸 Your Space Selfie!")
            st.image(st.session_state.selfie_frame, use_container_width=True)
            
            # Download button
            import cv2
            _, buffer = cv2.imencode('.jpg', st.session_state.selfie_frame)
            st.download_button(
                label="📥 Download Selfie",
                data=buffer.tobytes(),
                file_name=f"lunar_loot_{st.session_state.spacetag}.jpg",
                mime="image/jpeg"
            )
        
        # Leaderboard
        st.write("")
        st.markdown("### 🏆 Top Spacetags")
        scores = load_high_scores()
        if scores:
            for i, entry in enumerate(scores[:10], 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                is_current = entry['spacetag'] == st.session_state.spacetag and entry['score'] == st.session_state.score
                highlight = "**" if is_current else ""
                st.write(f"{medal} {highlight}{entry['spacetag']}{highlight} - {entry['score']} pts (Lvl {entry['level']})")
        else:
            st.info("No high scores yet. Be the first!")
    
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
        st.title("🎉 Level Complete!")
        st.markdown(f"### Level {st.session_state.level}")
        st.markdown(f"**Score: {st.session_state.score}**")
        
        if st.session_state.combo > 0:
            st.success(f"🔥 Max Combo: x{st.session_state.combo + 1}!")
        
        st.write("")
        st.write("🚀 Preparing next level...")
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
        
        st.title(f"🚀 Level {st.session_state.level}")
        
        # Get background name for display
        if st.session_state.background_image:
            bg_name = os.path.basename(st.session_state.background_image).replace('_1.png', '').replace('_', ' ')
            st.markdown(f"### 🌌 {bg_name}")
        
        st.write("")
        st.markdown(f"**Current Score: {st.session_state.score}**")
        st.markdown(f"**Spacetag: {st.session_state.spacetag}**")
        st.write("")
        st.info("💡 Collect moonrocks quickly for combo bonuses!")
        st.write("")
        
        if st.button("▶️ Begin Game", type="primary", use_container_width=True):
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
if 'cap' not in st.session_state:
    if 'OPENCV_AVFOUNDATION_SKIP_AUTH' not in os.environ:
        print("Warning: OPENCV_AVFOUNDATION_SKIP_AUTH not set. Camera auth may fail.")

    st.session_state.cap = cv2.VideoCapture(0)
    if not st.session_state.cap.isOpened():
        st.error("Cannot open camera. Check permissions.")
        st.stop()  # Stop execution

    st.session_state.video_width = int(st.session_state.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    st.session_state.video_height = int(st.session_state.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if st.session_state.video_width == 0 or st.session_state.video_width == 0:
        st.session_state.video_width, st.session_state.video_height = 640, 480
        st.warning(f"Width/height are zero, defaulting to {st.session_state.video_width}x{st.session_state.video_height}")

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
    #add the full screen background image here
    if st.session_state.background_image:
        background_image_bytes = convert_image_to_bytes(st.session_state.background_image)
        if background_image_bytes:
            st.session_state.background_image_bytes = background_image_bytes
            full_screen_background(st.session_state.background_image_bytes)

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

        # Drawing and Display
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



