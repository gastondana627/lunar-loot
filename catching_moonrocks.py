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

# Background files mapping
BACKGROUND_FILES = {
    1: "Mercury_1.png", 2: "Mars_1.png", 3: "Venus_1.png", 4: "Moon_1.png",
    5: "Saturn_1.png", 6: "Earth_1.png", 7: "Uranus_1.png", 8: "Uranus_1.png",
    9: "PlanetX_1.png", 10: "Ceres_1.png", 11: "Comet_3I_Atlas_1.png",
    12: "Oumuamua_1.png", 13: "PlanetX_1.png", 14: "Spaceship_1.png"
}

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
    st.session_state.game_state = 'title'
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'spacetag' not in st.session_state:
    st.session_state.spacetag = ''

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

# Chroma Awards Footer
st.markdown("""
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; z-index: 9998; 
                background: rgba(0,0,0,0.9); padding: 10px; text-align: center;">
        <a href="https://www.chromaawards.com" target="_blank" style="color: #6366f1; text-decoration: none; font-size: 14px;">
            🏆 Chroma Awards 2025
        </a>
    </div>
""", unsafe_allow_html=True)

# ==================== TITLE SCREEN ====================
if st.session_state.game_state == 'title':
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
    
    col1, col2 = st.columns([1, 1])
    with col1:
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
        if st.button("▶️ BEGIN MISSION", type="primary", use_container_width=True):
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
                let gameOver = false;
                let levelComplete = false;
                let snapshotTaken = false;
                
                // Load background image
                const bgImage = new Image();
                bgImage.src = '{bg_data_url}';
                
                // Load moonrock image
                const moonrockImage = new Image();
                moonrockImage.src = '{moonrock_data_url}';
                
                // Initialize moonrocks
                for (let i = 0; i < NUM_ROCKS; i++) {{
                    moonrocks.push({{
                        x: Math.random() * 580 + 30,
                        y: Math.random() * 420 + 30,
                        collected: false
                    }});
                }}
                
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
                        
                        // Draw hand skeleton
                        ctx.strokeStyle = '#00FF00';
                        ctx.lineWidth = 2;
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
                        
                        // Draw finger indicator with glow
                        ctx.shadowBlur = 10;
                        ctx.shadowColor = '#22C55E';
                        ctx.fillStyle = '#22C55E';
                        ctx.beginPath();
                        ctx.arc(fingerX, fingerY, 20, 0, Math.PI * 2);
                        ctx.fill();
                        ctx.shadowBlur = 0;
                        ctx.strokeStyle = '#FFFFFF';
                        ctx.lineWidth = 2;
                        ctx.stroke();
                        
                        // Collision detection with combo system
                        const currentTime = Date.now() / 1000;
                        moonrocks.forEach(rock => {{
                            if (!rock.collected) {{
                                const dist = Math.sqrt((fingerX - rock.x)**2 + (fingerY - rock.y)**2);
                                if (dist < 50) {{
                                    rock.collected = true;
                                    
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
                        
                        if (indexExtended && middleExtended && ringCurled && pinkyCurled && 
                            currentTime - peaceLastTrigger > 5.0) {{
                            score += 50;
                            peaceLastTrigger = currentTime;
                            // Show bonus text
                            ctx.fillStyle = '#22C55E';
                            ctx.font = 'bold 36px Orbitron';
                            ctx.fillText('✌️ PEACE! +50', canvas.width/2 - 120, canvas.height/2);
                        }}
                    }}
                    
                    // Update game state for external UI
                    const elapsed = (Date.now() - startTime) / 1000;
                    const remaining = Math.max(0, LEVEL_TIME - elapsed);
                    const rocksLeft = moonrocks.filter(r => !r.collected).length;
                    
                    // Send state to parent for UI display
                    window.parent.postMessage({{
                        type: 'gameState',
                        score: score,
                        time: Math.floor(remaining),
                        rocks: rocksLeft,
                        combo: combo
                    }}, '*');
                    
                    // Check win/lose conditions
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
                            window.parent.postMessage({{type: 'snapshot', data: snapshotData}}, '*');
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
                        
                        // Redirect to trigger level complete
                        setTimeout(() => {{
                            window.top.location.href = window.top.location.pathname + '?game_result=complete&score=' + score;
                        }}, 2000);
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
                            window.parent.postMessage({{type: 'snapshot', data: snapshotData}}, '*');
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
                        
                        setTimeout(() => {{
                            window.top.location.href = window.top.location.pathname + '?game_result=failed&score=' + score;
                        }}, 2000);
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
    
    with col1:
        components.html(game_html, height=600)
    
    with col2:
        # Score Panel (like in your screenshots)
        st.markdown(f"""
            <div style="background: rgba(10, 14, 39, 0.9); padding: 20px; border-radius: 12px; 
                        border: 2px solid rgba(99, 102, 241, 0.5); margin-top: 20px;">
                <h2 style="color: #6366f1; margin: 0 0 20px 0;">{st.session_state.spacetag or 'Player'}</h2>
                <p style="font-size: 1.5rem; margin: 10px 0;"><strong>Score:</strong> <span style="color: #22C55E;">{st.session_state.score}</span></p>
                <p style="font-size: 1.5rem; margin: 10px 0;"><strong>Level:</strong> {st.session_state.level}</p>
                <p style="font-size: 1.5rem; margin: 10px 0; color: #EF4444;"><strong>Time:</strong> <span id="timeDisplay">30s</span></p>
                <p style="font-size: 1.5rem; margin: 10px 0;"><strong>Rocks:</strong> <span id="rocksDisplay">{num_rocks}</span></p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("⏸️ PAUSE GAME", use_container_width=True):
            st.session_state.game_state = 'level_start'
            st.rerun()
    
    # Check query parameters for game state updates
    try:
        import streamlit as st
        query_params = st.query_params
        if 'game_result' in query_params:
            result = query_params['game_result']
            if result == 'complete':
                st.session_state.level += 1
                st.session_state.game_state = 'level_complete'
                st.query_params.clear()
                st.rerun()
            elif result == 'failed':
                st.session_state.game_state = 'level_failed'
                st.query_params.clear()
                st.rerun()
    except:
        pass

# ==================== LEVEL COMPLETE SCREEN ====================
elif st.session_state.game_state == 'level_complete':
    bg_bytes = load_background(st.session_state.level - 1)
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
            <div style="background: rgba(10, 14, 39, 0.9); padding: 40px; border-radius: 12px; 
                        text-align: center; backdrop-filter: blur(12px); border: 2px solid rgba(34, 197, 94, 0.5);">
        """, unsafe_allow_html=True)
        
        logo_bytes = load_logo()
        if logo_bytes:
            st.markdown(f"""
                <img src="data:image/png;base64,{logo_bytes}" 
                     style="max-width: 400px; width: 70%; animation: pulse 2s ease-in-out infinite;">
            """, unsafe_allow_html=True)
        
        st.markdown(f"<h1 style='color: #22c55e; margin: 20px 0;'>★ Level {st.session_state.level - 1} Complete!</h1>", 
                    unsafe_allow_html=True)
        st.markdown(f"<p style='color: #f8fafc; font-size: 20px;'><strong>Score:</strong> {st.session_state.score}</p>", 
                    unsafe_allow_html=True)
        
        st.success("▶ Preparing next sector...")
        st.markdown("</div>", unsafe_allow_html=True)
    
    import time
    time.sleep(2)
    st.session_state.game_state = 'level_start'
    st.rerun()

# ==================== LEVEL FAILED SCREEN ====================
elif st.session_state.game_state == 'level_failed':
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
        st.markdown(f"""
            <div style="background: rgba(10, 14, 39, 0.9); padding: 40px; border-radius: 20px; 
                        text-align: center; backdrop-filter: blur(10px); border: 2px solid rgba(239, 68, 68, 0.5);">
                <h1 style="font-size: 3rem; color: #ef4444;">TIME'S UP!</h1>
                <h2 style="color: #cbd5e1;">Final Score: {st.session_state.score}</h2>
                <h3 style="color: #cbd5e1;">Levels Completed: {st.session_state.level - 1}</h3>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 RETRY LEVEL", type="primary", use_container_width=True):
                st.session_state.game_state = 'level_start'
                st.rerun()
        with col_b:
            if st.button("🏠 MAIN MENU", use_container_width=True):
                st.session_state.score = 0
                st.session_state.level = 1
                st.session_state.game_state = 'title'
                st.rerun()
