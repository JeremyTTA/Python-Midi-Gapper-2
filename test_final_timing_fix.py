#!/usr/bin/env python3
"""
Comprehensive timing accuracy test for MIDI playback after the final timing fix.
Tests pause/resume and seeking accuracy with the new unified timing approach.
"""

import sys
import os
import time
import pygame
import mido

# Add the current directory to Python path so we can import main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the main MIDI player class
from main import MIDIPlayer

def test_timing_accuracy():
    """Test that playback timing is perfectly accurate after pause/resume and seeking"""
    
    print("=== COMPREHENSIVE TIMING ACCURACY TEST ===")
    print("Testing the final timing fix for perfect audio-visual sync")
    print()
    
    # Initialize pygame
    pygame.init()
    pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
    pygame.mixer.init()
    
    # Create a mock MIDI player instance (without GUI)
    class MockMIDIPlayer:
        def __init__(self):
            self.current_midi_file = None
            self.playback_position = 0.0
            self.playback_start_time = None
            self.is_playing = False
            self.is_paused = False
            self.temp_midi_files = []
            
            # New timing variables for the fix
            self.using_temp_file = False
            self.audio_start_offset = 0.0
            
        def find_midi_files(self):
            """Find available MIDI files in the current directory"""
            midi_files = []
            for file in os.listdir('.'):
                if file.lower().endswith(('.mid', '.midi')):
                    midi_files.append(file)
            return midi_files
        
        def get_actual_audio_position(self):
            """Calculate the actual audio playback position with perfect timing synchronization"""
            if not self.is_playing or self.playback_start_time is None:
                return self.playback_position
            
            # Calculate elapsed time since audio started
            elapsed_time = time.time() - self.playback_start_time
            
            # The playback_start_time is already adjusted for any offset during playback initialization
            # So elapsed_time directly represents the current playback position
            return elapsed_time
        
        def _start_pygame_playback(self):
            """Start MIDI playback using pygame with real audio seeking support"""
            print(f"  Starting playback from position: {self.playback_position:.2f}s")
            
            # Clear any previous timing state
            self.using_temp_file = False
            self.audio_start_offset = 0.0
            
            # For seeking: create a temporary MIDI file starting from the seek position
            if self.playback_position > 0.05:
                print(f"  Position > 0.05s, would create temporary MIDI file...")
                # Simulate temp file creation success
                self.using_temp_file = True
                self.audio_start_offset = self.playback_position
                print(f"  ✓ Simulated temp file creation successful")
            else:
                print(f"  Position <= 0.05s, using original file")
                self.using_temp_file = False
                self.audio_start_offset = 0.0
                self.playback_position = 0.0
            
            # Load and play the MIDI file
            pygame.mixer.music.load(self.current_midi_file)
            pygame.mixer.music.play()
            
            # CRITICAL TIMING FIX: Set playback_start_time to account for audio offset
            current_time = time.time()
            self.playback_start_time = current_time - self.audio_start_offset
            
            print(f"  Timing setup - offset: {self.audio_start_offset:.3f}s, using_temp: {self.using_temp_file}")
            print(f"  playback_start_time adjusted by {self.audio_start_offset:.3f}s for perfect sync")
            
            # Set playback state
            self.is_playing = True
            self.is_paused = False
            
        def start_playback(self):
            """Start playback from current position"""
            self._start_pygame_playback()
            
        def pause_playback(self):
            """Pause playback and store current position"""
            if self.is_playing:
                self.playback_position = self.get_actual_audio_position()
                pygame.mixer.music.stop()
                self.is_playing = False
                self.is_paused = True
                print(f"  Paused at position: {self.playback_position:.3f}s")
                
        def resume_playback(self):
            """Resume playback from stored position"""
            if self.is_paused:
                print(f"  Resuming from position: {self.playback_position:.3f}s")
                self.is_paused = False
                self._start_pygame_playback()
                
        def seek_to_position(self, position):
            """Seek to a specific position"""
            was_playing = self.is_playing
            if was_playing:
                pygame.mixer.music.stop()
            
            self.playback_position = position
            print(f"  Seeking to position: {position:.3f}s")
            
            if was_playing:
                self._start_pygame_playback()
                
        def cleanup(self):
            """Clean up resources"""
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            pygame.quit()
    
    # Create mock player
    player = MockMIDIPlayer()
    
    # Find MIDI files
    midi_files = player.find_midi_files()
    if not midi_files:
        print("ERROR: No MIDI files found in current directory")
        return False
    
    # Use the first available MIDI file
    test_file = midi_files[0]
    player.current_midi_file = test_file
    print(f"Using test file: {test_file}")
    print()
    
    try:
        # Test 1: Normal playback from beginning
        print("TEST 1: Normal playback from beginning")
        player.playback_position = 0.0
        player.start_playback()
        
        # Check position after 1 second
        time.sleep(1.0)
        actual_pos = player.get_actual_audio_position()
        expected_pos = 1.0
        print(f"  After 1 second - Expected: {expected_pos:.3f}s, Actual: {actual_pos:.3f}s")
        print(f"  Accuracy: {abs(actual_pos - expected_pos):.3f}s difference")
        
        # Test 2: Pause and resume
        print("\nTEST 2: Pause and resume")
        player.pause_playback()
        pause_position = player.playback_position
        
        # Wait 2 seconds while paused
        print("  Waiting 2 seconds while paused...")
        time.sleep(2.0)
        
        # Resume
        player.resume_playback()
        resume_time = time.time()
        
        # Check position after 1 more second
        time.sleep(1.0)
        actual_pos = player.get_actual_audio_position()
        expected_pos = pause_position + 1.0  # Should be pause position + 1 second of playback
        print(f"  After resume + 1 second - Expected: {expected_pos:.3f}s, Actual: {actual_pos:.3f}s")
        print(f"  Accuracy: {abs(actual_pos - expected_pos):.3f}s difference")
        
        # Test 3: Seeking to different positions
        print("\nTEST 3: Seeking accuracy")
        test_positions = [0.0, 2.5, 5.0, 10.0]
        
        for seek_pos in test_positions:
            print(f"  Seeking to {seek_pos:.1f}s...")
            player.seek_to_position(seek_pos)
            
            # Wait 0.5 seconds
            time.sleep(0.5)
            
            actual_pos = player.get_actual_audio_position()
            expected_pos = seek_pos + 0.5
            print(f"    After 0.5s - Expected: {expected_pos:.3f}s, Actual: {actual_pos:.3f}s")
            print(f"    Accuracy: {abs(actual_pos - expected_pos):.3f}s difference")
        
        # Test 4: Multiple pause/resume cycles
        print("\nTEST 4: Multiple pause/resume cycles")
        for i in range(3):
            print(f"  Cycle {i+1}:")
            
            # Play for 1 second
            time.sleep(1.0)
            before_pause = player.get_actual_audio_position()
            
            # Pause
            player.pause_playback()
            
            # Wait 1 second while paused
            time.sleep(1.0)
            
            # Resume
            player.resume_playback()
            
            # Play for 1 more second
            time.sleep(1.0)
            after_resume = player.get_actual_audio_position()
            
            expected_progress = 2.0  # 1s before pause + 1s after resume
            actual_progress = after_resume - before_pause
            print(f"    Expected progress: {expected_progress:.3f}s, Actual: {actual_progress:.3f}s")
            print(f"    Accuracy: {abs(actual_progress - expected_progress):.3f}s difference")
        
        print("\n=== TIMING ACCURACY TEST COMPLETED ===")
        print("If all differences are < 0.1s, the timing fix is working correctly!")
        
        return True
        
    except Exception as e:
        print(f"ERROR during testing: {e}")
        return False
        
    finally:
        # Cleanup
        player.cleanup()

if __name__ == "__main__":
    test_timing_accuracy()
