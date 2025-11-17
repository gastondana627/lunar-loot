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

# Mobile detection and warning
st.markdown("""
    <script>
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        document.body.innerHTML = '<div style="display: flex; align-items: center; justify-content: center; height: 100vh; background: #0a0e27; color: white; text-align: center; padding: 20px;"><div><h1>🌙 Lunar Loot</h1><p style="font-size: 18px; margin: 20px 0;">This game requires a desktop computer with a webcam for hand tracking.</p><p>Please visit on a desktop browser:</p><p style="color: #6366f1;">• Chrome (Recommended)<br>• Firefox<br>• Edge</p></div></div>';
    }
    </script>
""", unsafe_allow_html=True)

# Custom CSS for sophisticated space-themed UI
st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Chroma Awards Footer Badge */
    .chroma-badge {
        position: fixed;
        bottom: 10px;
        right: 10px;
        background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%);
        padding: 8px 16px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
        z-index: 9999;
    }
    
    .chroma-badge a {
        color: #fbbf24;
        text-decoration: none;
        font-size: 12px;
        font-weight: 600;
    }
    
    .chroma-badge span {
        color: white;
        font-size: 12px;
    }
    
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
    
    /* Disable browser text detection on images */
    [data-testid="stImage"] img {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        pointer-events: none;
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

# --- Load and display Chroma Awards footer video ---
chroma_footer_path = os.path.join(GAME_ROOT_DIR, "backgrounds", "Main_Menu", "Footer_Chroma_Awards.mp4")
if os.path.exists(chroma_footer_path):
    try:
        with open(chroma_footer_path, 'rb') as video_file:
            footer_video_bytes = base64.b64encode(video_file.read()).decode()
            st.markdown(f"""
                <a href="https://www.chromaawards.com" target="_blank" style="text-decoration: none;">
                    <div style="position: fixed; bottom: 0; left: 0; width: 100%; z-index: 9998; 
                                background: rgba(0,0,0,0.9); box-shadow: 0 -4px 12px rgba(0,0,0,0.5);
                                cursor: pointer; transition: all 0.3s ease;">
                        <video width="100%" height="50" autoplay loop muted playsinline 
                               style="display: block; object-fit: cover; pointer-events: none;">
                            <source src="data:video/mp4;base64,{footer_video_bytes}" type="video/mp4">
                        </video>
                    </div>
                </a>
            """, unsafe_allow_html=True)
    except Exception as e:
        print(f"Error loading footer video: {e}")

# --- Helper Functions ---
def play_sound_effect(sound_type="collect_1"):
    """
    Play a sound effect using HTML5 audio
    
    TWO TYPES OF AUDIO:
    1. Sound Effects (beeps/clicks) - Free online sounds (always available)
    2. AI Voice Announcements - ElevenLabs generated (optional, in sounds/ folder)
    
    Sound effects: collect_1, collect_2, collect_3, level_complete, etc.
    Voice announcements: level_01_earth, level_02_halley, etc.
    """
    # Check if local ElevenLabs AI voice exists (for level announcements)
    local_sound_path = os.path.join(GAME_ROOT_DIR, "sounds", f"{sound_type}.mp3")
    
    if os.path.exists(local_sound_path):
        # Use local AI voice file
        try:
            import base64
            with open(local_sound_path, 'rb') as audio_file:
                audio_bytes = base64.b64encode(audio_file.read()).decode()
                return f'<audio autoplay preload="auto"><source src="data:audio/mpeg;base64,{audio_bytes}" type="audio/mpeg"></audio>'
        except:
            pass
    
    # Fallback to online sound effects (always available)
    sounds = {
        # Collection sounds (short beeps)
        "collect_1": "https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3",
        "collect_2": "https://assets.mixkit.co/active_storage/sfx/2000/2000-preview.mp3",
        "collect_3": "https://assets.mixkit.co/active_storage/sfx/2019/2019-preview.mp3",
        
        # Game events
        "level_complete": "https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3",
        "game_over": "https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3",
        "time_warning_10": "https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3",
        "time_warning_5": "https://assets.mixkit.co/active_storage/sfx/2870/2870-preview.mp3",
        "high_score": "https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3",
    }
    
    if sound_type in sounds:
        return f'<audio autoplay preload="auto"><source src="{sounds[sound_type]}" type="audio/mpeg"></audio>'
    
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
    # Ensure valid dimensions
    if width <= 100:
        width = 640
    if height <= 100:
        height = 480
    return [(random.randint(50, width - 50), random.randint(50, height - 50)) for _ in range(num_rocks)]

def reset_level():
    """Resets the level, generates moonrocks, and selects a new background image."""
    st.session_state.moonrocks = []
    st.session_state.last_warning_time = 0  # Reset time warnings
    st.session_state.collect_sound_index = 0  # Reset sound cycling
    
    # Ensure video dimensions are set
    if not hasattr(st.session_state, 'video_width') or st.session_state.video_width == 0:
        st.session_state.video_width = 640
        st.session_state.video_height = 480
    
    st.session_state.moonrocks = generate_moonrocks(st.session_state.video_width, st.session_state.video_height)

    # Select and set new background image
    image_files = get_background_images(BACKGROUND_IMAGE_DIR)  # Pass directory
    if image_files:
        st.session_state.background_image = select_background_image(image_files)
    else:
        st.session_state.background_image = None

def display_start_screen():
    # Load and display main menu background
    main_menu_bg = os.path.join(GAME_ROOT_DIR, "backgrounds", "Main_Menu", "Main_Menu_Start_Screen_BG.png")
    
    # Try to load and display background
    if os.path.exists(main_menu_bg):
        try:
            bg_bytes = convert_image_to_bytes(main_menu_bg)
            if bg_bytes:
                st.markdown(f"""
                    <style>
                    .stApp {{
                        background-image: url(data:image/png;base64,{bg_bytes.decode()});
                        background-size: cover;
                        background-position: center;
                        background-attachment: fixed;
                    }}
                    </style>
                """, unsafe_allow_html=True)
        except Exception as e:
            print(f"Error loading background: {e}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Enhanced title with better styling for background
        st.markdown("""
            <div style="background: rgba(10, 14, 39, 0.85); padding: 30px; border-radius: 12px; 
                        border: 1px solid rgba(99, 102, 241, 0.3); backdrop-filter: blur(12px);
                        margin-bottom: 20px;">
                <h1 style="font-size: 3.5rem; margin: 0; color: #f8fafc; 
                           text-shadow: 0 0 20px rgba(99, 102, 241, 0.8);">
                    Lunar Loot
                </h1>
                <p style="font-size: 1.25rem; color: #cbd5e1; margin: 10px 0 0 0;">
                    Collect cosmic moonrocks before time runs out
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Spacetag entry with enhanced styling
        st.markdown('<p style="color: #e2e8f0; font-weight: 600; margin-bottom: 8px;">Enter your Spacetag</p>', 
                    unsafe_allow_html=True)
        spacetag = st.text_input("Enter your Spacetag", 
                                 value=st.session_state.get('spacetag', ''),
                                 max_chars=20,
                                 placeholder="AstroHunter42",
                                 help="Your pilot callsign for the leaderboard",
                                 label_visibility="collapsed")
        if spacetag:
            st.session_state.spacetag = spacetag
        
        st.write("")
        
        # Mission objectives in styled box
        st.markdown("""
            <div style="background: rgba(10, 14, 39, 0.85); padding: 20px; border-radius: 12px; 
                        border: 1px solid rgba(99, 102, 241, 0.3); backdrop-filter: blur(12px);
                        margin: 20px 0;">
                <p style="color: #f8fafc; font-weight: 600; font-size: 1.1rem; margin-bottom: 12px;">
                    Mission Objectives:
                </p>
                <p style="color: #cbd5e1; line-height: 1.8; margin: 0;">
                    • Use your index finger to touch the moonrocks<br>
                    • Collect all rocks before time runs out<br>
                    • Progress through levels with new space environments<br>
                    • Earn bonus points for speed and combos
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Camera warning
        st.info("Camera Required: This game uses your webcam for hand tracking. Please grant camera permissions when prompted.")
        
        # Browser compatibility
        st.markdown("""
            <div style="background: rgba(10, 14, 39, 0.7); padding: 15px; border-radius: 8px; 
                        border-left: 3px solid #6366f1; margin: 15px 0;">
                <p style="color: #e2e8f0; font-weight: 600; margin-bottom: 8px;">Browser Compatibility:</p>
                <p style="color: #cbd5e1; margin: 0; line-height: 1.6;">
                    • Chrome (Recommended)<br>
                    • Firefox<br>
                    • Edge<br>
                    • Desktop only (mobile not supported)
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        if st.button("Launch Mission", type="primary"):
            if not st.session_state.get('spacetag'):
                st.warning("Please enter a Spacetag to begin")
            else:
                # Enable audio by user interaction (browser autoplay policy)
                st.markdown("""
                    <script>
                    // Enable audio context on user interaction
                    document.addEventListener('click', function() {
                        var audio = new Audio();
                        audio.play().catch(e => console.log('Audio enabled'));
                    }, { once: true });
                    </script>
                """, unsafe_allow_html=True)
                
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
        
        # AI Technology Stack
        st.markdown("""
<div style="background: rgba(10, 14, 39, 0.7); padding: 15px; border-radius: 8px; margin: 15px 0;">
    <p style="color: #e2e8f0; font-weight: 600; margin-bottom: 8px;">AI Technology Stack:</p>
    <p style="color: #cbd5e1; margin: 0; line-height: 1.6;">
        • Google MediaPipe — Hand Tracking<br>
        • ElevenLabs — Sound Effects<br>
        • Freepik — Space Assets
    </p>
</div>
        """, unsafe_allow_html=True)
        

    
    with col2:
        # Hand Gesture Controls box
        hand_control_html = """
<div style="background: rgba(10, 14, 39, 0.85); padding: 24px; border-radius: 12px; border: 1px solid rgba(99, 102, 241, 0.3); backdrop-filter: blur(12px);">
    <h3 style="color: #f8fafc; font-size: 1.5rem; margin-bottom: 20px; text-shadow: 0 0 10px rgba(99, 102, 241, 0.5);">Hand Gesture Controls</h3>
    <div style="margin-bottom: 20px;">
        <p style="color: #e2e8f0; font-weight: 600; margin-bottom: 12px;">Control System</p>
        <p style="font-size: 16px; color: #cbd5e1; line-height: 2;">
            <strong style="color: #6366f1;">Step 1:</strong> Show your hand to the camera<br>
            <strong style="color: #6366f1;">Step 2:</strong> Point with your index finger<br>
            <strong style="color: #6366f1;">Step 3:</strong> Touch moonrocks to collect
        </p>
    </div>
    <div style="background: rgba(99, 102, 241, 0.15); padding: 16px; border-radius: 8px; border-left: 3px solid #6366f1;">
        <p style="font-size: 14px; margin: 0 0 10px 0; color: #f8fafc; font-weight: 600;">Pro Tips</p>
        <p style="font-size: 13px; color: #cbd5e1; margin: 0; line-height: 1.8;">
            • Maintain hand visibility in frame<br>
            • Ensure adequate ambient lighting<br>
            • Use smooth, deliberate movements
        </p>
    </div>
</div>
"""
        st.markdown(hand_control_html, unsafe_allow_html=True)
        
        st.write("")
        
        # Visual demo box
        demo_html = """
<div style="background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%); padding: 50px 20px; border-radius: 12px; text-align: center; margin-top: 20px; border: 1px solid rgba(255, 255, 255, 0.2); box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4);">
    <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
        <path d="M9 11l3 3L22 4"></path>
        <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"></path>
    </svg>
    <p style="font-size: 22px; color: white; margin: 20px 0 8px 0; font-weight: 700;">Point & Collect</p>
    <p style="font-size: 14px; color: rgba(255,255,255,0.95); margin: 0;">Real-time AI hand tracking</p>
</div>
"""
        st.markdown(demo_html, unsafe_allow_html=True)

def display_end_screen():
    from enhanced_features import save_high_score, load_high_scores
    
    # Check if this is a high score
    scores = load_high_scores()
    is_high_score = len(scores) == 0 or st.session_state.score > scores[0]['score']
    
    # Play appropriate sound
    if is_high_score:
        sound_html = play_sound_effect("high_score")
    else:
        sound_html = play_sound_effect("game_over")
    
    if sound_html:
        st.markdown(sound_html, unsafe_allow_html=True)
    
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
        
        # Show high score badge if applicable
        if is_high_score:
            st.success("🏆 NEW HIGH SCORE! 🏆")
        
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
            # Reset the game completely and release camera
            if 'cap' in st.session_state:
                try:
                    st.session_state.cap.release()
                except:
                    pass
                del st.session_state['cap']
            
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            
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
            st.markdown("### 📸 Mission Snapshot")
            st.image(st.session_state.selfie_frame, use_container_width=True)
            
            # Download button
            import cv2
            _, buffer = cv2.imencode('.jpg', st.session_state.selfie_frame)
            st.download_button(
                label="💾 Download Snapshot",
                data=buffer.tobytes(),
                file_name=f"lunar_loot_{st.session_state.spacetag}.jpg",
                mime="image/jpeg",
                use_container_width=True
            )
        else:
            # Debug: Show why selfie isn't available
            st.info("📷 No snapshot captured - complete at least one level to get your mission photo!")
        
        # Leaderboard
        st.write("")
        st.markdown("### 🏆 Top Pilots")
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
    """Displays a level transition animation - quick transition between levels."""
    
    # Simple level complete screen
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="background: rgba(10, 14, 39, 0.9); padding: 40px; border-radius: 12px; 
                        border: 1px solid rgba(99, 102, 241, 0.4); backdrop-filter: blur(12px);
                        text-align: center;">
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h1 style='color: #22c55e; margin: 0 0 20px 0;'>🎉 Level {st.session_state.level} Complete!</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #f8fafc; font-size: 20px; margin: 10px 0;'><strong>Score:</strong> {st.session_state.score}</p>", unsafe_allow_html=True)
        
        if st.session_state.combo > 0:
            st.markdown(f"<p style='color: #22c55e; font-size: 18px; margin: 10px 0;'>Maximum Combo: x{st.session_state.combo + 1}</p>", unsafe_allow_html=True)
        
        st.write("")
        st.info("🚀 Preparing next sector...")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Animation if available
        if 'animation_bytes' in st.session_state:
            video_html = f"""
            <div style="text-align: center; margin: 20px 0;">
                <video width="400" height="300" autoplay muted loop style="border-radius: 12px;">
                    <source src="data:video/mp4;base64,{st.session_state.animation_bytes.decode()}" type="video/mp4">
                </video>
            </div>
            """
            st.markdown(video_html, unsafe_allow_html=True)

    time.sleep(2)  # Quick transition

    st.session_state.level += 1  # Increment level counter
    st.session_state.combo = 0  # Reset combo for new level
    st.session_state.game_state = 'level_start'  # Go to the level Start Screen
    reset_level()
    st.rerun()


def display_level_start_screen():
    """Displays the level start screen with the background and 'Begin Game' button."""
    if 'background_image_bytes' in st.session_state and st.session_state.background_image_bytes is not None:
        full_screen_background(st.session_state.background_image_bytes)

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
if 'sound_placeholder' not in st.session_state:
    st.session_state.sound_placeholder = None
if 'last_warning_time' not in st.session_state:
    st.session_state.last_warning_time = 0
if 'collect_sound_index' not in st.session_state:
    st.session_state.collect_sound_index = 0
if 'bg_overlay_cached' not in st.session_state:
    st.session_state.bg_overlay_cached = None
if 'bg_overlay_path' not in st.session_state:
    st.session_state.bg_overlay_path = None

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

# --- Load Moonrock Image (CACHED) ---
if 'moonrock_img' not in st.session_state:
    moonrock_img = cv2.imread("moonrock.png", cv2.IMREAD_UNCHANGED)
    if moonrock_img is None:
        st.error("Could not load moonrock.png. Ensure it exists.")
        st.stop()
    moonrock_size = 50
    st.session_state.moonrock_img = cv2.resize(moonrock_img, (moonrock_size, moonrock_size), interpolation=cv2.INTER_AREA)

moonrock_img = st.session_state.moonrock_img

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
    # Initialize MediaPipe only once per session (MEMORY OPTIMIZATION)
    if 'hands' not in st.session_state:
        mp_hands = mp.solutions.hands
        st.session_state.hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        st.session_state.mp_drawing = mp.solutions.drawing_utils
    
    hands = st.session_state.hands
    mp_drawing = st.session_state.mp_drawing
    mp_hands = mp.solutions.hands
    # Add the full screen background image behind everything
    if st.session_state.background_image:
        background_image_bytes = convert_image_to_bytes(st.session_state.background_image)
        if background_image_bytes:
            st.session_state.background_image_bytes = background_image_bytes
            full_screen_background(st.session_state.background_image_bytes)
    
    # Create placeholders for dynamic updates
    hud_placeholder = st.empty()
    video_placeholder = st.empty()
    sound_placeholder = st.empty()
    
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
        
        # Time warnings
        if remaining_time <= 10 and remaining_time > 9 and st.session_state.last_warning_time != 10:
            sound_html = play_sound_effect("time_warning_10")
            if sound_html:
                sound_placeholder.markdown(sound_html, unsafe_allow_html=True)
            st.session_state.last_warning_time = 10
        elif remaining_time <= 5 and remaining_time > 4 and st.session_state.last_warning_time != 5:
            sound_html = play_sound_effect("time_warning_5")
            if sound_html:
                sound_placeholder.markdown(sound_html, unsafe_allow_html=True)
            st.session_state.last_warning_time = 5
        
        if remaining_time == 0:
            # Capture selfie before ending (if not already captured)
            if st.session_state.get('selfie_frame') is None:
                from enhanced_features import create_space_selfie
                st.session_state.selfie_frame = create_space_selfie(
                    frame, st.session_state.score, st.session_state.level, st.session_state.spacetag
                )
            
            # Check if they collected all moonrocks
            if len(st.session_state.moonrocks) > 0:
                # Failed to collect all - offer retry
                st.session_state.game_state = 'level_failed'
            else:
                # Time ran out but all collected
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
                        
                        # Sound effects disabled for now (browser autoplay restrictions)
                        # Will add back with proper user interaction handling
                        st.session_state.collect_sound_index += 1
                        
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
                            # Play level complete sound
                            sound_html = play_sound_effect("level_complete")
                            if sound_html:
                                sound_placeholder.markdown(sound_html, unsafe_allow_html=True)
                            
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
            
            # Cache background overlay to avoid loading from disk every frame (MEMORY OPTIMIZATION)
            if st.session_state.bg_overlay_path != st.session_state.background_image or st.session_state.bg_overlay_cached is None:
                try:
                    bg_overlay = cv2.imread(st.session_state.background_image, cv2.IMREAD_COLOR)
                    if bg_overlay is not None:
                        st.session_state.bg_overlay_cached = cv2.resize(bg_overlay, (frame.shape[1], frame.shape[0]))
                        st.session_state.bg_overlay_path = st.session_state.background_image
                except:
                    st.session_state.bg_overlay_cached = None
            
            # Use cached overlay
            if st.session_state.bg_overlay_cached is not None:
                frame = cv2.addWeighted(frame, 1 - overlay_alpha, st.session_state.bg_overlay_cached, overlay_alpha, 0)
        
        # Drawing moonrocks only - NO TEXT ON VIDEO
        for rx, ry in st.session_state.moonrocks:
            overlay_image(frame, moonrock_img, rx, ry)

        # Update HUD with current stats
        time_color = "#ef4444" if remaining_time < 10 else "#fbbf24" if remaining_time < 20 else "#22c55e"
        combo_display = f"<p style='color: #22c55e; font-size: 20px; margin: 15px 0 0 0; font-weight: bold;'>COMBO x{st.session_state.combo + 1}!</p>" if st.session_state.combo > 0 else ""
        
        hud_html = f"""
        <div style="position: fixed; top: 20px; right: 20px; 
                    background: rgba(10, 14, 39, 0.95); 
                    padding: 20px; border-radius: 12px; 
                    border: 1px solid rgba(99, 102, 241, 0.4);
                    backdrop-filter: blur(12px);
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
                    z-index: 9999;
                    min-width: 200px;">
            <h3 style='color: #6366f1; margin: 0 0 15px 0;'>{st.session_state.spacetag}</h3>
            <p style='color: #f8fafc; font-size: 18px; margin: 8px 0;'><strong>Score:</strong> {st.session_state.score}</p>
            <p style='color: #f8fafc; font-size: 18px; margin: 8px 0;'><strong>Level:</strong> {st.session_state.level}</p>
            <p style='color: {time_color}; font-size: 18px; margin: 8px 0;'><strong>Time:</strong> {int(remaining_time)}s</p>
            <p style='color: #f8fafc; font-size: 18px; margin: 8px 0;'><strong>Rocks:</strong> {len(st.session_state.moonrocks)}</p>
            {combo_display}
        </div>
        """
        hud_placeholder.markdown(hud_html, unsafe_allow_html=True)

        # Display clean video feed without any text overlay
        video_placeholder.image(frame, channels="BGR", use_container_width=True)

elif st.session_state.game_state == 'level_failed':
    # Level failed screen
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="background: rgba(10, 14, 39, 0.9); padding: 40px; border-radius: 12px; 
                        border: 1px solid rgba(239, 68, 68, 0.5); backdrop-filter: blur(12px);
                        text-align: center;">
        """, unsafe_allow_html=True)
        
        st.title("Time's Up!")
        st.write("")
        st.markdown(f"### Moonrocks Remaining: {len(st.session_state.moonrocks)}")
        st.markdown(f"### Current Score: {st.session_state.score}")
        st.markdown(f"### Level: {st.session_state.level}")
        st.write("")
        st.warning("You didn't collect all the moonrocks in time!")
        st.write("")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Retry Level", type="primary", use_container_width=True):
                # Retry same level
                st.session_state.combo = 0
                st.session_state.last_collect_time = 0
                reset_level()
                st.session_state.game_state = 'level_start'
                st.rerun()
        
        with col_b:
            if st.button("End Mission", use_container_width=True):
                st.session_state.game_state = 'end'
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.game_state == 'end':
    display_end_screen()

# --- Release Resources ---
# Clean up resources when not playing (MEMORY OPTIMIZATION)
if st.session_state.game_state != 'playing':
    # Release camera
    if 'cap' in st.session_state:
        try:
            st.session_state.cap.release()
        except:
            pass
        del st.session_state['cap']
        print("Camera released")
    
    # Release MediaPipe hands
    if 'hands' in st.session_state:
        try:
            st.session_state.hands.close()
        except:
            pass
        del st.session_state['hands']
        del st.session_state['mp_drawing']
        print("MediaPipe hands released")
    
    # Clear cached background overlay
    if 'bg_overlay_cached' in st.session_state:
        st.session_state.bg_overlay_cached = None
        st.session_state.bg_overlay_path = None
        print("Background cache cleared")



