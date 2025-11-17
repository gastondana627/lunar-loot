"""
Enhanced Features Module for Moonrock Collector
Includes: Spacetag, Colored Moonrocks, Enhanced Scoring, Space Selfie, Leaderboard
"""

import json
import os
from datetime import datetime

# Color schemes for moonrocks based on background
MOONROCK_COLORS = {
    "Earth": (100, 255, 255),      # Bright cyan (contrasts with blue/green)
    "Halleys Comet": (255, 100, 255),  # Bright magenta
    "Mars": (100, 255, 100),       # Bright green (contrasts with red)
    "Mercury": (255, 200, 100),    # Bright orange
    "Moon": (255, 100, 100),       # Bright red
    "Oumuamua": (100, 255, 255),   # Cyan
    "Planet X": (255, 255, 100),   # Bright yellow
    "Saturn": (255, 100, 255),     # Magenta
    "SpaceShip": (100, 255, 100),  # Green
    "Uranus": (255, 200, 100),     # Orange
    "Venus": (100, 100, 255),      # Bright blue
    "3I/ATLAS": (255, 255, 100),   # Bright yellow (contrasts with comet)
    "Ceres": (255, 100, 255),      # Magenta (contrasts with gray)
    "Makemake": (100, 255, 255),   # Cyan (contrasts with reddish surface)
}

def get_moonrock_color(background_name):
    """Get contrasting color for moonrocks based on background"""
    for key in MOONROCK_COLORS:
        if key.lower() in background_name.lower():
            return MOONROCK_COLORS[key]
    return (255, 100, 255)  # Default magenta

def calculate_bonus_score(time_remaining, combo_count):
    """Calculate bonus points based on speed and combo"""
    time_bonus = int(time_remaining * 2)  # 2 points per second remaining
    combo_bonus = combo_count * 10  # 10 points per combo
    return time_bonus + combo_bonus

def save_high_score(spacetag, score, level):
    """Save high score to local JSON file"""
    scores_file = "high_scores.json"
    
    # Load existing scores
    if os.path.exists(scores_file):
        with open(scores_file, 'r') as f:
            scores = json.load(f)
    else:
        scores = []
    
    # Add new score
    scores.append({
        "spacetag": spacetag,
        "score": score,
        "level": level,
        "timestamp": datetime.now().isoformat()
    })
    
    # Sort by score (descending) and keep top 10
    scores = sorted(scores, key=lambda x: x['score'], reverse=True)[:10]
    
    # Save back to file
    with open(scores_file, 'w') as f:
        json.dump(scores, f, indent=2)
    
    return scores

def load_high_scores():
    """Load high scores from file"""
    scores_file = "high_scores.json"
    if os.path.exists(scores_file):
        with open(scores_file, 'r') as f:
            return json.load(f)
    return []

def create_space_selfie(frame, score, level, spacetag):
    """Create a space selfie with overlay graphics"""
    import cv2
    import numpy as np
    
    # Create a copy of the frame
    selfie = frame.copy()
    
    # Add semi-transparent overlay at bottom
    overlay = selfie.copy()
    cv2.rectangle(overlay, (0, selfie.shape[0]-120), (selfie.shape[1], selfie.shape[0]), 
                  (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.7, selfie, 0.3, 0, selfie)
    
    # Add text
    font = cv2.FONT_HERSHEY_BOLD
    cv2.putText(selfie, f"🌙 {spacetag}", (20, selfie.shape[0]-80),
                font, 1.2, (255, 255, 255), 3, cv2.LINE_AA)
    cv2.putText(selfie, f"Score: {score} | Level: {level}", (20, selfie.shape[0]-40),
                font, 0.8, (100, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(selfie, "#MoonrockCollector #ChromaAwards", (20, selfie.shape[0]-10),
                font, 0.6, (200, 200, 200), 1, cv2.LINE_AA)
    
    return selfie
