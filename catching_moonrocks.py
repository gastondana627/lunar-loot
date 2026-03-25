## Lunar Loot - COMPLETE Production Version
## AI-Powered Hand Tracking Game
## Tools: Google MediaPipe, Freepik, Adobe
## JavaScript MediaPipe - Runs entirely in browser!

import streamlit as st
import streamlit.components.v1 as components
import os
import base64

# Page configuration
st.set_page_config(
    page_title="Lunar Loot - AI Game",
    page_icon="🌑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

GAME_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Sector names for 14 levels
SECTOR_NAMES = {
    1: "Mercury", 2: "Mars", 3: "Venus", 4: "Moon", 5: "Saturn",
    6: "Jupiter", 7: "Neptune", 8: "Uranus", 9: "Pluto", 10: "Ceres",
    11: "Comet Atlas", 12: "Oumuamua", 13: "Planet X", 14: "Spaceship"
}

# Background files mapping - CORRECTED to match sector names
BACKGROUND_FILES = {
    1: "Mercury_1.png",      # Mercury
    2: "Mars_1.png",         # Mars
    3: "Venus_1.png",        # Venus
    4: "Moon_1.png",         # Moon
    5: "Saturn_1.png",       # Saturn
    6: "Earth_1.png",        # Jupiter (using Earth as closest match)
    7: "Uranus_1.png",       # Neptune
    8: "Uranus_1.png",       # Uranus
    9: "PlanetX_1.png",      # Pluto
    10: "Ceres_1.png",       # Ceres
    11: "Comet_3I_Atlas_1.png",  # Comet Atlas
    12: "Oumuamua_1.png",    # Oumuamua
    13: "PlanetX_1.png",     # Planet X
    14: "Spaceship_1.png"    # Spaceship
}

MAX_LEVELS = 14  # Total number of levels

def load_logo():
    logo_path = os.path.join(GAME_ROOT_DIR, "ui_assets", "branding", "Lunar_Loot_Logo.png")
    if os.path.exists(logo_path):
        try:
            with open(logo_path, 'rb') as f:
                return base64.b64encode(f.read()).decode()
        except:
            pass
    return None

def load_background(level):
    bg_file = BACKGROUND_FILES.get(level, "Mercury_1.png")
    bg_path = os.path.join(GAME_ROOT_DIR, "backgrounds", "New_Background_Rotation_1", bg_file)
    if os.path.exists(bg_path):
        try:
            with open(bg_path, 'rb') as f:
                return base64.b64encode(f.read()).decode()
        except:
            pass
    return None

def load_main_menu_bg():
    bg_path = os.path.join(GAME_ROOT_DIR, "backgrounds", "Main_Menu", "Main_Menu_Start_Screen_BG.png")
    if os.path.exists(bg_path):
        try:
            with open(bg_path, 'rb') as f:
                return base64.b64encode(f.read()).decode()
        except:
            pass
    return None

def load_moonrock_image():
    moonrock_path = os.path.join(GAME_ROOT_DIR, "moonrock.png")
    if os.path.exists(moonrock_path):
        try:
            with open(moonrock_path, 'rb') as f:
                return base64.b64encode(f.read()).decode()
        except:
            pass
    return None

import json
import datetime
import gspread
from google.oauth2.service_account import Credentials

HIGH_SCORES_FILE = os.path.join(GAME_ROOT_DIR, "high_scores.json")
GSHEET_URL = "https://docs.google.com/spreadsheets/d/1VV1xnnJ_kohhrwUhLBLcDX15VVvXWeb3Rg4CcmLLvpk"
GSHEET_SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

def _get_gsheet():
    """Authenticate and return the first worksheet of the leaderboard sheet."""
    try:
        creds_dict = dict(st.secrets["connections"]["gsheets"])
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
        creds = Credentials.from_service_account_info(creds_dict, scopes=GSHEET_SCOPES)
        client = gspread.authorize(creds)
        return client.open_by_url(GSHEET_URL).sheet1
    except Exception:
        return None

def load_high_scores() -> list:
    sheet = _get_gsheet()
    if sheet is None:
        # Fallback to local JSON when credentials are not yet configured
        if not os.path.exists(HIGH_SCORES_FILE):
            return []
        try:
            with open(HIGH_SCORES_FILE, 'r') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except:
            return []
    try:
        records = sheet.get_all_records()
        records.sort(key=lambda x: int(x.get("score", 0)) if str(x.get("score", "0")).isdigit() else 0, reverse=True)
        return records
    except:
        return []

def save_high_score(spacetag, score, level):
    if not spacetag or score <= 0:
        return
    timestamp = datetime.datetime.now().isoformat()
    sheet = _get_gsheet()
    if sheet is None:
        # Fallback: write to local JSON
        scores = load_high_scores()
        scores.append({"spacetag": spacetag, "score": score, "level": level, "timestamp": timestamp})
        scores.sort(key=lambda x: x.get("score", 0) if isinstance(x, dict) else 0, reverse=True)
        try:
            with open(HIGH_SCORES_FILE, 'w') as f:
                json.dump(scores[:100], f, indent=2)
        except:
            pass
        return
    try:
        sheet.append_row([spacetag, score, level, timestamp], value_input_option="USER_ENTERED")
    except:
        pass
# Cleaned up obsoleted query_params polling

# Session state
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'intro'  # Start with intro screen
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'spacetag' not in st.session_state:
    st.session_state.spacetag = ''
if 'snapshot' not in st.session_state:
    st.session_state.snapshot = None
if 'rocks_remaining' not in st.session_state:
    st.session_state.rocks_remaining = 0
if 'is_resuming' not in st.session_state:
    st.session_state.is_resuming = False
if 'level_complete_time' not in st.session_state:
    st.session_state.level_complete_time = None

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
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
    }
    /* Hide Native Audio Player */
    [data-testid="stAudio"] {
        display: none !important;
    }
    .music-btn {
        position: absolute;
        top: 20px;
        right: 20px;
        z-index: 9999;
    }
    </style>
