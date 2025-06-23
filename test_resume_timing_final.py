#!/usr/bin/env python3
"""
Final test for resume timing accuracy with unpause compensation.
Tests that resuming from pause results in perfect timing synchronization.
"""

import time
import tkinter as tk
import pygame
import mido
import tempfile
import os

class ResumeTimingTest:
    def __init__(self):
        self.is_playing = False
        self.is_paused = False
        self.playback_start_time = None
        self.playback_position = 0.0
        self.visual_position_offset = 0.0
        self.current_midi_file = None
        self.temp_midi_file = None
        
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
        
        # Add notes every 0.5 seconds for clear timing reference
        ticks_per_beat = midi.ticks_per_beat
        ticks_per_second = ticks_per_beat * 2  # 120 BPM = 2 beats per second
        ticks_per_note = ticks_per_second // 2  # Note every 0.5 seconds
        
        for i in range(int(duration_seconds * 2)):  # One note every 0.5 seconds
            note = 60 + (i % 12)  # C4 to B4
            track.append(mido.Message('note_on', channel=0, note=note, velocity=64, time=ticks_per_note))
            track.append(mido.Message('note_off', channel=0, note=note, velocity=64, time=ticks_per_note))
        
        # Save to temp file
        temp_file = tempfile.NamedTemporaryFile(suffix='.mid', delete=False)
        midi.save(temp_file.name)
        temp_file.close()
        return temp_file.name
    
    def get_actual_audio_position(self):
        """Calculate the actual audio playback position using corrected timing logic"""
        if not self.is_playing or self.playback_start_time is None:
            return self.playback_position
        
        elapsed_time = time.time() - self.playback_start_time
        
        if hasattr(self, 'visual_position_offset') and self.visual_position_offset > 0.1:
            return self.visual_position_offset + elapsed_time
        else:
            return elapsed_time
    
    def start_playback(self, from_position=0.0):
        """Start playback from given position"""
        try:
            self.playback_position = from_position
            
            if from_position > 0.1:
                # Create temp file for seeking
                self.visual_position_offset = from_position
                self.temp_midi_file = self.create_temp_midi_from_position(from_position)
                pygame.mixer.music.load(self.temp_midi_file)
                self.playback_start_time = time.time()
            else:
                # Play from beginning
                self.visual_position_offset = 0.0
                pygame.mixer.music.load(self.current_midi_file)
                self.playback_start_time = time.time() - from_position
            
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            
            print(f"Started playback from {from_position:.2f}s")
            
        except Exception as e:
            print(f"Error starting playback: {e}")
    
    def create_temp_midi_from_position(self, start_seconds):
        """Create a temp MIDI file starting from given position"""
        # Simple implementation - just copy the original file
        # In real implementation, this would seek to the correct position
        temp_file = tempfile.NamedTemporaryFile(suffix='.mid', delete=False)
        with open(self.current_midi_file, 'rb') as src:
            temp_file.write(src.read())
        temp_file.close()
        return temp_file.name
    
    def pause_playback(self):
        """Pause playback"""
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.is_playing = False
            print(f"Paused at position {self.get_actual_audio_position():.2f}s")
    
    def resume_playback(self):
        """Resume playback with improved timing compensation"""
        if self.is_paused:
            try:
                # Calculate timing BEFORE unpausing to minimize delay
                current_time = time.time()
                if hasattr(self, 'visual_position_offset') and self.visual_position_offset > 0.1:
                    # We're using a temp file, so audio is at elapsed time, visual at offset + elapsed
                    adjusted_start_time = current_time - (self.playback_position - self.visual_position_offset)
                else:
                    # We're playing from beginning, so audio position = visual position
                    adjusted_start_time = current_time - self.playback_position
                
                # Add small compensation for pygame unpause latency (typically 10-20ms)
                unpause_compensation = 0.015  # 15ms compensation
                adjusted_start_time += unpause_compensation
                
                pygame.mixer.music.unpause()
                
                # Set timing variables immediately after unpause
                self.playback_start_time = adjusted_start_time
                self.is_playing = True
                self.is_paused = False
                
                print(f"Resumed at position {self.playback_position:.2f}s")
                
            except Exception as e:
                print(f"Error resuming: {e}")
    
    def cleanup(self):
        """Clean up temp files"""
        pygame.mixer.music.stop()
        if self.temp_midi_file and os.path.exists(self.temp_midi_file):
            os.unlink(self.temp_midi_file)
        if self.current_midi_file and os.path.exists(self.current_midi_file):
            os.unlink(self.current_midi_file)

