"""Audio manager using ElevenLabs for sound effects"""
import os
import base64
from elevenlabs import generate, save, Voice, VoiceSettings

class AudioManager:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY", "")
        self.sounds_cache = {}
        
    def generate_sound_effect(self, text, filename):
        """Generate a sound effect using ElevenLabs text-to-speech"""
        if not self.api_key:
            return None
            
        try:
            audio = generate(
                text=text,
                voice=Voice(
                    voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel voice
                    settings=VoiceSettings(
                        stability=0.5,
                        similarity_boost=0.75
                    )
                ),
                model="eleven_monolingual_v1"
            )
            
            # Save to file
            save(audio, filename)
            
            # Convert to base64 for embedding
            with open(filename, "rb") as f:
                audio_bytes = base64.b64encode(f.read()).decode()
            
            self.sounds_cache[filename] = audio_bytes
            return audio_bytes
            
        except Exception as e:
            print(f"Error generating sound: {e}")
            return None
    
    def get_sound_html(self, sound_key):
        """Get HTML audio tag for playing sound"""
        if sound_key not in self.sounds_cache:
            return ""
        
        return f'''
        <audio autoplay>
            <source src="data:audio/mp3;base64,{self.sounds_cache[sound_key]}" type="audio/mp3">
        </audio>
        '''
