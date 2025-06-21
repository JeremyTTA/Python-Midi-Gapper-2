#!/usr/bin/env python3
"""
Test script for MIDI playback functionality
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_pygame_availability():
    """Test if pygame is available and can be used for MIDI playback"""
    try:
        import pygame
        print("✓ pygame is available")
        
        # Test mixer initialization
        try:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
            pygame.mixer.init()
            print("✓ pygame mixer initialized successfully")
            return True
        except Exception as e:
            print(f"✗ pygame mixer initialization failed: {e}")
            return False
    except ImportError:
        print("✗ pygame is not installed")
        print("Install with: pip install pygame")
        return False

def test_midi_file_support():
    """Test if we can load a MIDI file"""
    # Check for any MIDI files in the directory
    midi_files = [f for f in os.listdir('.') if f.endswith(('.mid', '.midi'))]
    
    if not midi_files:
        print("No MIDI files found in current directory")
        print("The application will need a MIDI file to test playback")
        return False
    
    print(f"Found MIDI files: {midi_files}")
    
    # Try to load a MIDI file with pygame
    try:
        import pygame
        pygame.mixer.init()
        test_file = midi_files[0]
        pygame.mixer.music.load(test_file)
        print(f"✓ Successfully loaded {test_file}")
        return True
    except Exception as e:
        print(f"✗ Error loading MIDI file: {e}")
        return False

def test_main_app_syntax():
    """Test if the main app can be imported without syntax errors"""
    try:
        import main
        print("✓ main.py imports successfully")
        return True
    except SyntaxError as e:
        print(f"✗ Syntax error in main.py: {e}")
        return False
    except ImportError as e:
        print(f"⚠ Import error in main.py (expected): {e}")
        return True  # Import errors are expected if pygame isn't installed
    except Exception as e:
        print(f"✗ Unexpected error in main.py: {e}")
        return False

if __name__ == "__main__":
    print("Testing MIDI Playback Functionality")
    print("=" * 40)
    
    pygame_ok = test_pygame_availability()
    print()
    
    if pygame_ok:
        midi_ok = test_midi_file_support()
        print()
    else:
        midi_ok = False
    
    syntax_ok = test_main_app_syntax()
    print()
    
    print("Summary:")
    print("=" * 40)
    print(f"Pygame available: {'✓' if pygame_ok else '✗'}")
    print(f"MIDI files loadable: {'✓' if midi_ok else '✗'}")
    print(f"Main app syntax: {'✓' if syntax_ok else '✗'}")
    
    if pygame_ok and syntax_ok:
        print("\n✓ MIDI playback should work!")
    elif syntax_ok:
        print("\n⚠ Install pygame to enable MIDI playback")
    else:
        print("\n✗ Fix syntax errors first")
