#!/usr/bin/env python3
"""
Test the keyboard highlighting timing fix
"""

try:
    import sys
    import os
    import time
    sys.path.insert(0, os.path.dirname(__file__))
    
    from main import MidiGapperGUI
    
    # Test the timing calculation logic
    app = MidiGapperGUI()
    
    # Test case 1: Starting from beginning
    print("Test 1: Starting from beginning")
    app.playback_position = 0.0
    app.visual_position_offset = 0.0
    app.playback_start_time = time.time()
    app.is_playing = True
    
    # Simulate 1 second of playback
    time.sleep(0.1)  # Small delay to test
    audio_pos = app.get_actual_audio_position()
    print(f"  Visual position: {app.playback_position:.2f}s")
    print(f"  Audio position: {audio_pos:.2f}s")
    print(f"  Should be close to 0.1s")
    
    # Test case 2: Starting from middle
    print("\nTest 2: Starting from middle (seeking)")
    app.playback_position = 10.0
    app.visual_position_offset = 10.0
    app.playback_start_time = time.time()
    app.is_playing = True
    
    # Simulate 0.5 seconds of playback
    time.sleep(0.1)
    audio_pos = app.get_actual_audio_position()
    print(f"  Visual position: {app.playback_position:.2f}s")
    print(f"  Audio position: {audio_pos:.2f}s")
    print(f"  Audio should be around 0.1s (because pygame starts from 0)")
    
    # Test case 3: Not playing (manual seeking)
    print("\nTest 3: Not playing (manual seeking)")
    app.is_playing = False
    app.playback_position = 5.5
    audio_pos = app.get_actual_audio_position()
    print(f"  Visual position: {app.playback_position:.2f}s")
    print(f"  Audio position: {audio_pos:.2f}s")
    print(f"  Should match visual position: 5.5s")
    
    print("\n✓ Timing calculation tests completed")
    print("\nKey changes made:")
    print("- Added playback_start_time tracking")
    print("- Added visual_position_offset tracking")
    print("- Updated get_actual_audio_position() to handle pygame MIDI seeking limitation")
    print("- Keyboard highlighting now uses actual audio position instead of visual position")
    print("- This should fix the timing mismatch between highlighting and audio")
    
    app.destroy()
    
except Exception as e:
    print(f"Error during testing: {e}")
    import traceback
    traceback.print_exc()
