#!/usr/bin/env python3
"""
Deployment verification script for Lunar Loot
Checks that all required components are working correctly
"""

import sys
import os

def check_main_app():
    """Verify the main application file exists and is valid"""
    if not os.path.exists('catching_moonrocks.py'):
        print("❌ Main application file 'catching_moonrocks.py' not found")
        return False
    
    # Try to parse the file for basic syntax
    try:
        with open('catching_moonrocks.py', 'r') as f:
            content = f.read()
            compile(content, 'catching_moonrocks.py', 'exec')
        print("✅ Main application file syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in main application: {e}")
        return False

def check_assets():
    """Check that required asset directories exist"""
    required_dirs = [
        'backgrounds',
        'ui_assets',
    ]
    
    optional_files = [
        'moonrock.png',
    ]
    
    all_good = True
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ Directory '{dir_name}' found")
        else:
            print(f"⚠️  Directory '{dir_name}' not found (may cause visual issues)")
    
    for file_name in optional_files:
        if os.path.exists(file_name):
            print(f"✅ File '{file_name}' found")
        else:
            print(f"⚠️  File '{file_name}' not found (may use fallback)")
    
    return True

def check_requirements():
    """Verify requirements.txt doesn't contain problematic packages"""
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found")
        return False
    
    with open('requirements.txt', 'r') as f:
        content = f.read()
    
    # Check for problematic packages
    problematic = ['av==', 'streamlit-webrtc']
    found_issues = []
    
    for package in problematic:
        if package in content:
            found_issues.append(package)
    
    if found_issues:
        print(f"❌ Found problematic packages: {found_issues}")
        print("   These packages cause build failures on Streamlit Cloud")
        return False
    else:
        print("✅ requirements.txt looks clean")
        return True

def check_packages_txt():
    """Verify packages.txt doesn't contain FFmpeg libraries"""
    if not os.path.exists('packages.txt'):
        print("✅ No packages.txt file (good - no system dependencies)")
        return True
    
    with open('packages.txt', 'r') as f:
        content = f.read()
    
    # Check for FFmpeg libraries
    ffmpeg_libs = ['libav', 'ffmpeg']
    found_ffmpeg = []
    
    for lib in ffmpeg_libs:
        if lib in content.lower():
            found_ffmpeg.append(lib)
    
    if found_ffmpeg:
        print(f"⚠️  Found FFmpeg libraries in packages.txt: {found_ffmpeg}")
        print("   These may cause build issues if av package is not needed")
    else:
        print("✅ packages.txt is clean of FFmpeg dependencies")
    
    return True

def main():
    """Run all verification checks"""
    print("🚀 Lunar Loot Deployment Verification")
    print("=" * 50)
    
    checks = [
        ("Main Application", check_main_app),
        ("Requirements", check_requirements), 
        ("System Packages", check_packages_txt),
        ("Assets", check_assets),
    ]
    
    all_passed = True
    
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All checks passed! Deployment should succeed.")
        print("\n🎮 The app uses JavaScript MediaPipe for hand tracking")
        print("   - No Python WebRTC dependencies needed")
        print("   - Runs entirely in the browser")
        print("   - No server-side video processing")
    else:
        print("⚠️  Some issues found. Please review and fix before deploying.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)