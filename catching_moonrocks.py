## Lunar Loot - AI-Powered Hand Tracking Game
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

# Page configuration
st.set_page_config(
    page_title="Lunar Loot - AI Game",
    page_icon="🌑",  # Simple moon icon
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Mobile detection and warning
st.markdown("""
    <script>
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        document.body.innerHTML = '<div style="display: flex; align-items: center; justify-content: center; height: 100vh; background: #0a0e27; color: white; text-align: center; padding: 20px;"><div><h1>LUNAR LOOT</h1><p style="font-size: 18px; margin: 20px 0;">This game requires a desktop computer with a webcam for hand tracking.</p><p>Please visit on a desktop browser:</p><p style="color: #6366f1;">• Chrome (Recommended)<br>• Firefox<br>• Edge</p></div></div>';
    }
    </script>
""", unsafe_allow_html=True)

# Custom CSS for sophisticated space-themed UI
st.markdown("""
    <style>
    /* Import Orbitron space font */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;900&display=swap');
    
    /* Apply font globally */
    html, body, [class*="css"], * {
        font-family: 'Orbitron', sans-serif !important;
    }
    
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
    
    /* Disable browser text detection on ALL images */
    [data-testid="stImage"] img,
    img {
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        -ms-user-select: none !important;
        user-select: none !important;
        pointer-events: none !important;
        -webkit-touch-callout: none !important;
    }
    
    /* Disable Safari/Chrome text detection overlay */
    img::after {
        content: none !important;
    }
    
    /* Primary buttons with click animation */
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
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.6);
        background: linear-gradient(135deg, #7c3aed 0%, #6366f1 100%);
    }
    
    .stButton > button:active {
        transform: translateY(2px) scale(0.98);
        box-shadow: 0 2px 10px rgba(99, 102, 241, 0.4);
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
def get_sound_bytes(sound_type="collect"):
    """Get sound file bytes for playback"""
    for ext in ['.wav', '.mp3']:
        local_sound_path = os.path.join(GAME_ROOT_DIR, "sounds", f"{sound_type}{ext}")
        if os.path.exists(local_sound_path):
            try:
                with open(local_sound_path, 'rb') as audio_file:
                    return audio_file.read(), ext
            except Exception as e:
                print(f"Error loading sound {sound_type}: {e}")
    return None, None

def play_sound_effect(sound_type="collect"):
    """Play a sound effect - returns HTML audio string"""
    # Check for local sound files
    for ext in ['.wav', '.mp3']:
        local_sound_path = os.path.join(GAME_ROOT_DIR, "sounds", f"{sound_type}{ext}")
        if os.path.exists(local_sound_path):
            try:
                with open(local_sound_path, 'rb') as audio_file:
                    audio_bytes = base64.b64encode(audio_file.read()).decode()
                    mime_type = "audio/wav" if ext == '.wav' else "audio/mpeg"
                    return f'<audio autoplay preload="auto"><source src="data:{mime_type};base64,{audio_bytes}" type="{mime_type}"></audio>'
            except:
                pass
    
    # Fallback to online sounds
    sounds = {
        "collect": "https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3",
        "level_complete": "https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3",
        "level_failed": "https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3",
        "warning": "https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3",
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

def display_title_screen():
    """Classic game title screen with menu options"""
    # Load main menu background
    main_menu_bg = os.path.join(GAME_ROOT_DIR, "backgrounds", "Main_Menu", "Main_Menu_Start_Screen_BG.png")
    
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
    
    # Center column for menu
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("")
        st.write("")
        
        # Display logo
        try:
            logo_path = "ui_assets/branding/Lunar_Loot_Logo.png"
            with open(logo_path, 'rb') as f:
                logo_img = base64.b64encode(f.read()).decode()
            
            st.markdown(f"""
                <div style="text-align: center; margin: 40px 0;">
                    <img src="data:image/png;base64,{logo_img}" 
                         style="max-width: 500px; width: 90%; animation: logoPulse 3s ease-in-out infinite;"
                         alt="Lunar Loot">
                </div>
                <style>
                @keyframes logoPulse {{
                    0%, 100% {{ transform: scale(1); filter: brightness(1); }}
                    50% {{ transform: scale(1.02); filter: brightness(1.1); }}
                }}
                </style>
            """, unsafe_allow_html=True)
        except:
            st.title("LUNAR LOOT")
        
        st.write("")
        
        # Camera requirement notice
        st.markdown("""
            <div style="background: rgba(99, 102, 241, 0.15); padding: 15px; border-radius: 8px; 
                        border: 1px solid rgba(99, 102, 241, 0.4); margin-bottom: 20px;">
                <p style="color: #fbbf24; font-size: 14px; margin: 0; text-align: center;">
                    📷 <strong>Webcam Required</strong> - Please allow camera access when prompted
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Menu buttons
        if st.button("▶ BEGIN GAME", type="primary", use_container_width=True, key="begin_game"):
            st.session_state.game_state = 'start'
            st.rerun()
        
        st.write("")
        
        if st.button("ℹ️ ABOUT", use_container_width=True, key="about_btn"):
            st.session_state.game_state = 'about'
            st.rerun()
        
        st.write("")
        
        # Credits
        st.markdown("""
            <div style="background: rgba(10, 14, 39, 0.8); padding: 20px; border-radius: 12px; 
                        border: 1px solid rgba(99, 102, 241, 0.3); backdrop-filter: blur(12px);
                        text-align: center; margin-top: 30px;">
                <p style="color: #6366f1; font-size: 14px; margin: 5px 0;">POWERED BY</p>
                <p style="color: #f8fafc; font-size: 12px; margin: 5px 0;">
                    Google MediaPipe • Freepik • Adobe
                </p>
            </div>
        """, unsafe_allow_html=True)

def display_about_screen():
    """About screen with game information"""
    # Background
    main_menu_bg = os.path.join(GAME_ROOT_DIR, "backgrounds", "Main_Menu", "Main_Menu_Start_Screen_BG.png")
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
        except:
            pass
    
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("""
            <div style="background: rgba(10, 14, 39, 0.9); padding: 40px; border-radius: 12px; 
                        border: 1px solid rgba(99, 102, 241, 0.4); backdrop-filter: blur(12px);">
                <h1 style="color: #6366f1; text-align: center; margin-bottom: 30px;">ABOUT LUNAR LOOT</h1>
                
                <h3 style="color: #f8fafc;">🎮 The Game</h3>
                <p style="color: #cbd5e1; line-height: 1.8;">
                    Lunar Loot is an AI-powered hand-tracking game where you collect cosmic moonrocks 
                    using only your hand gestures. No controllers needed - just your webcam and your hands!
                </p>
                
                <h3 style="color: #f8fafc; margin-top: 25px;">🎯 How to Play</h3>
                <p style="color: #cbd5e1; line-height: 1.8;">
                    • Show your hand to the camera<br>
                    • Point with your index finger<br>
                    • Touch moonrocks to collect them<br>
                    • Collect all rocks before time runs out<br>
                    • Build combos for bonus points!
                </p>
                
                <h3 style="color: #f8fafc; margin-top: 25px;">🎁 Easter Eggs</h3>
                <p style="color: #cbd5e1; line-height: 1.8;">
                    • ✌️ Peace sign (2 fingers up): +50 points<br>
                    • 👍 Thumbs up: +100 points + Chroma Awards shoutout!
                </p>
                
                <h3 style="color: #f8fafc; margin-top: 25px;">🤖 AI Technology</h3>
                <p style="color: #cbd5e1; line-height: 1.8;">
                    • <strong>Google MediaPipe:</strong> Real-time hand tracking<br>
                    • <strong>Freepik AI:</strong> Space-themed visuals<br>
                    • <strong>Adobe:</strong> Editing and polish
                </p>
                
                <h3 style="color: #f8fafc; margin-top: 25px;">🏆 Created For</h3>
                <p style="color: #cbd5e1; line-height: 1.8; text-align: center;">
                    <strong style="color: #6366f1; font-size: 18px;">Chroma Awards 2025</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        if st.button("← BACK TO MENU", use_container_width=True):
            st.session_state.game_state = 'title'
            st.rerun()

def display_start_screen():
    # Music button with better online space music
    import streamlit.components.v1 as components
    
    components.html("""
        <!DOCTYPE html>
        <html>
        <body style="margin:0; padding:0; overflow:hidden;">
            <div style="position: fixed; bottom: 10px; left: 10px; z-index: 10000;">
                <button id="musicBtn" style="
                    background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%);
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 50%;
                    width: 50px;
                    height: 50px;
                    cursor: pointer;
                    font-size: 20px;
                    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.5);
                    transition: all 0.3s ease;
                ">
                    🎵
                </button>
            </div>
            <audio id="bgMusic" loop>
                <source src="https://assets.mixkit.co/active_storage/sfx/2745/2745-preview.mp3" type="audio/mpeg">
            </audio>
            <script>
                var music = document.getElementById('bgMusic');
                var btn = document.getElementById('musicBtn');
                var playing = false;
                
                btn.onmouseover = function() {
                    this.style.transform = 'scale(1.1)';
                };
                
                btn.onmouseout = function() {
                    this.style.transform = 'scale(1)';
                };
                
                btn.onclick = function() {
                    if (playing) {
                        music.pause();
                        btn.innerHTML = '🔇';
                        playing = false;
                    } else {
                        music.volume = 0.3;
                        music.play();
                        btn.innerHTML = '🎵';
                        playing = true;
                    }
                };
                
                // Auto-play attempt
                setTimeout(function() {
                    music.volume = 0.3;
                    music.play().then(function() {
                        playing = true;
                    }).catch(function() {});
                }, 500);
            </script>
        </body>
        </html>
    """, height=100, scrolling=False)
    
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
        # Display logo instead of text title
        try:
            import base64
            logo_path = "ui_assets/branding/Lunar_Loot_Logo.png"
            with open(logo_path, 'rb') as f:
                logo_img = base64.b64encode(f.read()).decode()
            
            st.markdown(f"""
                <div style="background: rgba(10, 14, 39, 0.85); padding: 30px; border-radius: 12px; 
                            border: 1px solid rgba(99, 102, 241, 0.3); backdrop-filter: blur(12px);
                            margin-bottom: 20px; text-align: center;">
                    <img src="data:image/png;base64,{logo_img}" 
                         style="max-width: 100%; width: 400px; margin-bottom: 15px;"
                         alt="Lunar Loot">
                    <p style="font-size: 1.25rem; color: #cbd5e1; margin: 10px 0 0 0;">
                        Collect cosmic moonrocks before time runs out
                    </p>
                </div>
            """, unsafe_allow_html=True)
        except:
            # Fallback to text if logo not found
            st.markdown("""
                <div style="background: rgba(10, 14, 39, 0.85); padding: 30px; border-radius: 12px; 
                            border: 1px solid rgba(99, 102, 241, 0.3); backdrop-filter: blur(12px);
                            margin-bottom: 20px;">
                    <h1 style="font-size: 3.5rem; margin: 0; color: #f8fafc; 
                               text-shadow: 0 0 20px rgba(99, 102, 241, 0.8);">
                        LUNAR LOOT
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
        
        # Camera warning - honest about limitations
        st.warning("📷 **Best Experience: Run Locally** - Streamlit Cloud has camera access limitations. For full gameplay, run locally (2-minute setup).")
        
        with st.expander("🚀 How to Run Locally (Recommended)"):
            st.code("""git clone https://github.com/gastondana627/lunar-loot.git
cd lunar-loot
pip install -r requirements.txt
streamlit run catching_moonrocks.py""", language="bash")
            st.markdown("Opens at `localhost:8501` with full camera access!")
        
        with st.expander("📹 Watch Demo Instead"):
            st.markdown("[View gameplay video](YOUR_YOUTUBE_URL) to see the game in action!")
        
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
        
        # Custom styled button matching your aesthetic
        st.markdown("""
            <style>
            .launch-mission-btn {
                background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 50px;
                padding: 20px 60px;
                font-size: 24px;
                font-weight: 700;
                color: white;
                text-align: center;
                cursor: pointer;
                transition: all 0.2s ease;
                box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4),
                            inset 0 2px 4px rgba(255, 255, 255, 0.2);
                text-transform: uppercase;
                letter-spacing: 2px;
                margin: 30px auto;
                max-width: 400px;
                display: block;
            }
            .launch-mission-btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 12px 40px rgba(99, 102, 241, 0.6);
                background: linear-gradient(135deg, #7c3aed 0%, #6366f1 100%);
            }
            .launch-mission-btn:active {
                transform: translateY(2px) scale(0.98);
                box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
            }
            </style>
        """, unsafe_allow_html=True)
        
        if st.button("LAUNCH MISSION", key="launch_btn", type="primary", use_container_width=True):
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
        
        # AI Technology Stack
        st.markdown("""
<div style="background: rgba(10, 14, 39, 0.7); padding: 15px; border-radius: 8px; margin: 15px 0;">
    <p style="color: #e2e8f0; font-weight: 600; margin-bottom: 8px;">AI Technology Stack:</p>
    <p style="color: #cbd5e1; margin: 0; line-height: 1.6;">
        • Google MediaPipe — Hand Tracking<br>
        • Freepik — Space Assets<br>
        • Adobe — Editing & Polish
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
            st.success("★ NEW HIGH SCORE ★")
        
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
        
        if st.button("NEW MISSION", key="new_mission_btn", type="primary", use_container_width=True):
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
            st.markdown("### ▶ Mission Snapshot")
            st.image(st.session_state.selfie_frame, use_container_width=True)
            
            # Download button
            import cv2
            _, buffer = cv2.imencode('.jpg', st.session_state.selfie_frame)
            st.download_button(
                label="↓ Download Snapshot",
                data=buffer.tobytes(),
                file_name=f"lunar_loot_{st.session_state.spacetag}.jpg",
                mime="image/jpeg",
                use_container_width=True
            )
        else:
            # Debug: Show why selfie isn't available
            st.info("○ No snapshot captured - complete at least one level to get your mission photo!")
        
        # Leaderboard
        st.write("")
        st.markdown("### ★ Top Pilots")
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
    st.markdown("★ *Submitted to [Chroma Awards 2025](https://www.chromaawards.com)*")


def display_level_transition_animation():
    """Displays a level transition animation - quick transition between levels."""
    
    # Success visual effect - VISIBLE overlay
    st.markdown("""
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                    background: radial-gradient(circle, rgba(34,197,94,0.5) 0%, rgba(10,14,39,0.8) 70%);
                    z-index: 1; pointer-events: none; animation: successPulse 2s ease-in-out infinite;">
        </div>
        <style>
            @keyframes successPulse {
                0%, 100% { opacity: 0.5; }
                50% { opacity: 0.9; }
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Play pending sound if any
    if st.session_state.get('pending_sound'):
        sound_html = play_sound_effect(st.session_state.pending_sound)
        if sound_html:
            st.markdown(sound_html, unsafe_allow_html=True)
        st.session_state.pending_sound = None
    
    # Simple level complete screen
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="background: rgba(10, 14, 39, 0.9); padding: 40px; border-radius: 12px; 
                        border: 1px solid rgba(99, 102, 241, 0.4); backdrop-filter: blur(12px);
                        text-align: center;">
        """, unsafe_allow_html=True)
        
        # Display logo centered
        try:
            import base64
            logo_path = "ui_assets/branding/Lunar_Loot_Logo.png"
            with open(logo_path, 'rb') as f:
                logo_img = base64.b64encode(f.read()).decode()
            
            st.markdown(f"""
                <div style="text-align: center; margin: 20px 0;">
                    <img src="data:image/png;base64,{logo_img}" 
                         style="max-width: 400px; width: 70%; margin-bottom: 20px;
                                animation: pulse 2s ease-in-out infinite;"
                         alt="Lunar Loot">
                </div>
                <style>
                @keyframes pulse {{
                    0%, 100% {{ opacity: 1; transform: scale(1); }}
                    50% {{ opacity: 0.8; transform: scale(1.05); }}
                }}
                </style>
            """, unsafe_allow_html=True)
        except:
            pass
        
        st.markdown(f"<h1 style='color: #22c55e; margin: 20px 0; text-align: center;'>★ Level {st.session_state.level} Complete!</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #f8fafc; font-size: 20px; margin: 10px 0; text-align: center;'><strong>Score:</strong> {st.session_state.score}</p>", unsafe_allow_html=True)
        
        if st.session_state.combo > 0:
            st.markdown(f"<p style='color: #22c55e; font-size: 18px; margin: 10px 0; text-align: center;'>Maximum Combo: x{st.session_state.combo + 1}</p>", unsafe_allow_html=True)
        
        st.write("")
        st.info("▶ Preparing next sector...")
        st.markdown("</div>", unsafe_allow_html=True)

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
        
        if st.button("BEGIN MISSION", key="begin_btn", type="primary", use_container_width=True):
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
    st.session_state.game_state = 'title'  # 'title', 'start', 'about', 'playing', 'level_transition', 'end', 'level_start'
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
if 'pending_sound' not in st.session_state:
    st.session_state.pending_sound = None
if 'sound_queue' not in st.session_state:
    st.session_state.sound_queue = []
if 'audio_enabled' not in st.session_state:
    st.session_state.audio_enabled = False
if 'sound_counter' not in st.session_state:
    st.session_state.sound_counter = 0
if 'flash_effect' not in st.session_state:
    st.session_state.flash_effect = None
if 'music_enabled' not in st.session_state:
    st.session_state.music_enabled = True
if 'peace_last_trigger' not in st.session_state:
    st.session_state.peace_last_trigger = 0
if 'chroma_last_trigger' not in st.session_state:
    st.session_state.chroma_last_trigger = 0

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
        st.error("📷 Camera not accessible on Streamlit Cloud")
        
        st.markdown("""
        ### 🎮 Play Locally for Best Experience
        
        Due to Streamlit Cloud's architecture, camera access works best when running locally:
        
        ```bash
        # Quick setup (2 minutes):
        git clone https://github.com/gastondana627/lunar-loot.git
        cd lunar-loot
        pip install -r requirements.txt
        streamlit run catching_moonrocks.py
        ```
        
        The game will open at `localhost:8501` with full camera access!
        
        **Why?** Streamlit uses server-side OpenCV which can't access browser cameras directly. 
        This is a known limitation of CV apps on Streamlit Cloud.
        """)
        
        st.info("💡 **For Judges:** Demo video available in submission showing full gameplay!")
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

if st.session_state.game_state == 'title':
    display_title_screen()
elif st.session_state.game_state == 'about':
    display_about_screen()
elif st.session_state.game_state == 'start':
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
    
    # Music button in gameplay
    import streamlit.components.v1 as components
    components.html("""
        <div style="position: fixed; bottom: 80px; left: 20px; z-index: 10000;">
            <button id="musicBtn" style="
                background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                width: 60px;
                height: 60px;
                cursor: pointer;
                font-size: 24px;
                box-shadow: 0 4px 15px rgba(99, 102, 241, 0.5);
                transition: all 0.3s ease;
            ">
                🎵
            </button>
        </div>
        <audio id="bgMusic" loop>
            <source src="https://assets.mixkit.co/active_storage/sfx/2462/2462-preview.mp3" type="audio/mpeg">
        </audio>
        <script>
            var music = document.getElementById('bgMusic');
            var btn = document.getElementById('musicBtn');
            var musicPlaying = false;
            
            btn.addEventListener('mouseover', function() {
                this.style.transform = 'scale(1.1)';
            });
            
            btn.addEventListener('mouseout', function() {
                this.style.transform = 'scale(1)';
            });
            
            btn.addEventListener('click', function() {
                if (musicPlaying) {
                    music.pause();
                    btn.innerHTML = '🔇';
                    musicPlaying = false;
                } else {
                    music.volume = 0.3;
                    music.play();
                    btn.innerHTML = '🎵';
                    musicPlaying = true;
                }
            });
            
            // Continue playing if already started
            if (window.musicStarted) {
                music.volume = 0.3;
                music.play();
                musicPlaying = true;
            }
        </script>
    """, height=80)
    
    # Create placeholders for dynamic updates
    hud_placeholder = st.empty()
    video_placeholder = st.empty()
    
    # Audio player using components.html - runs independently of loop
    audio_placeholder = st.empty()
    
    while st.session_state.cap.isOpened() and st.session_state.game_state == 'playing':  # keep the main loop here

        ret, frame = st.session_state.cap.read()
        if not ret:
            st.warning("End of stream or error reading frame.")
            st.session_state.game_state = 'end'
            st.rerun()

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        # Time Handling
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = max(0, LEVEL_TIME_LIMIT - elapsed_time)
        
        # Time warnings
        if remaining_time <= 10 and remaining_time > 9 and st.session_state.last_warning_time != 10:
            with audio_placeholder:
                components.html("""
                    <audio autoplay>
                        <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
                    </audio>
                """, height=0)
            st.session_state.last_warning_time = 10
        elif remaining_time <= 5 and remaining_time > 4 and st.session_state.last_warning_time != 5:
            with audio_placeholder:
                components.html("""
                    <audio autoplay>
                        <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
                    </audio>
                """, height=0)
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
                st.session_state.pending_sound = "level_failed"
                st.session_state.game_state = 'level_failed'
            else:
                # Time ran out but all collected
                st.session_state.game_state = 'end'
            
            # CRITICAL: Rerun to show the next screen
            st.rerun()

        if result.multi_hand_landmarks:
            # Easter egg: Detect peace sign (✌️)
            for hand_landmarks in result.multi_hand_landmarks:
                # Get finger tips and bases
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
                middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
                ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
                ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
                pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
                
                # Peace sign: index and middle extended, ring and pinky curled
                index_extended = index_tip.y < index_pip.y
                middle_extended = middle_tip.y < middle_pip.y
                ring_curled = ring_tip.y > ring_mcp.y
                pinky_curled = pinky_tip.y > pinky_mcp.y
                
                # Detect peace sign with cooldown
                current_time = time.time()
                peace_cooldown = st.session_state.get('peace_last_trigger', 0)
                
                if index_extended and middle_extended and ring_curled and pinky_curled:
                    # Only trigger if cooldown has passed (5 seconds)
                    if current_time - peace_cooldown > 5.0:
                        st.session_state.score += 50
                        st.session_state.flash_effect = "peace"
                        st.session_state.peace_last_trigger = current_time
                        
                        # Draw BIG visual indicator on frame (centered)
                        text = "PEACE! +50"
                        font_scale = 3
                        thickness = 5
                        font = cv2.FONT_HERSHEY_DUPLEX
                        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
                        x = (st.session_state.video_width - text_width) // 2
                        y = (st.session_state.video_height + text_height) // 2
                        # Draw background rectangle
                        cv2.rectangle(frame, (x-20, y-text_height-20), (x+text_width+20, y+20), (0, 0, 0), -1)
                        # Draw text
                        cv2.putText(frame, text, (x, y), font, font_scale, (34, 197, 94), thickness)
                        
                        # Play special sound
                        with audio_placeholder:
                            components.html("""
                                <audio autoplay>
                                    <source src="https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3" type="audio/mpeg">
                                </audio>
                            """, height=0)
                        break
            
            # Easter egg: Detect thumbs up for Chroma Awards shoutout!
            for hand_landmarks in result.multi_hand_landmarks:
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                
                # Thumbs up: thumb extended up, fingers curled
                thumb_extended = thumb_tip.y < thumb_ip.y - 0.05
                fingers_curled = index_tip.y > index_mcp.y
                
                # Detect thumbs up with cooldown
                current_time = time.time()
                chroma_cooldown = st.session_state.get('chroma_last_trigger', 0)
                
                if thumb_extended and fingers_curled:
                    # Only trigger if cooldown has passed (5 seconds)
                    if current_time - chroma_cooldown > 5.0:
                        st.session_state.score += 100
                        st.session_state.flash_effect = "chroma"
                        st.session_state.chroma_last_trigger = current_time
                        
                        # Draw BIG visual indicator on frame (centered)
                        text = "CHROMA AWARDS! +100"
                        font_scale = 2.5
                        thickness = 5
                        font = cv2.FONT_HERSHEY_DUPLEX
                        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
                        x = (st.session_state.video_width - text_width) // 2
                        y = (st.session_state.video_height + text_height) // 2
                        # Draw background rectangle
                        cv2.rectangle(frame, (x-20, y-text_height-20), (x+text_width+20, y+20), (0, 0, 0), -1)
                        # Draw text
                        cv2.putText(frame, text, (x, y), font, font_scale, (99, 102, 241), thickness)
                        
                        # Play epic sound
                        with audio_placeholder:
                            components.html("""
                                <audio autoplay>
                                    <source src="https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3" type="audio/mpeg">
                                </audio>
                            """, height=0)
                        break
            
            for hand_landmarks in result.multi_hand_landmarks:
                index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                fx, fy = int(index_finger.x * st.session_state.video_width), int(index_finger.y * st.session_state.video_height)  # Capture video width and height from session state
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Collection logic with combo system
                for rock in list(st.session_state.moonrocks):  # Iterate over a copy
                    rx, ry = rock
                    if abs(fx - rx) < 30 and abs(fy - ry) < 30:
                        st.session_state.moonrocks.remove(rock)
                        
                        # Visual flash effect on collection
                        st.session_state.flash_effect = "collect"
                        
                        # Play beep using components.html - works during loop!
                        with audio_placeholder:
                            components.html("""
                                <audio autoplay>
                                    <source src="https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3" type="audio/mpeg">
                                </audio>
                            """, height=0)
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
                            # Capture selfie frame FIRST
                            from enhanced_features import create_space_selfie
                            st.session_state.selfie_frame = create_space_selfie(
                                frame, st.session_state.score, st.session_state.level, st.session_state.spacetag
                            )
                            
                            # Time bonus
                            time_bonus = int(remaining_time * 2)
                            st.session_state.score += time_bonus
                            
                            # Store sound to play on next screen
                            st.session_state.pending_sound = "level_complete"
                            
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

        # Update HUD with current stats FIRST
        time_color = "#ef4444" if remaining_time < 10 else "#fbbf24" if remaining_time < 20 else "#22c55e"
        combo_display = f"<p style='color: #22c55e; font-size: 14px; margin: 8px 0 0 0; font-weight: bold;'>COMBO x{st.session_state.combo + 1}!</p>" if st.session_state.combo > 0 else ""
        
        # Visual flash effect overlay - SEPARATE from HUD
        flash_html = ""
        if st.session_state.flash_effect == "collect":
            flash_html = """
            <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                        background: radial-gradient(circle, rgba(34,197,94,0.3) 0%, transparent 70%);
                        pointer-events: none; z-index: 50; animation: flashCollect 0.3s ease-out;">
            </div>
            <style>
                @keyframes flashCollect {
                    0% { opacity: 1; }
                    100% { opacity: 0; }
                }
            </style>
            """
            st.session_state.flash_effect = None
        elif st.session_state.flash_effect == "peace":
            flash_html = """
            <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
                        font-size: 120px; z-index: 50; animation: peacePop 1s ease-out;
                        pointer-events: none; text-shadow: 0 0 20px rgba(34,197,94,0.8);">
                ✌️
            </div>
            <div style="position: fixed; top: 20%; left: 50%; transform: translateX(-50%);
                        background: rgba(34,197,94,0.9); padding: 15px 30px; border-radius: 25px;
                        z-index: 51; animation: bonusPop 1s ease-out; pointer-events: none;
                        box-shadow: 0 4px 20px rgba(34,197,94,0.5);">
                <p style="color: white; margin: 0; font-size: 24px; font-weight: bold;">✌️ +50 PEACE BONUS!</p>
            </div>
            <style>
                @keyframes peacePop {
                    0% { opacity: 0; transform: translate(-50%, -50%) scale(0) rotate(-20deg); }
                    50% { opacity: 1; transform: translate(-50%, -50%) scale(1.2) rotate(10deg); }
                    100% { opacity: 0; transform: translate(-50%, -50%) scale(1) rotate(0deg); }
                }
                @keyframes bonusPop {
                    0% { opacity: 0; transform: translateX(-50%) translateY(-20px); }
                    20% { opacity: 1; transform: translateX(-50%) translateY(0); }
                    80% { opacity: 1; transform: translateX(-50%) translateY(0); }
                    100% { opacity: 0; transform: translateX(-50%) translateY(20px); }
                }
            </style>
            """
            st.session_state.flash_effect = None
        elif st.session_state.flash_effect == "chroma":
            flash_html = """
            <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
                        font-size: 80px; z-index: 50; animation: chromaPop 1.5s ease-out;
                        pointer-events: none; text-shadow: 0 0 30px rgba(99,102,241,0.8);
                        background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;
                        font-weight: 900;">
                CHROMA AWARDS
            </div>
            <div style="position: fixed; top: 30%; left: 50%; transform: translateX(-50%);
                        background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%);
                        padding: 20px 40px; border-radius: 30px;
                        z-index: 51; animation: chromaBonusPop 1.5s ease-out; pointer-events: none;
                        box-shadow: 0 8px 30px rgba(99,102,241,0.6);
                        border: 2px solid rgba(255,255,255,0.3);">
                <p style="color: white; margin: 0; font-size: 28px; font-weight: bold;">👍 +100 BONUS!</p>
                <p style="color: #fbbf24; margin: 5px 0 0 0; font-size: 16px;">Thanks for the support!</p>
            </div>
            <style>
                @keyframes chromaPop {
                    0% { opacity: 0; transform: translate(-50%, -50%) scale(0) rotate(-10deg); }
                    50% { opacity: 1; transform: translate(-50%, -50%) scale(1.1) rotate(0deg); }
                    100% { opacity: 0; transform: translate(-50%, -50%) scale(1) rotate(10deg); }
                }
                @keyframes chromaBonusPop {
                    0% { opacity: 0; transform: translateX(-50%) translateY(-30px) scale(0.8); }
                    20% { opacity: 1; transform: translateX(-50%) translateY(0) scale(1); }
                    80% { opacity: 1; transform: translateX(-50%) translateY(0) scale(1); }
                    100% { opacity: 0; transform: translateX(-50%) translateY(30px) scale(0.8); }
                }
            </style>
            """
            st.session_state.flash_effect = None
        
        hud_html = f"""
        <div style="position: fixed; top: 10px; right: 10px; 
                    background: rgba(10, 14, 39, 0.75); 
                    padding: 12px 16px; border-radius: 8px; 
                    border: 1px solid rgba(99, 102, 241, 0.3);
                    backdrop-filter: blur(8px);
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
                    z-index: 100;
                    pointer-events: none;
                    min-width: 160px;">
            <p style='color: #6366f1; margin: 0 0 8px 0; font-size: 14px; font-weight: 600;'>{st.session_state.spacetag}</p>
            <p style='color: #f8fafc; font-size: 14px; margin: 4px 0;'><strong>Score:</strong> {st.session_state.score}</p>
            <p style='color: #f8fafc; font-size: 14px; margin: 4px 0;'><strong>Level:</strong> {st.session_state.level}</p>
            <p style='color: {time_color}; font-size: 14px; margin: 4px 0;'><strong>Time:</strong> {int(remaining_time)}s</p>
            <p style='color: #f8fafc; font-size: 14px; margin: 4px 0;'><strong>Rocks:</strong> {len(st.session_state.moonrocks)}</p>
            {combo_display}
        </div>
        """
        hud_placeholder.markdown(hud_html, unsafe_allow_html=True)

        # Display clean video feed without any text overlay
        video_placeholder.image(frame, channels="BGR", use_container_width=True)

elif st.session_state.game_state == 'level_failed':
    # Failure visual effect - BEHIND content with pointer-events: none
    st.markdown("""
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                    background: radial-gradient(circle, rgba(239,68,68,0.3) 0%, rgba(10,14,39,0.9) 70%);
                    z-index: -1; pointer-events: none; animation: failShake 0.5s ease-in-out;">
        </div>
        <style>
            @keyframes failShake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-10px); }
                75% { transform: translateX(10px); }
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Play pending sound or level failed sound
    # Play sound
    if st.session_state.get('pending_sound'):
        sound_html = play_sound_effect(st.session_state.pending_sound)
        st.session_state.pending_sound = None
    else:
        sound_html = play_sound_effect("level_failed")
    
    if sound_html:
        st.markdown(sound_html, unsafe_allow_html=True)
    
    # Level failed screen with selfie
    col1, col2 = st.columns([1, 1])
    
    with col1:
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
    
    with col2:
        # Display selfie with download button (captured instantly on failure)
        if st.session_state.get('selfie_frame') is not None:
            st.markdown("### 📸 Mission Snapshot")
            st.image(st.session_state.selfie_frame, use_container_width=True)
            
            # Download button
            import cv2
            _, buffer = cv2.imencode('.jpg', st.session_state.selfie_frame)
            st.download_button(
                label="↓ Download Snapshot",
                data=buffer.tobytes(),
                file_name=f"lunar_loot_failed_{st.session_state.spacetag}.jpg",
                mime="image/jpeg",
                use_container_width=True
            )
        else:
            st.info("○ No snapshot available")

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



