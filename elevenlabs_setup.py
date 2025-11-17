"""
ElevenLabs Sound Generation Script
Run this locally to generate all sound files for the game
"""

import os
from elevenlabs import generate, save, set_api_key

# Set your API key (or use environment variable)
API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
if API_KEY:
    set_api_key(API_KEY)
else:
    print("⚠️  No API key found. Set ELEVENLABS_API_KEY environment variable")
    print("   Or edit this file and add your key directly")
    exit(1)

# Create sounds directory
os.makedirs("sounds", exist_ok=True)

# Sound effects to generate - ALL 20 SOUNDS
sounds = {
    # Level announcements (11 total - one per background)
    "level_01_earth": "Level one! Welcome to Earth orbit. Let's collect some moonrocks!",
    "level_02_halley": "Level two! Halley's Comet approaches. Watch out for the cosmic debris!",
    "level_03_mars": "Level three! The red planet Mars. Time to explore the rusty surface!",
    "level_04_mercury": "Level four! Mercury's scorching surface. Stay cool and collect those rocks!",
    "level_05_moon": "Level five! Our Moon! One small step for you, one giant leap for your score!",
    "level_06_oumuamua": "Level six! The mysterious Oumuamua. An interstellar visitor from beyond!",
    "level_07_planetx": "Level seven! The legendary Planet X. Venture into the unknown!",
    "level_08_saturn": "Level eight! Saturn and its beautiful rings. Navigate the cosmic jewelry!",
    "level_09_spaceship": "Level nine! Aboard the spaceship. Collect moonrocks in zero gravity!",
    "level_10_uranus": "Level ten! Uranus, the sideways planet. Almost there, keep going!",
    "level_11_venus": "Level eleven! Venus, the morning star. Final level, give it your all!",
    "level_12_atlas": "Level twelve! Comet 3I/ATLAS, an interstellar wanderer. Chase the cosmic visitor!",
    "level_13_ceres": "Level thirteen! Ceres, queen of the asteroid belt. Navigate the rocky realm!",
    "level_14_makemake": "Level fourteen! Makemake, the distant dwarf planet. Journey to the edge of our solar system!",
    
    # Game events (9 total)
    "welcome": "Welcome to Moonrock Collector! Use your hand to collect the moonrocks. Good luck!",
    "collect_1": "Collected!",
    "collect_2": "Nice catch!",
    "collect_3": "Got it!",
    "level_complete": "Level complete! Excellent work! Get ready for the next challenge!",
    "time_warning_10": "Ten seconds remaining! Hurry!",
    "time_warning_5": "Five seconds left!",
    "game_over": "Game over! Thanks for playing Moonrock Collector!",
    "high_score": "New high score! You're a moonrock master!",
}

print("🎙️  Generating sound effects with ElevenLabs...")
print("=" * 50)

for name, text in sounds.items():
    print(f"\n📢 Generating: {name}")
    print(f"   Text: {text}")
    
    try:
        # Generate audio
        audio = generate(
            text=text,
            voice="Rachel",  # You can change this to other voices
            model="eleven_monolingual_v1"
        )
        
        # Save to file
        filename = f"sounds/{name}.mp3"
        save(audio, filename)
        print(f"   ✅ Saved to: {filename}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 50)
print("✅ Sound generation complete!")
print("\nGenerated files:")
for name in sounds.keys():
    print(f"   - sounds/{name}.mp3")

print("\n💡 Next steps:")
print("   1. Test the sounds by playing them")
print("   2. Adjust voice or text if needed")
print("   3. Integrate into catching_moonrocks.py")
print("   4. Deploy to Streamlit Cloud")
