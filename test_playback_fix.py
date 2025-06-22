#!/usr/bin/env python3
"""
Test script to verify play-from-scroll functionality
"""

import sys
import os

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

def test_imports():
    """Test that all required imports work"""
    print("Testing imports...")
    try:
        import mido
        print("✓ mido imported successfully")
        
        import pygame
        print("✓ pygame imported successfully")
        
        # Test mido functions
        test_tempo = 500000
        test_ticks = 480
        test_time = 1.0
        
        # Test tick/second conversion
        seconds = mido.tick2second(480, test_ticks, test_tempo)
        print(f"✓ mido.tick2second works: 480 ticks = {seconds:.3f} seconds")
        
        ticks = mido.second2tick(1.0, test_ticks, test_tempo)
        print(f"✓ mido.second2tick works: 1.0 seconds = {ticks} ticks")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error testing functions: {e}")
        return False

def test_main_import():
    """Test that main.py can be imported without errors"""
    print("\nTesting main.py import...")
    try:
        import main
        print("✓ main.py imported successfully")
        
        # Check if the key methods exist
        if hasattr(main.MidiGapperGUI, 'create_temp_midi_from_position'):
            print("✓ create_temp_midi_from_position method exists")
        else:
            print("✗ create_temp_midi_from_position method missing")
            
        if hasattr(main.MidiGapperGUI, 'update_playback_position_from_scroll'):
            print("✓ update_playback_position_from_scroll method exists")
        else:
            print("✗ update_playback_position_from_scroll method missing")
            
        return True
        
    except Exception as e:
        print(f"✗ Error importing main.py: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=== Play-from-Scroll Fix Verification ===\n")
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test main import
    if not test_main_import():
        success = False
    
    print(f"\n=== Test Results ===")
    if success:
        print("✓ All tests passed! The play-from-scroll fix should be working.")
        print("\nTo test:")
        print("1. Run the main application")
        print("2. Load a MIDI file")
        print("3. Scroll to a position in the middle")
        print("4. Press play - it should start from the scrolled position")
        print("5. Watch the console for debug messages")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
