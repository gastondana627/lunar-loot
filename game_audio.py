"""
Game Audio Manager - Handles all sound effects
Works with both local files and ElevenLabs-generated audio
"""

import os
import base64
import streamlit as st

class GameAudio:
    def __init__(self, sounds_dir="sounds"):
        self.sounds_dir = sounds_dir
        self.sounds_cache = {}
        self.load_sounds()
    
    def load_sounds(self):
        """Load all sound files into cache"""
        if not os.path.exists(self.sounds_dir):
            print(f"⚠️  Sounds directory '{self.sounds_dir}' not found")
            return
        
        for filename in os.listdir(self.sounds_dir):
            if filename.endswith('.mp3'):
                sound_name = filename.replace('.mp3', '')
                filepath = os.path.join(self.sounds_dir, filename)
                
                try:
                    with open(filepath, 'rb') as f:
                        audio_bytes = base64.b64encode(f.read()).decode()
                        self.sounds_cache[sound_name] = audio_bytes
                        print(f"✅ Loaded: {sound_name}")
                except Exception as e:
                    print(f"❌ Error loading {filename}: {e}")
    
    def play(self, sound_name, autoplay=True):
        """Play a sound effect"""
        if sound_name not in self.sounds_cache:
            print(f"⚠️  Sound '{sound_name}' not found in cache")
            return ""
        
        audio_html = f'''
        <audio {"autoplay" if autoplay else ""}>
            <source src="data:audio/mp3;base64,{self.sounds_cache[sound_name]}" type="audio/mp3">
        </audio>
        '''
        
        return audio_html
    
    def play_in_streamlit(self, sound_name):
        """Play sound directly in Streamlit"""
        audio_html = self.play(sound_name)
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)
    
    def get_available_sounds(self):
        """Get list of available sounds"""
        return list(self.sounds_cache.keys())


# Fallback: Free sound effects from CDN
FALLBACK_SOUNDS = {
    "collect": "https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3",
    "level_complete": "https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3",
    "game_over": "https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3",
    "countdown": "https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3",
}

def play_fallback_sound(sound_name):
    """Play fallback sound from CDN"""
    if sound_name in FALLBACK_SOUNDS:
        return f'<audio autoplay><source src="{FALLBACK_SOUNDS[sound_name]}" type="audio/mpeg"></audio>'
    return ""
