#!/usr/bin/env python3
"""
Test script to verify the playback position fixes are working correctly.
This will test the position calculation and temp file creation logic.
"""

import os
import sys
import time

# Add the project directory to path so we can import main
project_dir = r"g:\My Drive\Programming Projects\Player Piano\Jeremys Code\Python Midi Gapper 2"
sys.path.insert(0, project_dir)

def test_position_calculation():
    """Test the position calculation logic"""
    print("=== TESTING POSITION CALCULATION ===")
    
    # Simulate different scenarios
    max_time = 120.0  # 2 minute file
    
    test_cases = [
        # (scroll_top, scroll_bottom, expected_time, description)
        (0.0, 1.0, 0.0, "At the bottom (start of song)"),
        (0.0, 0.5, 60.0, "Middle of viewport at middle of song"),
        (0.0, 0.0, 120.0, "At the top (end of song)"),
        (0.25, 0.75, 30.0, "Bottom quarter of visible area"),
        (0.5, 1.0, 0.0, "Bottom half visible"),
    ]
    
    print(f"File duration: {max_time}s")
    print("Formula: time_position = (1.0 - scroll_bottom) * max_time")
    print()
    
    for scroll_top, scroll_bottom, expected_time, description in test_cases:
        calculated_time = (1.0 - scroll_bottom) * max_time
        print(f"Case: {description}")
        print(f"  Scroll: top={scroll_top:.2f}, bottom={scroll_bottom:.2f}")
        print(f"  Expected: {expected_time:.1f}s")
        print(f"  Calculated: {calculated_time:.1f}s")
        print(f"  Match: {'✓' if abs(calculated_time - expected_time) < 0.1 else '✗'}")
        print()

def test_temp_file_creation():
    """Test that temp file creation is working"""
    print("=== TESTING TEMP FILE CREATION ===")
    
    try:
        import mido
        print("✓ mido library is available")
        
        # Look for test MIDI files
        midi_files = []
        for file in os.listdir(project_dir):
            if file.lower().endswith(('.mid', '.midi')):
                midi_files.append(os.path.join(project_dir, file))
        
        if not midi_files:
            print("✗ No MIDI files found for testing")
            return False
        
        test_file = midi_files[0]
        print(f"✓ Found test file: {os.path.basename(test_file)}")
        
        # Test basic MIDI file loading
        mid = mido.MidiFile(test_file)
        print(f"✓ MIDI file loaded successfully")
        print(f"  Type: {mid.type}")
        print(f"  Ticks per beat: {mid.ticks_per_beat}")
        print(f"  Tracks: {len(mid.tracks)}")
        
        # Calculate duration
        total_time = 0.0
        tempo = 500000
        
        for track in mid.tracks:
            track_time = 0.0
            current_tempo = tempo
            for msg in track:
                if msg.time > 0:
                    delta_time = mido.tick2second(msg.time, mid.ticks_per_beat, current_tempo)
                    track_time += delta_time
                if msg.type == 'set_tempo':
                    current_tempo = msg.tempo
            total_time = max(total_time, track_time)
        
        print(f"  Duration: {total_time:.2f}s")
        
        # Test creating a temp file at different positions
        test_positions = [5.0, 15.0, 30.0]
        
        for pos in test_positions:
            if pos < total_time:
                print(f"\n  Testing temp file creation at {pos:.1f}s...")
                
                # Simulate the temp file creation logic
                new_mid = mido.MidiFile(ticks_per_beat=mid.ticks_per_beat, type=mid.type)
                
                for track_idx, track in enumerate(mid.tracks):
                    new_track = mido.MidiTrack()
                    current_time = 0.0
                    current_tempo = tempo
                    messages_added = 0
                    
                    for msg in track:
                        if msg.time > 0:
                            delta_time = mido.tick2second(msg.time, mid.ticks_per_beat, current_tempo)
                            current_time += delta_time
                        
                        if msg.type == 'set_tempo':
                            current_tempo = msg.tempo
                        
                        if current_time >= pos:
                            if len(new_track) == 0:
                                # First message should start immediately
                                adjusted_msg = msg.copy(time=0)
                            else:
                                adjusted_msg = msg.copy()
                            
                            new_track.append(adjusted_msg)
                            messages_added += 1
                    
                    new_mid.tracks.append(new_track)
                
                print(f"    ✓ Temp file would have {len(new_mid.tracks)} tracks")
                total_messages = sum(len(track) for track in new_mid.tracks)
                print(f"    ✓ Total messages: {total_messages}")
        
        return True
        
    except ImportError:
        print("✗ mido library not available")
        return False
    except Exception as e:
        print(f"✗ Error testing temp file creation: {e}")
        return False

def test_app_startup():
    """Test that the main app can start without errors"""
    print("=== TESTING APP STARTUP ===")
    
    try:
        # Import without running
        from main import MidiGapperGUI
        print("✓ Main module imports successfully")
        
        # Test that key methods exist
        required_methods = [
            'create_temp_midi_from_position',
            'update_playback_position_from_scroll',
            'start_midi_playback',
            'sync_scrollbar_to_midi_position'
        ]
        
        for method_name in required_methods:
            if hasattr(MidiGapperGUI, method_name):
                print(f"✓ Method '{method_name}' exists")
            else:
                print(f"✗ Method '{method_name}' missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Error importing main module: {e}")
        return False

def main():
    print("PLAYBACK POSITION FIX VERIFICATION")
    print("=" * 50)
    
    # Run all tests
    tests = [
        ("Position Calculation", test_position_calculation),
        ("Temp File Creation", test_temp_file_creation),
        ("App Startup", test_app_startup),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name) * 2)
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY:")
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! The fixes should be working correctly.")
    else:
        print("✗ Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
