## Lunar Loot - JavaScript MediaPipe Version
## Created for Chroma Awards 2025
## Tools: Google MediaPipe, Freepik, Adobe
## BREAKTHROUGH: Client-side hand tracking - NO SERVER CONNECTION NEEDED!

import streamlit as st
import streamlit.components.v1 as components
import os
import base64
import time
import random
import json

# Page configuration
st.set_page_config(
    page_title="Lunar Loot - AI Game",
    page_icon="🌑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Game constants
LEVEL_TIME_LIMIT = 30
NUM_MOONROCKS = 5
GAME_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Sector names
SECTOR_NAMES = {
    1: "Mercury", 2: "Mars", 3: "Venus", 4: "Moon", 5: "Saturn",
    6: "Jupiter", 7: "Neptune", 8: "Uranus", 9: "Pluto", 10: "Asteroid Belt",
    11: "Comet", 12: "Nebula", 13: "Black Hole", 14: "Spaceship"
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

def convert_image_to_bytes(image_path):
    try:
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except:
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

# Title Screen
if st.session_state.game_state == 'title':
    col1, col2 = st.columns([1, 1])
    with col1:
        logo_bytes = load_logo()
        if logo_bytes:
            st.markdown(f"""
                <div style="background: rgba(10, 14, 39, 0.85); padding: 30px; border-radius: 12px; 
                            border: 1px solid rgba(99, 102, 241, 0.3); margin-bottom: 20px; text-align: center;">
                    <img src="data:image/png;base64,{logo_bytes}" 
                         style="max-width: 100%; width: 400px; margin-bottom: 15px;">
                    <p style="font-size: 1.25rem; color: #cbd5e1; margin: 10px 0 0 0;">
                        Collect cosmic moonrocks before time runs out
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        spacetag = st.text_input("Enter your Spacetag", value=st.session_state.spacetag, placeholder="AstroHunter42")
        if spacetag:
            st.session_state.spacetag = spacetag
        
        st.success("🚀 **BREAKTHROUGH VERSION:** Uses JavaScript MediaPipe - runs entirely in YOUR browser!")
        
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
        
        if st.button("🚀 START GAME", type="primary", use_container_width=True):
            st.session_state.game_state = 'playing'
            st.rerun()

# Playing State - JavaScript MediaPipe
elif st.session_state.game_state == 'playing':
    st.markdown(f"""
        <h1 style='text-align: center; color: #6366f1;'>
            LEVEL {st.session_state.level} | SCORE: {st.session_state.score}
        </h1>
    """, unsafe_allow_html=True)
    
    st.info("📹 **Client-Side Processing:** Hand tracking runs in your browser - NO server connection needed!")
    
    # JavaScript MediaPipe Hand Tracking Game
    components.html("""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js"></script>
        </head>
        <body style="margin:0; padding:0; background:#0a0e27;">
            <div style="position: relative; width: 100%; height: 600px;">
                <video id="video" style="display:none;"></video>
                <canvas id="canvas" width="640" height="480" style="width:100%; height:100%; border-radius:8px;"></canvas>
            </div>
            
            <script>
                const video = document.getElementById('video');
                const canvas = document.getElementById('canvas');
                const ctx = canvas.getContext('2d');
                
                // Game state
                let score = 0;
                let moonrocks = [];
                let startTime = Date.now();
                const LEVEL_TIME = 30;
                const NUM_ROCKS = 6;
                
                // Initialize moonrocks
                for (let i = 0; i < NUM_ROCKS; i++) {
                    moonrocks.push({
                        x: Math.random() * 580 + 30,
                        y: Math.random() * 420 + 30,
                        collected: false
                    });
                }
                
                // MediaPipe Hands
                const hands = new Hands({
                    locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
                });
                
                hands.setOptions({
                    maxNumHands: 1,
                    modelComplexity: 1,
                    minDetectionConfidence: 0.5,
                    minTrackingConfidence: 0.5
                });
                
                hands.onResults((results) => {
                    // Clear canvas
                    ctx.fillStyle = '#0a0e27';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    
                    // Draw video
                    ctx.drawImage(results.image, 0, 0, canvas.width, canvas.height);
                    
                    // Draw moonrocks
                    moonrocks.forEach(rock => {
                        if (!rock.collected) {
                            ctx.fillStyle = '#FFB6C1';
                            ctx.beginPath();
                            ctx.arc(rock.x, rock.y, 30, 0, Math.PI * 2);
                            ctx.fill();
                            ctx.strokeStyle = '#FF69B4';
                            ctx.lineWidth = 3;
                            ctx.stroke();
                        }
                    });
                    
                    // Process hand landmarks
                    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
                        const landmarks = results.multiHandLandmarks[0];
                        
                        // Draw hand skeleton
                        ctx.strokeStyle = '#00FF00';
                        ctx.lineWidth = 2;
                        const connections = [
                            [0,1],[1,2],[2,3],[3,4],
                            [0,5],[5,6],[6,7],[7,8],
                            [0,9],[9,10],[10,11],[11,12],
                            [0,13],[13,14],[14,15],[15,16],
                            [0,17],[17,18],[18,19],[19,20],
                            [5,9],[9,13],[13,17]
                        ];
                        
                        connections.forEach(([start, end]) => {
                            ctx.beginPath();
                            ctx.moveTo(landmarks[start].x * canvas.width, landmarks[start].y * canvas.height);
                            ctx.lineTo(landmarks[end].x * canvas.width, landmarks[end].y * canvas.height);
                            ctx.stroke();
                        });
                        
                        // Get index finger tip
                        const indexTip = landmarks[8];
                        const fingerX = indexTip.x * canvas.width;
                        const fingerY = indexTip.y * canvas.height;
                        
                        // Draw finger indicator
                        ctx.fillStyle = '#22C55E';
                        ctx.beginPath();
                        ctx.arc(fingerX, fingerY, 20, 0, Math.PI * 2);
                        ctx.fill();
                        ctx.strokeStyle = '#FFFFFF';
                        ctx.lineWidth = 2;
                        ctx.stroke();
                        
                        // Check collisions
                        moonrocks.forEach(rock => {
                            if (!rock.collected) {
                                const dist = Math.sqrt((fingerX - rock.x)**2 + (fingerY - rock.y)**2);
                                if (dist < 50) {
                                    rock.collected = true;
                                    score += 10;
                                }
                            }
                        });
                    }
                    
                    // Draw UI
                    ctx.fillStyle = '#FFFFFF';
                    ctx.font = '24px Orbitron';
                    ctx.fillText(`Score: ${score}`, 10, 30);
                    
                    const elapsed = (Date.now() - startTime) / 1000;
                    const remaining = Math.max(0, LEVEL_TIME - elapsed);
                    ctx.fillText(`Time: ${Math.floor(remaining)}s`, 10, 60);
                    
                    const rocksLeft = moonrocks.filter(r => !r.collected).length;
                    ctx.fillText(`Rocks: ${rocksLeft}`, 10, 90);
                    
                    // Check win condition
                    if (rocksLeft === 0) {
                        ctx.fillStyle = '#22C55E';
                        ctx.font = '48px Orbitron';
                        ctx.fillText('LEVEL COMPLETE!', canvas.width/2 - 200, canvas.height/2);
                    } else if (remaining <= 0) {
                        ctx.fillStyle = '#EF4444';
                        ctx.font = '48px Orbitron';
                        ctx.fillText('TIME UP!', canvas.width/2 - 100, canvas.height/2);
                    }
                });
                
                // Start camera
                const camera = new Camera(video, {
                    onFrame: async () => {
                        await hands.send({image: video});
                    },
                    width: 640,
                    height: 480
                });
                
                camera.start();
            </script>
        </body>
        </html>
    """, height=650)
    
    if st.button("⏸️ BACK TO MENU", use_container_width=True):
        st.session_state.game_state = 'title'
        st.rerun()
