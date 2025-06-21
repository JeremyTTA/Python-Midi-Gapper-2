#!/usr/bin/env python3
"""
Test the improved keyboard highlighting timing fix
"""

try:
    import sys
    import os
    import time
    sys.path.insert(0, os.path.dirname(__file__))
    
    from main import MidiGapperGUI
    
    # Test the improved timing calculation logic
    app = MidiGapperGUI()
    
    print("Testing improved keyboard highlighting timing:")
    print("=" * 50)
    
    # Test case 1: Starting from beginning (should work normally)
    print("Test 1: Starting from beginning")
    app.playback_position = 0.0
    app.visual_position_offset = 0.0
    app.playback_start_time = time.time()
    app.is_playing = True
    
    time.sleep(0.1)  # Small delay
    audio_pos = app.get_actual_audio_position()
    print(f"  Visual position: {app.playback_position:.2f}s")
    print(f"  Audio position: {audio_pos:.2f}s")
    print(f"  Expected: ~0.1s (should highlight notes)")
    
    # Test case 2: Seeking to middle (audio should be disabled until catch-up)
    print("\nTest 2: Seeking to middle (immediate after seek)")
    app.playback_position = 10.0
    app.visual_position_offset = 10.0
    app.playback_start_time = time.time()  # Just started
    app.is_playing = True
    
    audio_pos = app.get_actual_audio_position()
    print(f"  Visual position: {app.playback_position:.2f}s")
    print(f"  Audio position: {audio_pos:.2f}s")
    print(f"  Expected: -1 (highlighting disabled until audio catches up)")
    
    # Test case 3: After audio has been playing for a while from seek position
    print("\nTest 3: After audio has played for a while from seek position")
    app.playback_position = 10.0
    app.visual_position_offset = 10.0
    app.playback_start_time = time.time() - 12.0  # Started 12 seconds ago
    app.is_playing = True
    
    audio_pos = app.get_actual_audio_position()
    print(f"  Visual position: {app.playback_position:.2f}s")
    print(f"  Audio position: {audio_pos:.2f}s")
    print(f"  Expected: ~22.0s (audio has caught up and passed seek position)")
    
    # Test case 4: Not playing (manual seeking)
    print("\nTest 4: Not playing (manual seeking)")
    app.is_playing = False
    app.playback_position = 5.5
    audio_pos = app.get_actual_audio_position()
    print(f"  Visual position: {app.playback_position:.2f}s")
    print(f"  Audio position: {audio_pos:.2f}s")
    print(f"  Expected: 5.5s (should match visual position)")
    
    print("\n" + "=" * 50)
    print("✓ Improved timing calculation tests completed")
    print("\nKey improvements:")
    print("- When seeking, highlighting is disabled until audio catches up")
    print("- This prevents notes from highlighting too early")
    print("- Audio position returns -1 when behind seek position")
    print("- Keyboard highlighting respects this and shows no highlights")
    print("- Once audio catches up, normal highlighting resumes")
    
    app.destroy()
    
except Exception as e:
    print(f"Error during testing: {e}")
    import traceback
    traceback.print_exc()
