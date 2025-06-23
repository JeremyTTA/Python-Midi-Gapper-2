#!/usr/bin/env python3
"""
Test for behind/ahead timing issue fix.
This tests the corrected timing logic to ensure audio position matches visual position.
"""

import time

class TimingTest:
    def __init__(self):
        self.is_playing = False
        self.playback_start_time = None
        self.playback_position = 0.0
        self.visual_position_offset = 0.0
        
    def get_actual_audio_position_old(self):
        """OLD method - had threshold mismatch and incorrect logic"""
        if not self.is_playing or self.playback_start_time is None:
            return self.playback_position
        
        elapsed_time = time.time() - self.playback_start_time
        
        # OLD LOGIC - threshold mismatch (0.1 vs 0.05) and complex conditional
        if hasattr(self, 'visual_position_offset') and self.visual_position_offset > 0.1:
            return self.visual_position_offset + elapsed_time
        else:
            return elapsed_time
    
    def get_actual_audio_position_new(self):
        """NEW method - simplified and consistent"""
        if not self.is_playing or self.playback_start_time is None:
            return self.playback_position
        
        elapsed_time = time.time() - self.playback_start_time
        
        # NEW LOGIC - playback_start_time is calculated to make elapsed_time = desired_position
        return elapsed_time
    
    def simulate_temp_file_playback(self, seek_position):
        """Simulate starting playback with temp file (NEW logic)"""
        print(f"\n--- Simulating temp file playback from {seek_position:.2f}s ---")
        
        # NEW timing logic for temp file
        self.playback_position = seek_position
        self.visual_position_offset = seek_position
        self.playback_start_time = time.time()  # Temp file starts at time 0
        self.is_playing = True
        
        print(f"Setup: position={self.playback_position:.2f}s, offset={self.visual_position_offset:.2f}s")
        print(f"Start time set to current time (temp file starts at 0)")
        
        # Test immediately
        time.sleep(0.1)
        new_pos = self.get_actual_audio_position_new()
        old_pos = self.get_actual_audio_position_old()
        expected = seek_position + 0.1
        
        print(f"After 0.1s:")
        print(f"  Expected position: {expected:.2f}s")
        print(f"  NEW method: {new_pos:.2f}s (drift: {new_pos - expected:.3f}s)")
        print(f"  OLD method: {old_pos:.2f}s (drift: {old_pos - expected:.3f}s)")
        
        return abs(new_pos - expected), abs(old_pos - expected)
    
    def simulate_original_file_with_offset(self, seek_position):
        """Simulate fallback to original file when temp creation fails (NEW logic)"""
        print(f"\n--- Simulating original file with offset {seek_position:.2f}s ---")
        
        # NEW timing logic when temp file creation fails
        self.playback_position = seek_position
        self.visual_position_offset = seek_position
        self.playback_start_time = time.time() - seek_position  # Adjusted for offset
        self.is_playing = True
        
        print(f"Setup: position={self.playback_position:.2f}s, offset={self.visual_position_offset:.2f}s")
        print(f"Start time adjusted backward by {seek_position:.2f}s")
        
        # Test immediately  
        time.sleep(0.1)
        new_pos = self.get_actual_audio_position_new()
        old_pos = self.get_actual_audio_position_old()
        expected = seek_position + 0.1
        
        print(f"After 0.1s:")
        print(f"  Expected position: {expected:.2f}s")
        print(f"  NEW method: {new_pos:.2f}s (drift: {new_pos - expected:.3f}s)")
        print(f"  OLD method: {old_pos:.2f}s (drift: {old_pos - expected:.3f}s)")
        
        return abs(new_pos - expected), abs(old_pos - expected)
    
    def simulate_normal_playback(self, start_position):
        """Simulate normal playback from beginning or small offset"""
        print(f"\n--- Simulating normal playback from {start_position:.2f}s ---")
        
        # Normal timing logic
        self.playback_position = start_position
        self.visual_position_offset = 0.0 if start_position <= 0.05 else start_position
        self.playback_start_time = time.time() - start_position
        self.is_playing = True
        
        print(f"Setup: position={self.playback_position:.2f}s, offset={self.visual_position_offset:.2f}s")
        print(f"Start time adjusted backward by {start_position:.2f}s")
        
        # Test immediately
        time.sleep(0.1)
        new_pos = self.get_actual_audio_position_new()
        old_pos = self.get_actual_audio_position_old()
        expected = start_position + 0.1
        
        print(f"After 0.1s:")
        print(f"  Expected position: {expected:.2f}s")
        print(f"  NEW method: {new_pos:.2f}s (drift: {new_pos - expected:.3f}s)")
        print(f"  OLD method: {old_pos:.2f}s (drift: {old_pos - expected:.3f}s)")
        
        return abs(new_pos - expected), abs(old_pos - expected)

def test_timing_fix():
    """Test the timing fix for various scenarios"""
    print("=== TIMING POSITION FIX TEST ===")
    print("Testing the fix for 'playing behind where it should' issue\n")
    
    tester = TimingTest()
    
    # Test scenarios
    test_positions = [0.0, 0.02, 0.1, 1.5, 5.7, 12.3]
    
    new_method_drifts = []
    old_method_drifts = []
    
    for pos in test_positions:
        if pos > 0.05:
            # Would use temp file normally
            new_drift, old_drift = tester.simulate_temp_file_playback(pos)
            new_method_drifts.append(new_drift)
            old_method_drifts.append(old_drift)
            
            # Also test fallback scenario
            new_drift2, old_drift2 = tester.simulate_original_file_with_offset(pos)
            new_method_drifts.append(new_drift2)
            old_method_drifts.append(old_drift2)
        else:
            # Normal playback
            new_drift, old_drift = tester.simulate_normal_playback(pos)
            new_method_drifts.append(new_drift)
            old_method_drifts.append(old_drift)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY:")
    avg_new_drift = sum(new_method_drifts) / len(new_method_drifts)
    avg_old_drift = sum(old_method_drifts) / len(old_method_drifts)
    max_new_drift = max(new_method_drifts)
    max_old_drift = max(old_method_drifts)
    
    print(f"NEW method - Average drift: {avg_new_drift:.3f}s, Max drift: {max_new_drift:.3f}s")
    print(f"OLD method - Average drift: {avg_old_drift:.3f}s, Max drift: {max_old_drift:.3f}s")
    
    if avg_new_drift < 0.02 and max_new_drift < 0.05:
        print("🎉 EXCELLENT: NEW method has very accurate timing!")
    elif avg_new_drift < avg_old_drift:
        print("✅ IMPROVED: NEW method is more accurate than OLD method")
    else:
        print("⚠️  WARNING: NEW method needs further refinement")
    
    print("\nThe fix should eliminate the 'playing behind' issue by:")
    print("1. Fixing threshold mismatch (0.05 vs 0.1)")
    print("2. Simplifying timing calculation")
    print("3. Consistent playback_start_time adjustment")

if __name__ == "__main__":
    test_timing_fix()