def test_resume_timing_accuracy():
    """Test resume timing accuracy with the improved compensation"""
    tester = ResumeTimingTest()
    
    try:
        print("=== Resume Timing Accuracy Test (With Unpause Compensation) ===\n")
        
        # Create test MIDI
        tester.current_midi_file = tester.create_test_midi(15)
        
        print("1. Starting playback from beginning...")
        tester.start_playback(0.0)
        
        # Let it play for 3 seconds
        time.sleep(3.0)
        position_before_pause = tester.get_actual_audio_position()
        print(f"Position before pause: {position_before_pause:.2f}s")
        
        print("2. Pausing playback...")
        tester.pause_playback()
        
        # Wait while paused
        time.sleep(1.0)
        
        print("3. Resuming playback...")
        tester.resume_playback()
        
        # Measure timing accuracy immediately after resume
        immediate_position = tester.get_actual_audio_position()
        print(f"Position immediately after resume: {immediate_position:.2f}s")
        print(f"Expected position: {position_before_pause:.2f}s")
        immediate_drift = immediate_position - position_before_pause
        print(f"Immediate timing drift: {immediate_drift:.3f}s")
        
        # Wait a moment and check again
        time.sleep(0.5)
        later_position = tester.get_actual_audio_position()
        expected_later = position_before_pause + 0.5
        print(f"Position 0.5s after resume: {later_position:.2f}s")
        print(f"Expected position: {expected_later:.2f}s")
        later_drift = later_position - expected_later
        print(f"Later timing drift: {later_drift:.3f}s")
        
        # Test multiple pause/resume cycles
        print("\n4. Testing multiple pause/resume cycles...")
        for i in range(3):
            time.sleep(1.0)
            pre_pause_pos = tester.get_actual_audio_position()
            
            tester.pause_playback()
            time.sleep(0.5)
            tester.resume_playback()
            
            post_resume_pos = tester.get_actual_audio_position()
            cycle_drift = post_resume_pos - pre_pause_pos
            print(f"Cycle {i+1} drift: {cycle_drift:.3f}s")
        
        # Test with seeking
        print("\n5. Testing pause/resume after seeking...")
        tester.playback_position = 7.0
        tester.start_playback(7.0)
        
        time.sleep(2.0)
        seek_pause_pos = tester.get_actual_audio_position()
        
        tester.pause_playback()
        time.sleep(0.5)
        tester.resume_playback()
        
        seek_resume_pos = tester.get_actual_audio_position()
        seek_drift = seek_resume_pos - seek_pause_pos
        print(f"Seek + pause/resume drift: {seek_drift:.3f}s")
        
        print("\n=== Test Results ===")
        print(f"Immediate resume drift: {immediate_drift:.3f}s")
        print(f"Later timing drift: {later_drift:.3f}s")
        print(f"Seek resume drift: {seek_drift:.3f}s")
        
        # Assess results
        if abs(immediate_drift) < 0.05 and abs(later_drift) < 0.05 and abs(seek_drift) < 0.05:
            print("✅ EXCELLENT: All resume operations within 50ms accuracy!")
        elif abs(immediate_drift) < 0.1 and abs(later_drift) < 0.1 and abs(seek_drift) < 0.1:
            print("✅ GOOD: All resume operations within 100ms accuracy!")
        elif abs(immediate_drift) < 0.2 and abs(later_drift) < 0.2 and abs(seek_drift) < 0.2:
            print("⚠️  ACCEPTABLE: Resume operations within 200ms accuracy")
        else:
            print("❌ POOR: Resume timing accuracy needs improvement")
        
    except Exception as e:
        print(f"Test error: {e}")
    finally:
        tester.cleanup()

if __name__ == "__main__":
    test_resume_timing_accuracy()
