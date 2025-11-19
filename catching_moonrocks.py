## Lunar Loot - COMPLETE Production Version
## Created for Chroma Awards 2025
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
    </style>
""", unsafe_allow_html=True)

# Chroma Awards Footer with animation
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
        st.markdown("""
            <div style="position: fixed; bottom: 0; left: 0; width: 100%; z-index: 9998; 
                        background: rgba(0,0,0,0.9); padding: 10px; text-align: center;">
                <a href="https://www.chromaawards.com" target="_blank" style="color: #6366f1; text-decoration: none; font-size: 14px;">
                    🏆 Chroma Awards 2025
                </a>
            </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div style="position: fixed; bottom: 0; left: 0; width: 100%; z-index: 9998; 
                    background: rgba(0,0,0,0.9); padding: 10px; text-align: center;">
            <a href="https://www.chromaawards.com" target="_blank" style="color: #6366f1; text-decoration: none; font-size: 14px;">
                🏆 Chroma Awards 2025
            </a>
        </div>
    """, unsafe_allow_html=True)

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
    
    # Music toggle in top right
    if 'music_playing' not in st.session_state:
        st.session_state.music_playing = False
    
    # Background music player
    music_html = f"""
        <div style="position: fixed; top: 20px; right: 80px; z-index: 9999;">
            <button onclick="toggleMusic()" style="background: rgba(10, 14, 39, 0.9); border: 2px solid #6366f1; 
                    border-radius: 50%; width: 50px; height: 50px; cursor: pointer; font-size: 24px;">
                <span id="musicIcon">🔊</span>
            </button>
        </div>
        <audio id="bgMusic" loop>
            <source src="https://raw.githubusercontent.com/gastondana627/lunar-loot/main/sounds/menu_theme.wav" type="audio/wav">
        </audio>
        <script>
            const music = document.getElementById('bgMusic');
            const icon = document.getElementById('musicIcon');
            let isPlaying = false;
            
            function toggleMusic() {{
                if (isPlaying) {{
                    music.pause();
                    icon.textContent = '🔇';
                    isPlaying = false;
                }} else {{
                    music.play().catch(e => console.log('Audio play failed:', e));
                    icon.textContent = '🔊';
                    isPlaying = true;
                }}
            }}
            
            // Auto-play on first interaction
            document.addEventListener('click', () => {{
                if (!isPlaying) {{
                    toggleMusic();
                }}
            }}, {{ once: true }});
        </script>
    """
    st.markdown(music_html, unsafe_allow_html=True)
    
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
        st.markdown("""
            <div style="background: rgba(0,0,0,0.85); padding: 40px; border-radius: 20px; 
                        text-align: center; backdrop-filter: blur(10px); border: 2px solid rgba(99, 102, 241, 0.5);">
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h1 style='color: #6366f1; font-size: 3rem;'>Level {st.session_state.level}</h1>", unsafe_allow_html=True)
        sector_name = SECTOR_NAMES.get(st.session_state.level, "Unknown Sector")
        st.markdown(f"<h2 style='color: #cbd5e1; font-size: 2rem;'>Sector: {sector_name}</h2>", unsafe_allow_html=True)
        
        st.write("")
        st.markdown(f"<p style='font-size: 1.2rem;'><strong>Current Score:</strong> {st.session_state.score}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 1.2rem;'><strong>Pilot:</strong> {st.session_state.spacetag or 'Anonymous'}</p>", unsafe_allow_html=True)
        st.write("")
        
        rocks_count = 5 + st.session_state.level
        st.info(f"💎 Collect {rocks_count} moonrocks in 30 seconds!")
        st.success("⚡ Build combos by collecting rocks quickly!")
        
        st.write("")
        # Show "RESUME" if coming from pause, otherwise "BEGIN"
        button_text = "▶️ RESUME MISSION" if st.session_state.is_resuming else "▶️ BEGIN MISSION"
        if st.button(button_text, type="primary", use_container_width=True):
            st.session_state.is_resuming = False  # Reset flag
            st.session_state.game_state = 'playing'
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

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
                
                // Initialize moonrocks (avoid score panel area on right)
                for (let i = 0; i < NUM_ROCKS; i++) {{
                    moonrocks.push({{
                        x: Math.random() * 420 + 30,  // Keep away from right 190px (score panel)
                        y: Math.random() * 320 + 30,  // Keep away from top 150px (score panel)
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
                    
                    // Draw moonrocks with actual image
                    moonrocks.forEach(rock => {{
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
                        
                        // AUTO ADVANCE after 2 seconds
                        if (!autoAdvanceTriggered) {{
                            autoAdvanceTriggered = true;
                            setTimeout(() => {{
                                // Store result in localStorage for polling script
                                localStorage.setItem('lunar_loot_result', 'complete');
                                localStorage.setItem('lunar_loot_rocks', '0');
                            }}, 2000);
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
                        
                        // AUTO ADVANCE after 2 seconds
                        if (!autoAdvanceTriggered) {{
                            autoAdvanceTriggered = true;
                            setTimeout(() => {{
                                // Store result in localStorage for polling script
                                localStorage.setItem('lunar_loot_result', 'failed');
                                localStorage.setItem('lunar_loot_rocks', rocksLeft.toString());
                            }}, 2000);
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
    
    # Full width game (score is now inside the canvas on the right)
    components.html(game_html, height=600, scrolling=False)
    
    st.write("")
    st.success("🎮 Game will automatically advance when timer expires or all rocks are collected!")
    
    # Pause button only
    if st.button("⏸️ PAUSE GAME", use_container_width=True, key="pause_btn"):
        st.session_state.is_resuming = True  # Set flag for resume
        st.session_state.game_state = 'level_start'
        st.rerun()
    
    # Auto-advance polling mechanism - searches parent window
    auto_advance_html = """
        <script>
        let pollCount = 0;
        const maxPolls = 40; // 20 seconds max
        
        const pollInterval = setInterval(() => {
            pollCount++;
            
            try {
                const result = localStorage.getItem('lunar_loot_result');
                const rocksLeft = localStorage.getItem('lunar_loot_rocks');
                
                if (result) {
                    console.log('Found result:', result, 'rocks:', rocksLeft);
                    
                    // Clear localStorage
                    localStorage.removeItem('lunar_loot_result');
                    localStorage.removeItem('lunar_loot_rocks');
                    
                    // Search in parent window for Streamlit buttons
                    let clicked = false;
                    const searchButtons = (doc) => {
                        const buttons = doc.querySelectorAll('button');
                        buttons.forEach(btn => {
                            const text = btn.textContent || btn.innerText || '';
                            console.log('Checking button:', text);
                            if (result === 'complete' && (text.includes('🎯') || text.includes('AUTO_COMPLETE')) && !clicked) {
                                console.log('Clicking complete button!');
                                btn.click();
                                clicked = true;
                                clearInterval(pollInterval);
                            } else if (result === 'failed' && (text.includes('⏱️') || text.includes('AUTO_FAIL')) && !clicked) {
                                console.log('Clicking fail button!');
                                btn.click();
                                clicked = true;
                                clearInterval(pollInterval);
                            }
                        });
                    };
                    
                    // Try current document
                    searchButtons(document);
                    
                    // Try parent if available
                    if (!clicked && window.parent && window.parent.document) {
                        try {
                            searchButtons(window.parent.document);
                        } catch(e) {
                            console.log('Cannot access parent:', e);
                        }
                    }
                    
                    // Try top if available
                    if (!clicked && window.top && window.top.document) {
                        try {
                            searchButtons(window.top.document);
                        } catch(e) {
                            console.log('Cannot access top:', e);
                        }
                    }
                }
                
                if (pollCount >= maxPolls) {
                    console.log('Polling timeout');
                    clearInterval(pollInterval);
                }
            } catch(e) {
                console.log('Polling error:', e);
            }
        }, 500);
        </script>
    """
    components.html(auto_advance_html, height=0)
    
    # Hidden auto-trigger buttons (invisible but clickable)
    st.markdown("""
        <style>
        button[kind="secondary"] p {
            font-size: 0 !important;
            line-height: 0 !important;
        }
        button[kind="secondary"] {
            opacity: 0 !important;
            position: absolute !important;
            left: -9999px !important;
            pointer-events: auto !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎯 AUTO_COMPLETE", key="auto_complete", use_container_width=False):
            st.session_state.score += 100  # Bonus for completing
            st.session_state.level += 1
            
            # Check if all levels complete
            if st.session_state.level > MAX_LEVELS:
                st.session_state.game_state = 'game_complete'
            else:
                st.session_state.game_state = 'level_complete'
            st.rerun()
    with col2:
        if st.button("⏱️ AUTO_FAIL", key="auto_fail", use_container_width=False):
            # Get rocks remaining from localStorage if available
            try:
                rocks_str = st.query_params.get('rocks', '0')
                st.session_state.rocks_remaining = int(rocks_str) if rocks_str else 0
            except:
                st.session_state.rocks_remaining = 0
            st.session_state.game_state = 'level_failed'
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
    
    # Auto-advance to next level after 3 seconds
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
