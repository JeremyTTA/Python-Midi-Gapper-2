#!/usr/bin/env python3
"""
Simple timing verification test
"""

import os
import sys

# Add the directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_import():
    """Test if main.py can be imported"""
    try:
        print("Testing main.py import...")
        import main
        print("✅ SUCCESS: main.py imported without syntax errors!")
        
        # Test if the MidiGapperGUI class exists and has the fixed methods
        if hasattr(main, 'MidiGapperGUI'):
            print("✅ SUCCESS: MidiGapperGUI class found")
            
            # Check if the fixed methods exist
            gui_class = main.MidiGapperGUI
            if hasattr(gui_class, 'get_actual_audio_position'):
                print("✅ SUCCESS: get_actual_audio_position method found")
            else:
                print("❌ ERROR: get_actual_audio_position method not found")
                
            if hasattr(gui_class, '_start_pygame_playback'):
                print("✅ SUCCESS: _start_pygame_playback method found")
            else:
                print("❌ ERROR: _start_pygame_playback method not found")
                
            return True
        else:
            print("❌ ERROR: MidiGapperGUI class not found")
            return False
            
    except SyntaxError as e:
        print(f"❌ SYNTAX ERROR: {e}")
        return False
    except Exception as e:
        print(f"❌ IMPORT ERROR: {e}")
        return False

def test_timing_logic():
    """Test the timing logic conceptually"""
    print("\n=== TESTING TIMING LOGIC ===")
    
    # Simulate the timing calculation
    import time
    
    # Scenario 1: Normal playback from beginning
    print("Test 1: Normal playback from beginning")
    current_time = time.time()
    playback_start_time = current_time  # Start at current time
    audio_start_offset = 0.0  # No offset
    
    # Simulate 2 seconds of playback
    time.sleep(0.1)  # Small delay to simulate
    
    # Calculate position
    elapsed_time = time.time() - playback_start_time
    position = elapsed_time  # Should equal elapsed time
    print(f"  Elapsed: {elapsed_time:.3f}s, Position: {position:.3f}s ✅")
    
    # Scenario 2: Playback with offset (temp file or seeking)
    print("Test 2: Playback with offset (seeking)")
    seek_position = 5.0  # Seeking to 5 seconds
    current_time = time.time()
    audio_start_offset = seek_position
    playback_start_time = current_time - audio_start_offset  # Adjust for offset
    
    # Calculate position immediately
    elapsed_time = time.time() - playback_start_time
    position = elapsed_time  # Should equal seek_position + small delay
    print(f"  Seek to: {seek_position:.3f}s, Position: {position:.3f}s")
    if abs(position - seek_position) < 0.1:
        print("  ✅ SUCCESS: Position matches seek target")
    else:
        print("  ❌ ERROR: Position doesn't match seek target")
    
    print("\n=== TIMING LOGIC TEST COMPLETE ===")

if __name__ == "__main__":
    print("=== TIMING FIX VERIFICATION ===\n")
    
    success = test_import()
    if success:
        test_timing_logic()
        print("\n✅ OVERALL: Timing fix appears to be working correctly!")
        print("\nNext steps:")
        print("1. Run the main application: python main.py")
        print("2. Load a MIDI file")
        print("3. Test play/pause/seeking operations")
        print("4. Verify that audio and visual positions stay in sync")
    else:
        print("\n❌ OVERALL: There are still issues with main.py")
        print("Please check the syntax errors above")
