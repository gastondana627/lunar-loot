#!/usr/bin/env python3
"""
Test script to verify all required imports work correctly
"""

def test_main_app_imports():
    """Test that the main application can import all its dependencies"""
    try:
        import streamlit as st
        import streamlit.components.v1 as components
        import os
        import base64
        print("✅ All main application imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_optional_imports():
    """Test optional imports that might be used"""
    optional_packages = [
        'mediapipe',
        'numpy', 
        'opencv-python',
        'pillow'
    ]
    
    for package in optional_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} available")
        except ImportError:
            print(f"⚠️  {package} not available (optional)")

if __name__ == "__main__":
    print("Testing Lunar Loot dependencies...")
    print("=" * 50)
    
    success = test_main_app_imports()
    print()
    test_optional_imports()
    
    print("=" * 50)
    if success:
        print("🚀 Application should deploy successfully!")
    else:
        print("❌ Deployment may fail due to missing dependencies")