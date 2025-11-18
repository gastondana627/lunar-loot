"""List available ElevenLabs voices"""
import os
from elevenlabs.client import ElevenLabs

API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=API_KEY)

print("Available voices:")
try:
    voices = client.voices.get_all()
    for voice in voices.voices:
        print(f"  - {voice.name} (ID: {voice.voice_id})")
except Exception as e:
    print(f"Error: {e}")
