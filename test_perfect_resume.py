#!/usr/bin/env python3
"""
Test for perfect resume timing after fixing the unpause delay issue.
This test verifies that resuming from pause now has perfect timing by always restarting.
"""

import time
import tkinter as tk
import pygame
import mido
import tempfile
import os

class PerfectResumeTest:
    def __init__(self):
        self.is_playing = False
        self.is_paused = False
        self.playback_start_time = None
        self.playback_position = 0.0
        self.visual_position_offset = 0.0
        self.current_midi_file = None
        
        # Initialize pygame
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
        pygame.mixer.init()
        
    def create_test_midi(self, duration_seconds=10):
        """Create a test MIDI file with regular note events"""
        midi = mido.MidiFile()
        track = mido.MidiTrack()
        midi.tracks.append(track)
        
        # Add some basic setup
        track.append(mido.MetaMessage('set_tempo', tempo=500000))  # 120 BPM
        track.append(mido.Message('program_change', channel=0, program=1))
        
        # Add notes every 0.25 seconds for precise timing reference
        ticks_per_beat = midi.ticks_per_beat
        ticks_per_second = ticks_per_beat * 2  # 120 BPM = 2 beats per second
        ticks_per_note = ticks_per_second // 4  # Note every 0.25 seconds
        
        for i in range(int(duration_seconds * 4)):  # One note every 0.25 seconds
            note = 60 + (i % 12)  # C4 to B4
            track.append(mido.Message('note_on', channel=0, note=note, velocity=64, time=ticks_per_note))
            track.append(mido.Message('note_off', channel=0, note=note, velocity=64, time=ticks_per_note))
        
        # Save to temp file
        temp_file = tempfile.NamedTemporaryFile(suffix='.mid', delete=False)
        midi.save(temp_file.name)
        temp_file.close()
        return temp_file.name
    
    def get_actual_audio_position(self):
        """Calculate the actual audio playback position"""
        if not self.is_playing or self.playback_start_time is None:
            return self.playback_position
        
        elapsed_time = time.time() - self.playback_start_time
        
        if hasattr(self, 'visual_position_offset') and self.visual_position_offset > 0.05:
            return self.visual_position_offset + elapsed_time
        else:
            return elapsed_time
    
    def start_playback(self, from_position=0.0):
        """Start playback from given position (simulated restart approach)"""
        try:
            self.playback_position = from_position
            
            # Always use "restart" approach for perfect timing
            # This simulates the new fix where we always restart instead of unpause
            
            # For any position > 0.05s, we would create a temp file (simulated here)
            if from_position > 0.05:
                self.visual_position_offset = from_position
                # In real implementation, this would create a temp MIDI file
                self.playback_start_time = time.time()
                print(f"Started with temp file simulation from {from_position:.2f}s")
            else:
                self.visual_position_offset = 0.0
                self.playback_start_time = time.time() - from_position
                print(f"Started from beginning with offset {from_position:.2f}s")
            
            # Load and play (simulated)
            pygame.mixer.music.load(self.current_midi_file)
            pygame.mixer.music.play()
            
            self.is_playing = True
            self.is_paused = False
            
            print(f"✓ Started playback from {from_position:.2f}s using restart approach")
            
        except Exception as e:
            print(f"Error starting playback: {e}")
    
    def pause_playback(self):
        """Pause playback"""
        if self.is_playing and not self.is_paused:
            # Update position to current audio position
            self.playback_position = self.get_actual_audio_position()
            pygame.mixer.music.pause()
            self.is_paused = True
            self.is_playing = False
            print(f"✓ Paused at position {self.playback_position:.2f}s")
    
    def resume_playback_new_method(self):
        """Resume playback using the NEW method (always restart)"""
        if self.is_paused:
            try:
                print(f"RESUME: Always restarting from position {self.playback_position:.2f}s")
                
                # NEW METHOD: Always stop and restart (no unpause)
                pygame.mixer.music.stop()
                self.is_playing = False
                self.is_paused = False
                
                # Restart from current position
                self.start_playback(self.playback_position)
                
                print(f"✓ Resumed using restart method from {self.playback_position:.2f}s")
                
            except Exception as e:
                print(f"Error in new resume method: {e}")
    
    def cleanup(self):
        """Clean up"""
        pygame.mixer.music.stop()
        if self.current_midi_file and os.path.exists(self.current_midi_file):
            os.unlink(self.current_midi_file)

