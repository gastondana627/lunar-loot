"""
Simple audio test to verify sound files work
"""
import streamlit as st
import base64
import os

st.title("🔊 Audio Test - Lunar Loot")

st.write("Click the buttons below to test each sound effect:")

sounds_dir = "sounds"
sound_files = [
    "collect.wav",
    "level_complete.wav", 
    "level_failed.wav",
    "Beep.wav",
]

for sound_file in sound_files:
    sound_path = os.path.join(sounds_dir, sound_file)
    if os.path.exists(sound_path):
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button(f"Play", key=sound_file):
                with open(sound_path, 'rb') as audio_file:
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format='audio/wav')
        with col2:
            st.write(f"**{sound_file}**")
    else:
        st.error(f"❌ {sound_file} not found")

st.write("---")
st.write("### Menu Theme Test")
menu_path = os.path.join(sounds_dir, "menu_theme.wav")
if os.path.exists(menu_path):
    file_size = os.path.getsize(menu_path) / (1024 * 1024)
    st.write(f"File size: {file_size:.2f} MB")
    
    if st.button("Play Menu Theme"):
        with open(menu_path, 'rb') as audio_file:
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/wav')
else:
    st.error("❌ menu_theme.wav not found")

st.write("---")
st.info("If sounds play here but not in the game, the issue is with the HTML audio implementation in the main game.")
