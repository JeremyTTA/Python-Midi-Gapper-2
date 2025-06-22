#!/usr/bin/env python3
"""
Test script for the new FluidSynth-based MIDI playback with seeking support
"""

import sys
import os
import subprocess

def test_fluidsynth_seeking():
    """Test the FluidSynth seeking functionality"""
    
    print("=== FLUIDSYNTH SEEKING TEST ===")
    print()
    print("This test will verify that the MIDI Gapper now supports proper seeking")
    print("using FluidSynth instead of temporary file workarounds.")
    print()
    
    print("WHAT TO TEST:")
    print("1. Launch the app")
    print("2. Load a MIDI file (use one of the test files)")
    print("3. Scroll to different positions (30s, 60s, etc.)")
    print("4. Press play - audio should start from the scrolled position")
    print("5. No more 'temp file creation' messages")
    print("6. Immediate playback from the correct position")
    print()
    
    print("EXPECTED BEHAVIOR:")
    print("✓ FluidSynth initialization message on startup")
    print("✓ 'Using FluidSynth for playback with seeking support' when playing")
    print("✓ No temporary MIDI file creation")
    print("✓ Immediate audio playback from the scrolled position")
    print("✓ No audio delay or offset")
    print()
    
    print("FALLBACK BEHAVIOR (if FluidSynth fails):")
    print("⚠ 'Using pygame fallback (no seeking)' message")
    print("⚠ Falls back to the old temp file approach")
    print()
    
    # Check if required packages are installed
    print("=== CHECKING DEPENDENCIES ===")
    
    try:
        import fluidsynth
        print("✓ pyfluidsynth is installed")
    except ImportError:
        print("✗ pyfluidsynth not installed")
        print("  Run: pip install pyfluidsynth")
        return
    
    try:
        import mido
        print("✓ mido is available")
    except ImportError:
        print("✗ mido not available")
        print("  Run: pip install mido")
        return
    
    try:
        import pygame
        print("✓ pygame is available")
    except ImportError:
        print("✗ pygame not available")
        return
    
    print("✓ All dependencies available")
    print()
    
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Use the correct Python path
    python_path = "C:/Users/JeremyStandlee/AppData/Local/Programs/Python/Python313/python.exe"
    
    try:
        print("=== LAUNCHING MIDI GAPPER WITH FLUIDSYNTH SUPPORT ===")
        print("Watch for FluidSynth initialization messages...")
        print("Test seeking by scrolling and pressing play!")
        print()
        
        # Run the main app
        result = subprocess.run([python_path, "main.py"], 
                              capture_output=False, 
                              text=True)
        
        print(f"App closed with exit code: {result.returncode}")
        
    except Exception as e:
        print(f"Error launching app: {e}")

def show_comparison():
    """Show the difference between old and new approaches"""
    print()
    print("=== OLD vs NEW APPROACH ===")
    print()
    print("OLD APPROACH (temporary files):")
    print("1. User scrolls to 60 seconds")
    print("2. User presses play")
    print("3. App uses mido to scan through MIDI file")
    print("4. App creates temporary MIDI file starting at 60s")
    print("5. pygame loads and plays temp file from beginning")
    print("6. Complex timing calculations for visual sync")
    print("❌ Temp files often had issues (empty, malformed)")
    print("❌ Complex and error-prone")
    print("❌ Still no real seeking")
    print()
    print("NEW APPROACH (FluidSynth):")
    print("1. User scrolls to 60 seconds")
    print("2. User presses play")
    print("3. App loads MIDI file into FluidSynth")
    print("4. App seeks directly to 60 seconds")
    print("5. FluidSynth starts playing from 60 seconds")
    print("6. No temp files needed")
    print("✓ Real seeking support")
    print("✓ Simpler and more reliable")
    print("✓ Better audio quality")
    print("✓ No complex workarounds")

if __name__ == "__main__":
    test_fluidsynth_seeking()
    show_comparison()
