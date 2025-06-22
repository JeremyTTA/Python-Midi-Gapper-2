#!/usr/bin/env python3
"""
Simple test to run the app and see what debug output we get
"""

import os
import sys

# Add the project directory to path so we can import main
project_dir = r"g:\My Drive\Programming Projects\Player Piano\Jeremys Code\Python Midi Gapper 2"
sys.path.insert(0, project_dir)

def test_basic_import():
    """Test basic imports and method existence"""
    print("Testing basic imports...")
    
    try:
        from main import MidiGapperGUI
        print("✓ Main module imported successfully")
        
        # Check if key methods exist
        methods_to_check = [
            'create_temp_midi_from_position',
            'update_playback_position_from_scroll', 
            'start_midi_playback',
            'toggle_play_pause'
        ]
        
        for method in methods_to_check:
            if hasattr(MidiGapperGUI, method):
                print(f"✓ Method {method} exists")
            else:
                print(f"✗ Method {method} missing")
        
        return True
        
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_mido():
    """Test mido library"""
    print("\nTesting mido library...")
    
    try:
        import mido
        print("✓ mido imported successfully")
        
        # Look for MIDI files to test with
        midi_files = []
        for file in os.listdir(project_dir):
            if file.lower().endswith(('.mid', '.midi')):
                midi_files.append(file)
        
        print(f"✓ Found {len(midi_files)} MIDI files: {midi_files}")
        
        if midi_files:
            test_file = os.path.join(project_dir, midi_files[0])
            mid = mido.MidiFile(test_file)
            print(f"✓ Successfully loaded {midi_files[0]}")
            print(f"  - Type: {mid.type}")
            print(f"  - Ticks per beat: {mid.ticks_per_beat}")
            print(f"  - Tracks: {len(mid.tracks)}")
        
        return True
        
    except ImportError:
        print("✗ mido not available")
        return False
    except Exception as e:
        print(f"✗ mido test failed: {e}")
        return False

if __name__ == "__main__":
    print("BASIC APP TEST")
    print("=" * 40)
    
    import_ok = test_basic_import()
    mido_ok = test_mido()
    
    print("\n" + "=" * 40)
    if import_ok and mido_ok:
        print("✓ Basic tests passed - app should work")
    else:
        print("✗ Some tests failed - check the output above")
    
    print("\nTo manually test the position fix:")
    print("1. Run the main app: python main.py")
    print("2. Load a MIDI file")
    print("3. Scroll to a position in the middle")
    print("4. Press Play and watch the debug output")
    print("5. Check if playback starts from the scroll position")
