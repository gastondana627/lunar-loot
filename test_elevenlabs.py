"""Quick test to see if ElevenLabs API is working"""
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

API_KEY = os.getenv("ELEVENLABS_API_KEY")
print(f"API Key found: {API_KEY[:20]}...")

try:
    # Initialize client
    client = ElevenLabs(api_key=API_KEY)
    print("✅ Client initialized")
    
    # Generate one test sound
    print("🎙️  Generating test sound...")
    audio = client.generate(
        text="Test! This is a test sound from Lunar Loot.",
        voice="Sarah",  # Using Sarah voice (available in your account)
        model="eleven_monolingual_v1"
    )
    print("✅ Audio generated")
    
    # Save to file
    os.makedirs("sounds", exist_ok=True)
    save(audio, "sounds/test.mp3")
    print("✅ Saved to sounds/test.mp3")
    
    # Check file exists
    if os.path.exists("sounds/test.mp3"):
        size = os.path.getsize("sounds/test.mp3")
        print(f"✅ File created successfully! Size: {size} bytes")
    else:
        print("❌ File not found after save")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