""", unsafe_allow_html=True)

# Global Music Player Logic
if 'music_playing' not in st.session_state:
    st.session_state.music_playing = False

def render_global_music():
    if st.session_state.music_playing:
        st.audio("https://raw.githubusercontent.com/gastondana627/lunar-loot/main/sounds/menu_theme.wav", format="audio/wav", autoplay=True, loop=True)

render_global_music()

# ==================== INTRO SCREEN ====================
if st.session_state.game_state == 'intro':
    # Load main menu background
    main_bg = load_main_menu_bg()
    logo_bytes = load_logo()
    
    if main_bg:
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{main_bg});
                background-size: cover;
                background-position: center;
            }}
            </style>
        """, unsafe_allow_html=True)
    
    # Centered content
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Logo
        if logo_bytes:
            st.markdown(f"""
                <div style="text-align: center; margin: 60px 0 40px 0;">
                    <img src="data:image/png;base64,{logo_bytes}" 
                         style="max-width: 500px; width: 80%; animation: pulse 2s ease-in-out infinite;">
                </div>
            """, unsafe_allow_html=True)
        
        # Menu buttons
        st.write("")
        st.write("")
        
        if st.button("▶ BEGIN GAME", type="primary", use_container_width=True, key="begin_game"):
            st.session_state.game_state = 'title'
            st.rerun()
            
        st.write("")
        
        if st.button("🏆 HALL OF FAME", type="primary", use_container_width=True, key="leaderboard_btn"):
            st.session_state.game_state = 'leaderboard'
            st.rerun()
        
        st.write("")
        
        if st.button("ℹ️ ABOUT", use_container_width=True, key="about_btn"):
            st.session_state.game_state = 'about'
            st.rerun()
        
        # AI Credits at bottom
        st.write("")
        st.write("")
        st.markdown("""
            <div style="background: rgba(10, 14, 39, 0.85); padding: 20px; border-radius: 12px; 
                        border: 1px solid rgba(99, 102, 241, 0.3); margin-top: 40px; text-align: center;">
                <p style="color: #6366f1; font-size: 1rem; font-weight: 600; margin-bottom: 10px;">
                    AI POWERED BY
                </p>
                <p style="color: #cbd5e1; font-size: 0.95rem; margin: 0;">
                    Google MediaPipe · Freepik · Adobe
                </p>
            </div>
        """, unsafe_allow_html=True)

# ==================== ABOUT SCREEN ====================
elif st.session_state.game_state == 'about':
    main_bg = load_main_menu_bg()
    if main_bg:
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{main_bg});
                background-size: cover;
                background-position: center;
            }}
            </style>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="background: rgba(10, 14, 39, 0.9); padding: 40px; border-radius: 12px; 
                        border: 2px solid rgba(99, 102, 241, 0.5);">
                <h1 style='color: #6366f1; text-align: center; margin-bottom: 30px;'>About Lunar Loot</h1>
                
                <h3 style='color: #22c55e; margin-top: 25px;'>🎮 How to Play</h3>
                <p style='color: #cbd5e1; line-height: 1.8;'>
                    • Use your <strong>index finger</strong> to touch moonrocks<br>
                    • Collect all rocks before time runs out<br>
                    • Build combos by collecting quickly<br>
                    • Progress through 14 space sectors
                </p>
                
                <h3 style='color: #22c55e; margin-top: 25px;'>🤖 Computer Vision Technology</h3>
                <p style='color: #cbd5e1; line-height: 1.8;'>
                    • <strong>Google MediaPipe</strong> - Real-time hand tracking AI<br>
                    • Runs entirely in your browser (JavaScript)<br>
                    • No controllers needed - just your hands!<br>
                    • Privacy-first: No recording, no data stored
                </p>
                
                <h3 style='color: #22c55e; margin-top: 25px;'>🎨 AI Tools Used</h3>
                <p style='color: #cbd5e1; line-height: 1.8;'>
                    • <strong>Freepik</strong> - Space backgrounds & UI assets<br>
                    • <strong>Adobe</strong> - Logo & visual design<br>
                    • <strong>ElevenLabs</strong> - Voice & sound effects<br>
                    • <strong>MediaPipe</strong> - Hand gesture recognition
                </p>
                
                <h3 style='color: #22c55e; margin-top: 25px;'>🎁 Easter Eggs</h3>
                <p style='color: #cbd5e1; line-height: 1.8;'>
                    • ✌️ <strong>Peace Sign</strong> = +50 points<br>
                    • 👍 <strong>Thumbs Up</strong> = +100 points
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("◀ BACK TO MENU", use_container_width=True):
            st.session_state.game_state = 'intro'
            st.rerun()

# ==================== TITLE SCREEN ====================
elif st.session_state.game_state == 'title':
    main_bg = load_main_menu_bg()
    if main_bg:
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{main_bg});
                background-size: cover;
                background-position: center;
            }}
            </style>
        """, unsafe_allow_html=True)
    
    # Title Screen Layout
    # Music toggle in top right
    col_empty, col_music = st.columns([9, 1])
    with col_music:
        st.write("")
        st.write("")
        if st.button("🔊" if st.session_state.music_playing else "🔇", key="toggle_music_btn", help="Toggle Background Music"):
            st.session_state.music_playing = not st.session_state.music_playing
            st.rerun()
    
    # Centered content
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        logo_bytes = load_logo()
        if logo_bytes:
            st.markdown(f"""
                <div style="background: rgba(10, 14, 39, 0.85); padding: 30px; border-radius: 12px; 
                            border: 1px solid rgba(99, 102, 241, 0.3); margin-bottom: 20px; text-align: center;">
                    <img src="data:image/png;base64,{logo_bytes}" 
                         style="max-width: 100%; width: 400px; margin-bottom: 15px; animation: pulse 2s ease-in-out infinite;">
                    <p style="font-size: 1.25rem; color: #cbd5e1; margin: 10px 0 0 0;">
                        Collect cosmic moonrocks before time runs out
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        spacetag = st.text_input("Enter your Spacetag", value=st.session_state.spacetag, placeholder="AstroHunter42")
        if spacetag:
            st.session_state.spacetag = spacetag
        
        st.success("🚀 **JavaScript MediaPipe** - Runs entirely in YOUR browser! Real-time hand tracking with NO server lag!")
        
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
                    • Build combos for bonus points<br>
                    • Find hidden gesture bonuses (✌️ peace sign, 👍 thumbs up)!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.info("📹 **AI Powered by Google MediaPipe** - Advanced hand tracking technology")
        
        if st.button("🚀 START GAME", type="primary", use_container_width=True):
            st.session_state.game_state = 'level_start'
            st.rerun()

