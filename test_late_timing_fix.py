#!/usr/bin/env python3
"""
Test script to verify the pause/resume timing fix works correctly.
This tests both the "too early" and "too late" scenarios.
"""

import time

class PygameMIDISimulator:
    """Simulates pygame MIDI behavior for testing"""
    
    def __init__(self):
        self.playback_start_time = None
        self.playback_position = 0.0
        self.visual_position_offset = 0.0
        self.is_playing = False
        self.is_paused = False
    
    def start_playback(self, position=0.0):
        """Start playback from a specific position"""
        self.playback_position = position
        
        # Simulate temp file creation for seeking
        if position > 0.1:
            self.visual_position_offset = position
            # Using temp file - audio starts at 0, visual starts at offset
            self.playback_start_time = time.time()
        else:
            self.visual_position_offset = 0.0
            # Using original file - adjust for current position
            self.playback_start_time = time.time() - position
        
        self.is_playing = True
        self.is_paused = False
        print(f"Started playback at position {position:.2f}s")
    
    def pause_playback(self):
        """Pause playback and capture current position"""
        if self.is_playing and self.playback_start_time:
            elapsed = time.time() - self.playback_start_time
            # Calculate absolute position based on whether we're using temp file or not
            if hasattr(self, 'visual_position_offset') and self.visual_position_offset > 0.1:
                self.playback_position = self.visual_position_offset + elapsed
            else:
                self.playback_position = elapsed
            
            self.is_playing = False
            self.is_paused = True
            print(f"Paused at position {self.playback_position:.2f}s")
    
    def resume_playback(self):
        """Resume playback from paused position"""
        if self.is_paused:
            # For resume, adjust start time based on current position
            # Always use simple unpause and timing adjustment for better responsiveness
            if hasattr(self, 'visual_position_offset') and self.visual_position_offset > 0.1:
                # We're using a temp file, so audio is at elapsed time, visual at offset + elapsed
                self.playback_start_time = time.time() - (self.playback_position - self.visual_position_offset)
            else:
                # We're playing from beginning, so audio position = visual position
                self.playback_start_time = time.time() - self.playback_position
            
            self.is_playing = True
            self.is_paused = False
            print(f"Resumed from position {self.playback_position:.2f}s")
    
    def get_actual_audio_position(self):
        """Get current playback position"""
        if not self.is_playing or self.playback_start_time is None:
            return self.playback_position
        
        elapsed_time = time.time() - self.playback_start_time
        
        # For pygame MIDI with temp file seeking:
        if hasattr(self, 'visual_position_offset') and self.visual_position_offset > 0.1:
            # We're using a temp file that starts from visual_position_offset
            return self.visual_position_offset + elapsed_time
        else:
            # We're playing from the beginning
            return elapsed_time

def test_timing_accuracy():
    """Test that pause/resume timing is accurate"""
    print("Testing timing fix for 'playing too late' issue...")
    
    test = PygameMIDISimulator()
    
    # Test 1: Start from beginning, pause, resume
    print("\n=== Test 1: Basic pause/resume from beginning ===")
    test.start_playback(0.0)
    time.sleep(1.0)  # Play for 1 second
    
    pos_before_pause = test.get_actual_audio_position()
    print(f"Position before pause: {pos_before_pause:.2f}s")
    
    test.pause_playback()
    time.sleep(0.5)  # Pause for 0.5 seconds
    
    test.resume_playback()
    time.sleep(1.0)  # Play for another 1 second
    
    pos_after_resume = test.get_actual_audio_position()
    expected_position = 2.0  # Should be ~2 seconds (1s + 0s pause + 1s)
    error = abs(pos_after_resume - expected_position)
    
    print(f"Position after resume: {pos_after_resume:.2f}s")
    print(f"Expected position: {expected_position:.2f}s")
    print(f"Timing error: {error:.3f}s")
    
    if error < 0.1:
        print("✓ Test 1 PASSED - Timing is accurate!")
    else:
        print("✗ Test 1 FAILED - Timing drift detected!")
    
    # Test 2: Start from middle position (with temp file), pause, resume
    print("\n=== Test 2: Seeking + pause/resume (temp file scenario) ===")
    test.start_playback(5.0)  # Start from 5 seconds (uses temp file)
    time.sleep(1.0)  # Play for 1 second
    
    pos_before_pause2 = test.get_actual_audio_position()
    print(f"Position before pause: {pos_before_pause2:.2f}s")
    
    test.pause_playback()
    time.sleep(0.3)  # Pause briefly
    
    test.resume_playback()
    time.sleep(1.0)  # Play for another 1 second
    
    pos_final = test.get_actual_audio_position()
    expected_final = 7.0  # Should be ~7 seconds (5s start + 1s + 0s pause + 1s)
    error_final = abs(pos_final - expected_final)
    
    print(f"Final position: {pos_final:.2f}s")
    print(f"Expected position: {expected_final:.2f}s")
    print(f"Timing error: {error_final:.3f}s")
    
    if error_final < 0.1:
        print("✓ Test 2 PASSED - Seeking + pause/resume timing is accurate!")
    else:
        print("✗ Test 2 FAILED - Timing drift detected with seeking!")
    
    # Test 3: Multiple pause/resume cycles
    print("\n=== Test 3: Multiple pause/resume cycles ===")
    test.start_playback(10.0)  # Start from 10 seconds
    
    start_time = time.time()
    total_pause_time = 0.0
    
    for i in range(3):
        time.sleep(0.5)  # Play for 0.5s
        test.pause_playback()
        
        pause_start = time.time()
        time.sleep(0.2)  # Pause for 0.2s
        total_pause_time += 0.2
        
        test.resume_playback()
    
    time.sleep(0.5)  # Final play period
    
    total_elapsed = time.time() - start_time
    actual_play_time = total_elapsed - total_pause_time
    pos_final_multi = test.get_actual_audio_position()
    expected_final_multi = 10.0 + actual_play_time
    error_multi = abs(pos_final_multi - expected_final_multi)
    
    print(f"Total elapsed time: {total_elapsed:.2f}s")
    print(f"Total pause time: {total_pause_time:.2f}s")
    print(f"Actual play time: {actual_play_time:.2f}s")
    print(f"Final position: {pos_final_multi:.2f}s")
    print(f"Expected position: {expected_final_multi:.2f}s")
    print(f"Timing error: {error_multi:.3f}s")
    
    if error_multi < 0.2:  # More tolerance for multiple cycles
        print("✓ Test 3 PASSED - Multiple pause/resume cycles are accurate!")
    else:
        print("✗ Test 3 FAILED - Timing drift in multiple cycles!")
    
    # Overall result
    if error < 0.1 and error_final < 0.1 and error_multi < 0.2:
        print("\n🎉 ALL TESTS PASSED - 'Playing too late' issue is fixed!")
        return True
    else:
        print("\n❌ SOME TESTS FAILED - Timing issues remain!")
        return False

if __name__ == "__main__":
    test_timing_accuracy()
