#!/bin/bash

# Setup script for local development on macOS

echo "🚀 Setting up Moonrock Collector..."

# Set environment variable for macOS camera access
export OPENCV_AVFOUNDATION_SKIP_AUTH=1

echo "✅ Environment configured"
echo ""
echo "📸 Note: You'll need to grant camera permissions when prompted"
echo ""
echo "🎮 Starting game..."
echo ""

streamlit run catching_moonrocks.py