# ==================== LEVEL START SCREEN ====================
elif st.session_state.game_state == 'level_start':
    bg_bytes = load_background(st.session_state.level)
    if bg_bytes:
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{bg_bytes});
                background-size: cover;
                background-position: center;
            }}
            </style>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        sector_name = SECTOR_NAMES.get(st.session_state.level, "Unknown Sector").upper()
        rocks_count = 5 + st.session_state.level
        
        st.markdown(f"""
            <style>
            .sci-fi-hud {{
                background: rgba(10, 16, 40, 0.7);
                backdrop-filter: blur(15px);
                border: 2px solid #00f3ff;
                box-shadow: 0 0 20px rgba(0, 243, 255, 0.5), inset 0 0 30px rgba(0, 243, 255, 0.2);
                padding: 40px;
                border-radius: 15px;
                color: #e0f7fa;
                font-family: 'Orbitron', sans-serif;
                margin-top: 50px;
                margin-bottom: 20px;
                clip-path: polygon(5% 0, 95% 0, 100% 5%, 100% 95%, 95% 100%, 5% 100%, 0 95%, 0 5%);
            }}
            .hud-header {{
                text-align: center;
                color: #d8b4fe;
                font-size: 2.2rem;
                font-weight: 700;
                text-shadow: 0 0 10px #d8b4fe, 0 0 20px #8b5cf6;
                margin-bottom: 30px;
                letter-spacing: 2px;
                border-bottom: 1px solid rgba(0,243,255,0.3);
                padding-bottom: 15px;
            }}
            .hud-list {{
                list-style-type: none;
                padding-left: 10px;
                font-size: 1.3rem;
                line-height: 2.4;
                margin-bottom: 20px;
            }}
            .hud-list li::before {{
                content: '• ';
                color: #00f3ff;
                font-weight: bold;
                margin-right: 15px;
            }}
            .hud-highlight {{
                color: #00f3ff;
                font-weight: 600;
                text-shadow: 0 0 5px rgba(0,243,255,0.5);
            }}
            
            /* Restyle the Streamlit button */
            div[data-testid="stButton"] button {{
                background: linear-gradient(135deg, rgba(0,180,216,0.2) 0%, rgba(0,119,182,0.8) 100%) !important;
                border: 2px solid #00f3ff !important;
                color: #ffffff !important;
                font-family: 'Orbitron', sans-serif !important;
                font-size: 1.5rem !important;
                font-weight: 700 !important;
                padding: 15px 30px !important;
                box-shadow: 0 0 15px rgba(0,243,255,0.6), inset 0 0 10px rgba(0,243,255,0.4) !important;
                text-shadow: 0 0 8px rgba(255,255,255,0.8) !important;
                transition: all 0.3s ease !important;
                clip-path: polygon(3% 0, 97% 0, 100% 15%, 100% 85%, 97% 100%, 3% 100%, 0 85%, 0 15%) !important;
                border-radius: 0px !important;
            }}
            div[data-testid="stButton"] button:hover {{
                background: linear-gradient(135deg, rgba(0,180,216,0.6) 0%, rgba(0,119,182,1) 100%) !important;
                box-shadow: 0 0 25px rgba(0,243,255,1), inset 0 0 15px rgba(0,243,255,0.8) !important;
                transform: scale(1.02) !important;
                color: #ffffff !important;
            }}
            div[data-testid="stButton"] button p {{
                font-size: 1.5rem !important;
                font-weight: 700 !important;
            }}
            </style>
            
            <div class="sci-fi-hud">
                <div class="hud-header">SECTOR: {sector_name} - MISSION START</div>
                <ul class="hud-list">
                    <li>Mission Briefing:</li>
                    <li>☑&nbsp; <span class="hud-highlight">Moonrocks to Collect:</span> {rocks_count}</li>
                    <li>⏱&nbsp; <span class="hud-highlight">Time Limit:</span> 30s</li>
                    <li>🎯&nbsp; <span class="hud-highlight">Bonus Objective:</span> Build combos for bonus points</li>
                    <li>⚠&nbsp; <span class="hud-highlight">Hazard Warning:</span> Zero-Gravity Drifting Objects</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        button_text = "▶ RESUME MISSION" if st.session_state.is_resuming else "▶ BEGIN MISSION"
        if st.button(button_text, type="primary", use_container_width=True):
            st.session_state.is_resuming = False  # Reset flag
            st.session_state.game_state = 'playing'
            st.rerun()

# ==================== PLAYING STATE ====================
elif st.session_state.game_state == 'playing':
    
    # Full screen space background
    bg_bytes = load_background(st.session_state.level)
    if bg_bytes:
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{bg_bytes});
                background-size: cover;
                background-position: center;
            }}
            </style>
        """, unsafe_allow_html=True)
    
    bg_data_url = f"data:image/png;base64,{bg_bytes}" if bg_bytes else ""
    
    # Calculate rocks for this level
    num_rocks = 5 + st.session_state.level
    
    # Layout: Video on left, Score panel on right
    col1, col2 = st.columns([3, 1])
    
    # Load moonrock image
    moonrock_img_data = load_moonrock_image()
    moonrock_data_url = f"data:image/png;base64,{moonrock_img_data}" if moonrock_img_data else ""
    
    # JavaScript MediaPipe Game with ALL features
    game_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js"></script>
            <style>
                body {{ margin:0; padding:0; background:#0a0e27; font-family: 'Orbitron', sans-serif; }}
                #gameCanvas {{ width:100%; height:100%; border-radius:8px; box-shadow: 0 0 20px rgba(99,102,241,0.5); }}
            </style>
        </head>
        <body>
            <div style="position: relative; width: 100%; height: 650px;">
                <video id="video" style="display:none;"></video>
                <canvas id="gameCanvas" width="640" height="480"></canvas>
            </div>
            
            <script>
                // --- STREAMLIT CUSTOM COMPONENT HANDSHAKE ---
                function sendToStreamlit(type, data) {{
                    var outData = Object.assign({{
                        isStreamlitMessage: true,
                        type: type,
                    }}, data);
                    window.parent.postMessage(outData, "*");
                }}
                
                // Initialize component so Streamlit opens the iframe
                sendToStreamlit("streamlit:componentReady", {{apiVersion: 1}});
                sendToStreamlit("streamlit:setFrameHeight", {{height: 650}});
                
                // Helper to return values to Python backend
                function returnToPython(val) {{
                    sendToStreamlit("streamlit:setComponentValue", {{value: val}});
                }}
                // ---------------------------------------------
                
                const video = document.getElementById('video');
                const canvas = document.getElementById('gameCanvas');
                const ctx = canvas.getContext('2d');
                
                // Game state
                let score = {st.session_state.score};
                let level = {st.session_state.level};
                let moonrocks = [];
                let startTime = Date.now();
                const LEVEL_TIME = 30;
                const NUM_ROCKS = {num_rocks};
                let combo = 0;
                let lastCollectTime = 0;
                let peaceLastTrigger = 0;
                let thumbsLastTrigger = 0;
                let peaceDisplayUntil = 0;
                let thumbsDisplayUntil = 0;
                let gameOver = false;
                let levelComplete = false;
                let snapshotTaken = false;
                let autoAdvanceTriggered = false;
                let lastBeepSecond = -1;
                
                // Load background image
                const bgImage = new Image();
                bgImage.src = '{bg_data_url}';
                
                // Load moonrock image
                const moonrockImage = new Image();
                moonrockImage.src = '{moonrock_data_url}';
                
                // Load audio files with user interaction unlock
                const collectSound = new Audio('https://raw.githubusercontent.com/gastondana627/lunar-loot/main/sounds/collect.wav');
                const completeSound = new Audio('https://raw.githubusercontent.com/gastondana627/lunar-loot/main/sounds/level_complete.wav');
                const failSound = new Audio('https://raw.githubusercontent.com/gastondana627/lunar-loot/main/sounds/level_failed.wav');
                const beepSound = new Audio('https://raw.githubusercontent.com/gastondana627/lunar-loot/main/sounds/Beep.wav');
                
                // Unlock audio on first user interaction
                let audioUnlocked = false;
                document.addEventListener('click', () => {{
                    if (!audioUnlocked) {{
                        collectSound.play().then(() => collectSound.pause()).catch(() => {{}});
                        audioUnlocked = true;
                    }}
                }}, {{ once: true }});
                
                // Initialize moonrocks (avoid score panel area on right initially)
                // Base speed increases with level
                const baseSpeed = 0.5 + ({st.session_state.level} * 0.3);
                
                for (let i = 0; i < NUM_ROCKS; i++) {{
                    const angle = Math.random() * Math.PI * 2;
                    const speed = baseSpeed * (0.8 + Math.random() * 0.6);
                    moonrocks.push({{
                        x: Math.random() * 420 + 30,  // Keep away from right 190px (score panel)
                        y: Math.random() * 320 + 30,  // Keep away from top 150px (score panel)
                        vx: Math.cos(angle) * speed,
                        vy: Math.sin(angle) * speed,
                        collected: false
                    }});
                }}
                
                // Clear any leftover localStorage from previous games
                localStorage.removeItem('lunar_loot_result');
                localStorage.removeItem('lunar_loot_rocks');
                localStorage.removeItem('lunar_loot_snapshot');
                
                // MediaPipe Hands
                const hands = new Hands({{
                    locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${{file}}`
                }});
                
                hands.setOptions({{
                    maxNumHands: 1,
                    modelComplexity: 1,
                    minDetectionConfidence: 0.5,
                    minTrackingConfidence: 0.5
                }});
                
                hands.onResults((results) => {{
                    // Get current time at the start of frame
                    const currentTime = Date.now() / 1000;
                    
                    // Clear canvas
                    ctx.fillStyle = '#0a0e27';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    
                    // Draw background blend
                    if (bgImage.complete) {{
                        ctx.globalAlpha = 0.3;
                        ctx.drawImage(bgImage, 0, 0, canvas.width, canvas.height);
                        ctx.globalAlpha = 1.0;
                    }}
                    
                    // Draw video
                    ctx.globalAlpha = 0.7;
                    ctx.drawImage(results.image, 0, 0, canvas.width, canvas.height);
                    ctx.globalAlpha = 1.0;
                    
                    // Draw background overlay (40% transparency - fixed for stability)
                    if (bgImage.complete) {{
                        ctx.globalAlpha = 0.4;
                        ctx.drawImage(bgImage, 0, 0, canvas.width, canvas.height);
                        ctx.globalAlpha = 1.0;
                    }}
                    
                    // Update and draw moonrocks
                    moonrocks.forEach(rock => {{
                        if (!rock.collected && !gameOver && !levelComplete) {{
                            // Zero-gravity drift update
                            rock.x += rock.vx;
                            rock.y += rock.vy;
                            
                            // Bounce off canvas boundaries (with a 30px padding for the rock's radius)
                            if (rock.x < 30 || rock.x > canvas.width - 30) {{
                                rock.vx *= -1;
                                rock.x = rock.x < 30 ? 30 : canvas.width - 30;
                            }}
                            if (rock.y < 30 || rock.y > canvas.height - 30) {{
                                rock.vy *= -1;
                                rock.y = rock.y < 30 ? 30 : canvas.height - 30;
                            }}
                        }}
                        
                        if (!rock.collected && moonrockImage.complete) {{
                            // Glow effect
                            ctx.shadowBlur = 15;
                            ctx.shadowColor = '#FF69B4';
                            // Draw moonrock image
                            ctx.drawImage(moonrockImage, rock.x - 30, rock.y - 30, 60, 60);
                            ctx.shadowBlur = 0;
                        }}
                    }});
                    
                    // Process hand landmarks
                    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0 && !gameOver && !levelComplete) {{
                        const landmarks = results.multiHandLandmarks[0];
                        
                        // Draw hand skeleton (thinner lines)
                        ctx.strokeStyle = '#00FF00';
                        ctx.lineWidth = 1.5;
                        const connections = [
                            [0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],
                            [0,9],[9,10],[10,11],[11,12],[0,13],[13,14],[14,15],[15,16],
                            [0,17],[17,18],[18,19],[19,20],[5,9],[9,13],[13,17]
                        ];
                        
                        connections.forEach(([start, end]) => {{
                            ctx.beginPath();
                            ctx.moveTo(landmarks[start].x * canvas.width, landmarks[start].y * canvas.height);
                            ctx.lineTo(landmarks[end].x * canvas.width, landmarks[end].y * canvas.height);
                            ctx.stroke();
                        }});
                        
                        // Get index finger tip
                        const indexTip = landmarks[8];
                        const fingerX = indexTip.x * canvas.width;
                        const fingerY = indexTip.y * canvas.height;
                        
                        // Dynamic finger indicator size (grows with combo and level)
                        const baseSize = 15;
                        const comboBonus = combo * 2;
                        const levelBonus = {st.session_state.level} * 0.5;
                        const indicatorSize = baseSize + comboBonus + levelBonus;
                        
                        // Draw finger indicator with glow
                        ctx.shadowBlur = 12;
                        ctx.shadowColor = '#22C55E';
                        ctx.fillStyle = '#22C55E';
                        ctx.beginPath();
                        ctx.arc(fingerX, fingerY, indicatorSize, 0, Math.PI * 2);
                        ctx.fill();
                        ctx.shadowBlur = 0;
                        ctx.strokeStyle = '#FFFFFF';
                        ctx.lineWidth = 2;
                        ctx.stroke();
                        
                        // Collision detection with combo system
                        moonrocks.forEach(rock => {{
                            if (!rock.collected) {{
                                const dist = Math.sqrt((fingerX - rock.x)**2 + (fingerY - rock.y)**2);
                                if (dist < 50) {{
                                    rock.collected = true;
                                    
                                    // Play collect sound
                                    collectSound.currentTime = 0;
                                    collectSound.play().catch(e => console.log('Audio play failed:', e));
                                    
                                    // Combo system
                                    if (currentTime - lastCollectTime < 2.0) {{
                                        combo++;
                                    }} else {{
                                        combo = 0;
                                    }}
                                    
                                    const points = 10 * (combo + 1);
                                    score += points;
                                    lastCollectTime = currentTime;
                                }}
                            }}
                        }});
                        
                        // Easter eggs - Peace sign
                        const indexPip = landmarks[6];
                        const middleTip = landmarks[12];
                        const middlePip = landmarks[10];
                        const ringTip = landmarks[16];
                        const ringMcp = landmarks[13];
                        const pinkyTip = landmarks[20];
                        const pinkyMcp = landmarks[17];
                        
                        const indexExtended = indexTip.y < indexPip.y;
                        const middleExtended = middleTip.y < middlePip.y;
                        const ringCurled = ringTip.y > ringMcp.y;
                        const pinkyCurled = pinkyTip.y > pinkyMcp.y;
                        
                        // Thumbs up gesture (check FIRST - more specific)
                        const thumb = landmarks[4];
                        const thumbExtended = thumb.y < landmarks[2].y;
                        const allFingersCurled = !indexExtended && !middleExtended && ringCurled && pinkyCurled;
                        
                        if (thumbExtended && allFingersCurled && currentTime - thumbsLastTrigger > 6.0) {{
                            score += 100;
                            thumbsLastTrigger = currentTime;
                            thumbsDisplayUntil = currentTime + 2.5; // Display for 2.5 seconds
                            peaceDisplayUntil = 0; // Cancel peace display
                        }}
                        // Peace sign gesture (check SECOND - stricter detection)
                        else if (indexExtended && middleExtended && ringCurled && pinkyCurled && 
                            currentTime - peaceLastTrigger > 6.0 && !thumbExtended &&
                            currentTime > thumbsDisplayUntil) {{ // Don't trigger during thumbs display
                            score += 50;
                            peaceLastTrigger = currentTime;
                            peaceDisplayUntil = currentTime + 2.5; // Display for 2.5 seconds
                            thumbsDisplayUntil = 0; // Cancel thumbs display
                        }}
                    }}
                    
                    // Calculate game state
                    const elapsed = (Date.now() - startTime) / 1000;
                    const remaining = Math.max(0, LEVEL_TIME - elapsed);
                    const rocksLeft = moonrocks.filter(r => !r.collected).length;
                    
                    // Beep sound for last 10 seconds
                    const currentSecond = Math.floor(remaining);
                    if (remaining > 0 && remaining <= 10 && currentSecond !== lastBeepSecond) {{
                        lastBeepSecond = currentSecond;
                        beepSound.currentTime = 0;
                        beepSound.play().catch(e => console.log('Audio play failed:', e));
                    }}
                    
                    // Draw compact score panel (top right corner, smaller)
                    const panelWidth = 180;
                    const panelHeight = combo > 0 ? 140 : 120;
                    const panelX = canvas.width - panelWidth - 10;
                    const panelY = 10;
                    
                    ctx.fillStyle = 'rgba(10, 14, 39, 0.9)';
                    ctx.fillRect(panelX, panelY, panelWidth, panelHeight);
                    ctx.strokeStyle = 'rgba(99, 102, 241, 0.6)';
                    ctx.lineWidth = 1;
                    ctx.strokeRect(panelX, panelY, panelWidth, panelHeight);
                    
                    ctx.fillStyle = '#6366f1';
                    ctx.font = 'bold 16px Orbitron';
                    ctx.fillText('{st.session_state.spacetag or "Player"}', panelX + 10, panelY + 25);
                    
                    ctx.fillStyle = '#FFFFFF';
                    ctx.font = '14px Orbitron';
                    ctx.fillText('Score:', panelX + 10, panelY + 50);
                    ctx.fillStyle = '#22C55E';
                    ctx.fillText(score.toString(), panelX + 70, panelY + 50);
                    
                    ctx.fillStyle = '#FFFFFF';
                    ctx.fillText(`Level: {st.session_state.level}`, panelX + 10, panelY + 70);
                    
                    ctx.fillStyle = remaining < 10 ? '#EF4444' : '#FFFFFF';
                    ctx.fillText(`Time: ${{Math.floor(remaining)}}s`, panelX + 10, panelY + 90);
                    
                    ctx.fillStyle = '#FFFFFF';
                    ctx.fillText(`Rocks: ${{rocksLeft}}`, panelX + 10, panelY + 110);
                    
                    if (combo > 0) {{
                        ctx.fillStyle = '#22C55E';
                        ctx.font = 'bold 14px Orbitron';
                        ctx.fillText(`COMBO x${{combo + 1}}!`, panelX + 10, panelY + 130);
                    }}
                    
                    // Display gesture bonuses (persistent for 2 seconds)
                    if (currentTime < peaceDisplayUntil) {{
                        ctx.fillStyle = '#22C55E';
                        ctx.font = 'bold 48px Orbitron';
                        ctx.shadowBlur = 20;
                        ctx.shadowColor = '#22C55E';
                        ctx.fillText('✌️ PEACE! +50', canvas.width/2 - 150, canvas.height/2 - 50);
                        ctx.shadowBlur = 0;
                    }}
                    
                    if (currentTime < thumbsDisplayUntil) {{
                        ctx.fillStyle = '#FFD700';
                        ctx.font = 'bold 48px Orbitron';
                        ctx.shadowBlur = 20;
                        ctx.shadowColor = '#FFD700';
                        ctx.fillText('👍 THUMBS UP! +100', canvas.width/2 - 180, canvas.height/2 - 50);
                        ctx.shadowBlur = 0;
                    }}
                    
                    // Check win/lose conditions - AUTO ADVANCE
                    if (rocksLeft === 0 && !levelComplete) {{
                        levelComplete = true;
                        
                        // Take snapshot before overlay
                        if (!snapshotTaken) {{
                            const snapshotCanvas = document.createElement('canvas');
                            snapshotCanvas.width = canvas.width;
                            snapshotCanvas.height = canvas.height;
                            const snapCtx = snapshotCanvas.getContext('2d');
                            snapCtx.drawImage(canvas, 0, 0);
                            const snapshotData = snapshotCanvas.toDataURL('image/png');
                            localStorage.setItem('lunar_loot_snapshot', snapshotData);
                            snapshotTaken = true;
                        }}
                        
                        // GREEN overlay for success
                        ctx.fillStyle = 'rgba(34, 197, 94, 0.3)';
                        ctx.fillRect(0, 0, canvas.width, canvas.height);
                        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
                        ctx.fillRect(0, 0, canvas.width, canvas.height);
                        ctx.fillStyle = '#22C55E';
                        ctx.font = 'bold 48px Orbitron';
                        ctx.fillText('★ LEVEL COMPLETE! ★', canvas.width/2 - 250, canvas.height/2);
                        ctx.font = 'bold 32px Orbitron';
                        ctx.fillStyle = '#FFFFFF';
                        ctx.fillText(`Score: ${{score}}`, canvas.width/2 - 80, canvas.height/2 + 50);
                        
                        // Play success sound
                        completeSound.play().catch(e => console.log('Audio play failed:', e));
                        
                        // Stop camera
                        camera.stop();
                        video.srcObject.getTracks().forEach(track => track.stop());
                        
                        // AUTO ADVANCE with 10s countdown
                        if (!autoAdvanceTriggered) {{
                            autoAdvanceTriggered = true;
                            let countdown = 10;
                            const countInterval = setInterval(() => {{
                                // Clear previous text area
                                ctx.fillStyle = 'rgba(0, 0, 0, 0.9)';
                                ctx.fillRect(canvas.width/2 - 175, canvas.height/2 + 80, 350, 50);
                                ctx.fillStyle = '#22C55E';
                                ctx.font = 'bold 24px Orbitron';
                                ctx.fillText(`Advancing in ${{countdown}}s...`, canvas.width/2 - 120, canvas.height/2 + 115);
                                
                                if (countdown <= 0) {{
                                    clearInterval(countInterval);
                                    returnToPython({{result: 'complete', rocks: '0'}});
                                }}
                                countdown--;
                            }}, 1000);
                        }}
                    }} else if (remaining <= 0 && !gameOver && !levelComplete) {{
                        gameOver = true;
                        
                        // Take snapshot before overlay
                        if (!snapshotTaken) {{
                            const snapshotCanvas = document.createElement('canvas');
                            snapshotCanvas.width = canvas.width;
                            snapshotCanvas.height = canvas.height;
                            const snapCtx = snapshotCanvas.getContext('2d');
                            snapCtx.drawImage(canvas, 0, 0);
                            const snapshotData = snapshotCanvas.toDataURL('image/png');
                            localStorage.setItem('lunar_loot_snapshot', snapshotData);
                            snapshotTaken = true;
                        }}
                        
                        // RED overlay for failure
                        ctx.fillStyle = 'rgba(239, 68, 68, 0.3)';
                        ctx.fillRect(0, 0, canvas.width, canvas.height);
                        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
                        ctx.fillRect(0, 0, canvas.width, canvas.height);
                        ctx.fillStyle = '#EF4444';
                        ctx.font = 'bold 48px Orbitron';
                        ctx.fillText('TIME UP!', canvas.width/2 - 120, canvas.height/2);
                        ctx.font = 'bold 32px Orbitron';
                        ctx.fillStyle = '#FFFFFF';
                        ctx.fillText(`Final Score: ${{score}}`, canvas.width/2 - 120, canvas.height/2 + 50);
                        ctx.fillText(`Rocks Remaining: ${{rocksLeft}}`, canvas.width/2 - 150, canvas.height/2 + 90);
                        
                        // Play fail sound
                        failSound.play().catch(e => console.log('Audio play failed:', e));
                        
                        // Stop camera
                        camera.stop();
                        video.srcObject.getTracks().forEach(track => track.stop());
                        
                        // AUTO ADVANCE with 10s countdown
                        if (!autoAdvanceTriggered) {{
                            autoAdvanceTriggered = true;
                            let countdown = 10;
                            const countInterval = setInterval(() => {{
                                // Clear previous text area
                                ctx.fillStyle = 'rgba(0, 0, 0, 0.9)';
                                ctx.fillRect(canvas.width/2 - 175, canvas.height/2 + 120, 350, 50);
                                ctx.fillStyle = '#EF4444';
                                ctx.font = 'bold 24px Orbitron';
                                ctx.fillText(`Advancing in ${{countdown}}s...`, canvas.width/2 - 120, canvas.height/2 + 155);
                                
                                if (countdown <= 0) {{
                                    clearInterval(countInterval);
                                    returnToPython({{result: 'failed', rocks: rocksLeft.toString()}});
                                }}
                                countdown--;
                            }}, 1000);
                        }}
                    }}
                }});
                
                // Start camera
                const camera = new Camera(video, {{
                    onFrame: async () => {{
                        await hands.send({{image: video}});
                    }},
                    width: 640,
                    height: 480
                }});
                
                camera.start();
            </script>
        </body>
        </html>
    """
    
    # === NATIVE COMPONENT INJECTION ===
    import os
    os.makedirs("component_dist", exist_ok=True)
    with open("component_dist/index.html", "w", encoding="utf-8") as f:
        f.write(game_html)
        
    game_comp = components.declare_component("lunar_loot_game", path="component_dist")
    
    # Render component and capture the returned dictionary when Javascript fires returnToPython()
    component_value = game_comp(key=f"game_canvas_lvl_{st.session_state.level}")
    
    if component_value:
        res = component_value.get("result")
        if res == "complete":
            st.session_state.score += 100
            st.session_state.level += 1
            if st.session_state.level > MAX_LEVELS:
                save_high_score(st.session_state.spacetag, st.session_state.score, st.session_state.level)
                st.session_state.game_state = 'game_complete'
            else:
                st.session_state.game_state = 'level_complete'
            st.rerun()
        elif res == "failed":
            save_high_score(st.session_state.spacetag, st.session_state.score, st.session_state.level)
            try:
                st.session_state.rocks_remaining = int(component_value.get("rocks", 0))
            except:
                st.session_state.rocks_remaining = 0
            st.session_state.game_state = 'level_failed'
            st.rerun()
    # =======================================
    
    st.write("")
    st.info("⏱️ Level will automatically advance 10 seconds after completion.")
    
    # Pause button
    if st.button("⏸️ PAUSE GAME", use_container_width=True, key="pause_btn"):
        st.session_state.is_resuming = True
        st.session_state.game_state = 'level_start'
        st.rerun()

# ==================== LEVEL COMPLETE SCREEN ====================
elif st.session_state.game_state == 'level_complete':
    # Full screen with logo and "Level Complete" title - CLEAN
    logo_bytes = load_logo()
    
    # Hide all previous content and show only this screen
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0a4d2e 0%, #1a5f3a 50%, #0a3d2e 100%) !important;
        }
        /* Hide any iframes or components from previous state */
        iframe, .stMarkdown iframe {
            display: none !important;
        }
        /* Ensure clean screen */
        .stApp > div:first-child {
            overflow: hidden !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Centered content
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if logo_bytes:
            st.markdown(f"""
                <div style="text-align: center; margin: 40px 0;">
                    <img src="data:image/png;base64,{logo_bytes}" 
                         style="max-width: 400px; width: 70%; animation: pulse 2s ease-in-out infinite;">
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="text-align: center; margin: 30px 0;">
                <h1 style='color: #22c55e; font-size: 4rem; text-shadow: 0 0 20px rgba(34, 197, 94, 0.5); margin: 0;'>
                    ★ Level {st.session_state.level - 1}<br>Complete!
                </h1>
                <p style='color: #f8fafc; font-size: 2rem; margin: 20px 0;'>
                    <strong>Score: {st.session_state.score}</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    import time
    time.sleep(3)
    st.session_state.game_state = 'level_start'
    st.rerun()

# ==================== LEVEL FAILED SCREEN ====================
elif st.session_state.game_state == 'level_failed':
    # Dark space background
    bg_bytes = load_background(st.session_state.level)
    if bg_bytes:
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{bg_bytes});
                background-size: cover;
                background-position: center;
            }}
            .stApp::before {{
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(10, 14, 39, 0.85);
                z-index: 0;
            }}
            /* Hide any iframes or components from previous state */
            iframe, .stMarkdown iframe {{
                display: none !important;
            }}
            /* Ensure clean screen */
            .stApp > div:first-child {{
                overflow: hidden !important;
            }}
            </style>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    # Left: Game Over Stats
    with col1:
        rocks_left = st.session_state.rocks_remaining
        player_name = st.session_state.spacetag or "Anonymous"
        
        st.markdown(f"""
            <div style="background: rgba(10, 14, 39, 0.95); padding: 40px; border-radius: 12px; 
                        backdrop-filter: blur(12px); border: 2px solid rgba(239, 68, 68, 0.5); position: relative; z-index: 1;">
                <h1 style='color: #ef4444; font-size: 2.5rem; margin: 0 0 30px 0; font-weight: 700;'>
                    Game Over!
                </h1>
                
                <p style='color: #cbd5e1; font-size: 1.2rem; margin: 15px 0;'>
                    <strong>{player_name}</strong>
                </p>
                
                <p style='color: #f8fafc; font-size: 1.8rem; margin: 20px 0;'>
                    <strong>Final Score: {st.session_state.score}</strong>
                </p>
                
                <p style='color: #cbd5e1; font-size: 1.2rem; margin: 15px 0;'>
                    Level Reached: {st.session_state.level}
                </p>
                
                <div style='background: rgba(239, 68, 68, 0.2); padding: 15px; border-radius: 8px; margin: 25px 0;'>
                    <p style='color: #ef4444; font-size: 1rem; margin: 0;'>
                        Moonrocks Remaining: {rocks_left}
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Play Again", type="primary", use_container_width=True):
                st.session_state.game_state = 'level_start'
                st.rerun()
        with col_b:
            if st.button("Main Menu", use_container_width=True):
                st.session_state.score = 0
                st.session_state.level = 1
                st.session_state.game_state = 'title'
                st.rerun()
    
    # Right: Snapshot with download
    with col2:
        st.markdown("""
            <div style="background: rgba(10, 14, 39, 0.95); padding: 20px; border-radius: 12px; 
                        backdrop-filter: blur(12px); border: 2px solid rgba(239, 68, 68, 0.5); position: relative; z-index: 1; margin-bottom: 20px;">
                <h3 style='color: #f8fafc; text-align: center; margin: 0;'>Your Space Selfie!</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Snapshot capture and download
        snapshot_html = """
            <div style="text-align: center; position: relative; z-index: 1;">
                <canvas id="snapshotCanvas" width="640" height="480" style="max-width: 100%; border-radius: 8px; border: 2px solid #ef4444; margin-bottom: 20px;"></canvas>
                <br>
                <a id="downloadLink" download="lunar_loot_spaceshot.png" style="display: inline-block; padding: 14px 28px; background: #ef4444; color: white; text-decoration: none; border-radius: 8px; font-weight: 600; font-family: Orbitron; font-size: 1rem;">
                    Download Selfie
                </a>
            </div>
            <script>
                const canvas = document.getElementById('snapshotCanvas');
                const ctx = canvas.getContext('2d');
                const snapshot = localStorage.getItem('lunar_loot_snapshot');
                
                if (snapshot) {
                    const img = new Image();
                    img.onload = () => {
                        ctx.drawImage(img, 0, 0);
                        document.getElementById('downloadLink').href = snapshot;
                    };
                    img.src = snapshot;
                } else {
                    ctx.fillStyle = '#1a1f3a';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    ctx.fillStyle = '#ef4444';
                    ctx.font = '24px Orbitron';
                    ctx.textAlign = 'center';
                    ctx.fillText('Snapshot Captured!', canvas.width/2, canvas.height/2);
                }
            </script>
        """
        components.html(snapshot_html, height=600)

# ==================== GAME COMPLETE SCREEN ====================
elif st.session_state.game_state == 'game_complete':
    logo_bytes = load_logo()
    
    # Clean screen - hide all previous content
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0a4d2e 0%, #1a5f3a 50%, #0a3d2e 100%) !important;
        }
        /* Hide any iframes or components from previous state */
        iframe, .stMarkdown iframe {
            display: none !important;
        }
        /* Ensure clean screen */
        .stApp > div:first-child {
            overflow: hidden !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Centered content
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if logo_bytes:
            st.markdown(f"""
                <div style="text-align: center; margin: 40px 0;">
                    <img src="data:image/png;base64,{logo_bytes}" 
                         style="max-width: 400px; width: 70%; animation: pulse 2s ease-in-out infinite;">
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="text-align: center; margin: 30px 0; background: rgba(10, 14, 39, 0.9); padding: 40px; border-radius: 20px; border: 2px solid rgba(34, 197, 94, 0.5);">
                <h1 style='color: #22c55e; font-size: 3.5rem; text-shadow: 0 0 20px rgba(34, 197, 94, 0.5); margin: 20px 0;'>
                    🎉 IGC Journey Complete! 🎉
                </h1>
                <p style='color: #f8fafc; font-size: 2rem; margin: 30px 0;'>
                    <strong>Final Score: {st.session_state.score}</strong>
                </p>
                <p style='color: #cbd5e1; font-size: 1.5rem; margin: 20px 0;'>
                    Levels Completed: {MAX_LEVELS}
                </p>
                <p style='color: #22c55e; font-size: 1.2rem; margin: 30px 0; font-style: italic;'>
                    You've successfully collected moonrocks across all sectors!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 PLAY AGAIN", type="primary", use_container_width=True):
                st.session_state.score = 0
                st.session_state.level = 1
                st.session_state.game_state = 'title'
                st.rerun()
        with col_b:
            if st.button("🏠 MAIN MENU", use_container_width=True):
                st.session_state.score = 0
                st.session_state.level = 1
                st.session_state.game_state = 'title'
                st.rerun()

# ==================== HALL OF FAME SCREEN ====================
elif st.session_state.game_state == 'leaderboard':
    main_bg = load_main_menu_bg()
    if main_bg:
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{main_bg});
                background-size: cover;
                background-position: center;
            }}
            </style>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        /* Neon Grid & Typography */
        .hof-title {
            text-align: center;
            font-size: 4rem;
            font-weight: 900;
            color: #e0f7fa;
            text-shadow: 0 0 10px #00f3ff, 0 0 20px #8b5cf6, 0 0 40px #8b5cf6;
            margin-bottom: 5px;
            letter-spacing: 4px;
        }
        .hof-subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: #94a3b8;
            letter-spacing: 2px;
            margin-bottom: 50px;
        }
        
        /* Podium Cards */
        .podium-card {
            background: rgba(10, 16, 40, 0.7);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 30px;
            text-align: center;
            position: relative;
            margin-bottom: 20px;
            color: white;
            transition: transform 0.3s ease;
        }
        .podium-card:hover {
            transform: scale(1.02);
        }
        
        /* Gold (1st) */
        .card-gold {
            border: 2px solid #fbbf24;
            box-shadow: 0 0 20px rgba(251, 191, 36, 0.4), inset 0 0 20px rgba(251, 191, 36, 0.1);
            transform: scale(1.05);
            z-index: 10;
        }
        .card-gold h2 { color: #fbbf24; text-shadow: 0 0 10px #fbbf24; }
        
        /* Silver (2nd) */
        .card-silver {
            border: 2px solid #e2e8f0;
            box-shadow: 0 0 15px rgba(226, 232, 240, 0.3), inset 0 0 15px rgba(226, 232, 240, 0.1);
        }
        .card-silver h2 { color: #e2e8f0; text-shadow: 0 0 10px #e2e8f0; }
        
        /* Bronze (3rd) */
        .card-bronze {
            border: 2px solid #b45309;
            box-shadow: 0 0 15px rgba(180, 83, 9, 0.4), inset 0 0 15px rgba(180, 83, 9, 0.1);
        }
        .card-bronze h2 { color: #b45309; text-shadow: 0 0 10px #b45309; }
        
        /* Ranks List Table */
        .rank-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0 10px;
            margin-top: 40px;
        }
        .rank-table th {
            color: #64748b;
            text-align: left;
            padding: 10px 20px;
            font-size: 0.9rem;
            letter-spacing: 2px;
            border-bottom: 1px solid rgba(99, 102, 241, 0.3);
        }
        .rank-table td {
            background: rgba(10, 16, 40, 0.6);
            backdrop-filter: blur(5px);
            padding: 15px 20px;
            color: #cbd5e1;
            font-size: 1.1rem;
        }
        .rank-table tr td:first-child { border-top-left-radius: 8px; border-bottom-left-radius: 8px; border-left: 2px solid transparent;}
        .rank-table tr td:last-child { border-top-right-radius: 8px; border-bottom-right-radius: 8px; border-right: 2px solid transparent;}
        
        .rank-table tr:hover td {
            background: rgba(99, 102, 241, 0.15);
        }
        
        /* Glow for specifically the user's row if needed, or alternating borders */
        .row-accent td {
            border-top: 1px solid #00f3ff;
            border-bottom: 1px solid #00f3ff;
            background: rgba(0, 243, 255, 0.15);
        }
        .row-accent td:first-child { border-left: 1px solid #00f3ff; }
        .row-accent td:last-child { border-right: 1px solid #00f3ff; }
        
        .rank-num { color: #94a3b8; font-weight: bold; }
        .score-val { color: #00f3ff; font-weight: bold; font-family: monospace; font-size: 1.3rem !important;}
        .level-badge {
            background: rgba(255,255,255,0.1);
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.8rem;
        }
        
        /* Stats block in cards */
        .stat-block {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
            border-top: 1px solid rgba(255,255,255,0.1);
            padding-top: 15px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="hof-title">HALL OF FAME</div>', unsafe_allow_html=True)
    st.markdown('<div class="hof-subtitle">GLOBAL TACTICAL RANKINGS AND PILOT EXCELLENCE</div>', unsafe_allow_html=True)
    
    col_back, col_b2, col_b3 = st.columns([1, 4, 1])
    with col_back:
        if st.button("◀ BACK", use_container_width=True):
            st.session_state.game_state = 'intro'
            st.rerun()
        
    st.write("")
    
    scores = load_high_scores()
    
    if not scores:
        st.info("No flight records found. Be the first to enter the Hall of Fame!")
    else:
        # Podium
        col1, col2, col3 = st.columns([1, 1.1, 1])
        
        # Rank 2 (Silver)
        if len(scores) >= 2:
            with col1:
                st.markdown(f"""
                <div class="podium-card card-silver">
                    <h1 style="margin:0; font-size: 3rem;">🥈</h1>
                    <h2>{scores[1].get('spacetag', 'UNKNOWN')}</h2>
                    <p style="color: #94a3b8; font-size: 0.9rem;">SILVER BADGE</p>
                    <div class="stat-block">
                        <div><div style="font-size: 0.8rem; color: #64748b;">SCORE</div><div style="color: #00f3ff; font-weight: bold;">{scores[1].get('score')}</div></div>
                        <div><div style="font-size: 0.8rem; color: #64748b;">LEVEL</div><div style="color: white; font-weight: bold;">LVL {scores[1].get('level')}</div></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Rank 1 (Gold)
        if len(scores) >= 1:
            with col2:
                st.markdown(f"""
                <div class="podium-card card-gold">
                    <h1 style="margin:0; font-size: 4rem;">🏆</h1>
                    <h2 style="font-size: 2rem;">{scores[0].get('spacetag', 'UNKNOWN')}</h2>
                    <p style="color: #fbbf24; font-size: 1rem; font-weight: bold;">CHAMPION'S GOLD</p>
                    <div class="stat-block">
                        <div><div style="font-size: 0.8rem; color: #fbbf24;">HIGH SCORE</div><div style="color: #00f3ff; font-size: 1.5rem; font-weight: bold;">{scores[0].get('score')}</div></div>
                        <div><div style="font-size: 0.8rem; color: #fbbf24;">LEVEL</div><div style="color: white; font-size: 1.5rem; font-weight: bold;">LVL {scores[0].get('level')}</div></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        # Rank 3 (Bronze)
        if len(scores) >= 3:
            with col3:
                st.markdown(f"""
                <div class="podium-card card-bronze">
                    <h1 style="margin:0; font-size: 3rem;">🥉</h1>
                    <h2>{scores[2].get('spacetag', 'UNKNOWN')}</h2>
                    <p style="color: #94a3b8; font-size: 0.9rem;">BRONZE BADGE</p>
                    <div class="stat-block">
                        <div><div style="font-size: 0.8rem; color: #64748b;">SCORE</div><div style="color: #00f3ff; font-weight: bold;">{scores[2].get('score')}</div></div>
                        <div><div style="font-size: 0.8rem; color: #64748b;">LEVEL</div><div style="color: white; font-weight: bold;">LVL {scores[2].get('level')}</div></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Rankings Table (4 through 10)
        table_html = """
        <table class="rank-table" style="width: 100%;">
            <thead>
                <tr>
                    <th>RANK</th>
                    <th>PILOT SPACETAG</th>
                    <th>HIGH SCORE</th>
                    <th>LEVEL ACHIEVED</th>
                    <th>DATE RECORDED</th>
                </tr>
            </thead>
            <tbody>
        """
        for i, s in enumerate(scores[3:10]): # type: ignore
            rank = i + 4
            row_class = "row-accent" if s.get('spacetag') == st.session_state.spacetag else ""
            date_str = "UNKNOWN"
            if 'timestamp' in s:
                try:
                    date_str = s['timestamp'][:10] # YYYY-MM-DD
                except: pass
                
            table_html += f"""
            <tr class="{row_class}">
                <td class="rank-num">#{rank:02d}</td>
                <td style="font-weight: bold;">{s.get('spacetag', 'UNKNOWN')}</td>
                <td class="score-val">{s.get('score', 0):,}</td>
                <td><span class="level-badge">LVL {s.get('level', 1)}</span></td>
                <td style="color: #64748b; font-size: 0.9rem;">{date_str}</td>
            </tr>
            """
        
        table_html += "</tbody></table>"
        if len(scores) > 3:
            st.markdown(table_html, unsafe_allow_html=True)