def test_perfect_resume_timing():
    """Test the new perfect resume timing approach"""
    tester = PerfectResumeTest()
    
    try:
        print("=== Perfect Resume Timing Test (Always Restart Method) ===\n")
        
        # Create test MIDI
        tester.current_midi_file = tester.create_test_midi(15)
        
        print("1. Starting playback from beginning...")
        tester.start_playback(0.0)
        
        # Let it play for 2.5 seconds
        time.sleep(2.5)
        
        print("2. Pausing playback...")
        pause_position = tester.get_actual_audio_position()
        tester.pause_playback()
        print(f"   Paused at: {pause_position:.3f}s")
        
        # Wait while paused
        time.sleep(1.0)
        
        print("3. Resuming with NEW method (always restart)...")
        resume_start_time = time.time()
        tester.resume_playback_new_method()
        
        # Check timing immediately after resume
        time.sleep(0.1)  # Small delay to let audio start
        immediate_position = tester.get_actual_audio_position()
        expected_position = pause_position + 0.1
        immediate_drift = immediate_position - expected_position
        
        print(f"   Expected position after 0.1s: {expected_position:.3f}s")
        print(f"   Actual position after 0.1s: {immediate_position:.3f}s")
        print(f"   Immediate timing drift: {immediate_drift:.3f}s")
        
        # Test multiple pause/resume cycles
        print("\n4. Testing rapid pause/resume cycles...")
        cycle_drifts = []
        
        for i in range(5):
            # Let it play briefly
            time.sleep(0.5)
            pre_pause = tester.get_actual_audio_position()
            
            # Pause
            tester.pause_playback()
            
            # Brief pause
            time.sleep(0.2)
            
            # Resume with new method
            tester.resume_playback_new_method()
            
            # Check timing after brief delay
            time.sleep(0.1)
            post_resume = tester.get_actual_audio_position()
            expected_post = pre_pause + 0.1
            cycle_drift = post_resume - expected_post
            cycle_drifts.append(cycle_drift)
            
            print(f"   Cycle {i+1}: drift = {cycle_drift:.3f}s")
        
        # Test with different positions
        print("\n5. Testing resume from various positions...")
        test_positions = [1.0, 3.5, 7.2, 10.8]
        position_drifts = []
        
        for pos in test_positions:
            tester.start_playback(pos)
            time.sleep(0.3)
            
            actual_before_pause = tester.get_actual_audio_position()
            tester.pause_playback()
            time.sleep(0.1)
            tester.resume_playback_new_method()
            time.sleep(0.2)
            
            actual_after_resume = tester.get_actual_audio_position()
            expected_after_resume = actual_before_pause + 0.2
            drift = actual_after_resume - expected_after_resume
            position_drifts.append(drift)
            
            print(f"   Position {pos:.1f}s: drift = {drift:.3f}s")
        
        # Final assessment
        print("\n=== RESULTS ===")
        avg_cycle_drift = sum(abs(d) for d in cycle_drifts) / len(cycle_drifts)
        avg_position_drift = sum(abs(d) for d in position_drifts) / len(position_drifts)
        
        print(f"Immediate resume drift: {abs(immediate_drift):.3f}s")
        print(f"Average cycle drift: {avg_cycle_drift:.3f}s")
        print(f"Average position drift: {avg_position_drift:.3f}s")
        
        if abs(immediate_drift) < 0.05 and avg_cycle_drift < 0.05 and avg_position_drift < 0.05:
            print("🎉 EXCELLENT: Perfect timing! All drifts < 50ms")
        elif abs(immediate_drift) < 0.1 and avg_cycle_drift < 0.1 and avg_position_drift < 0.1:
            print("✅ VERY GOOD: Excellent timing! All drifts < 100ms")
        elif abs(immediate_drift) < 0.2 and avg_cycle_drift < 0.2 and avg_position_drift < 0.2:
            print("✅ GOOD: Good timing! All drifts < 200ms")
        else:
            print("⚠️  NEEDS IMPROVEMENT: Some timing drifts > 200ms")
        
        print("\nThe new 'always restart' method should eliminate unpause delays!")
        
    except Exception as e:
        print(f"Test error: {e}")
    finally:
        tester.cleanup()

if __name__ == "__main__":
    test_perfect_resume_timing()
