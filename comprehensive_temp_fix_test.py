#!/usr/bin/env python3
"""
Comprehensive test and fix for temp MIDI file playback issues
"""

import os
import sys
import traceback

def log(message):
    """Log message to both console and file"""
    print(message)
    with open("temp_fix_test_log.txt", "a") as f:
        f.write(message + "\n")

def main():
    """Main test function"""
    
    # Clear log file
    if os.path.exists("temp_fix_test_log.txt"):
        os.unlink("temp_fix_test_log.txt")
    
    log("=== COMPREHENSIVE TEMP MIDI FIX TEST ===")
    log(f"Python version: {sys.version}")
    log(f"Working directory: {os.getcwd()}")
    
    # Test imports
    try:
        import mido
        log(f"✓ mido available: {mido.__version__}")
    except ImportError as e:
        log(f"✗ mido not available: {e}")
        return False
    
    try:
        import pygame
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)
        log("✓ pygame mixer initialized")
    except Exception as e:
        log(f"✗ pygame error: {e}")
        return False
    
    # Find test files
    midi_files = [f for f in os.listdir('.') if f.endswith(('.mid', '.midi'))]
    log(f"Available MIDI files: {midi_files}")
    
    if not midi_files:
        log("✗ No MIDI files found")
        return False
    
    test_file = midi_files[0]
    log(f"Using test file: {test_file}")
    
    try:
        # Load original file
        log("\n=== ORIGINAL FILE ANALYSIS ===")
        original = mido.MidiFile(test_file)
        log(f"Original file loaded successfully")
        log(f"  Tracks: {len(original.tracks)}")
        log(f"  Duration: {original.length:.2f} seconds")
        log(f"  Ticks per beat: {original.ticks_per_beat}")
        
        # Count content
        original_notes = 0
        for track in original.tracks:
            for msg in track:
                if msg.type == 'note_on' and msg.velocity > 0:
                    original_notes += 1
        log(f"  Total notes: {original_notes}")
        
        # Test original file with pygame
        log("\n=== ORIGINAL FILE PYGAME TEST ===")
        try:
            pygame.mixer.music.load(test_file)
            pygame.mixer.music.play()
            
            import time
            time.sleep(0.2)
            
            if pygame.mixer.music.get_busy():
                log("✓ Original file plays correctly in pygame")
                pygame.mixer.music.stop()
            else:
                log("⚠ Original file doesn't play in pygame")
            
        except Exception as e:
            log(f"✗ Original file pygame error: {e}")
        
        # Now test our temp file creation
        log("\n=== TEMP FILE CREATION TEST ===")
        
        # Use 20% through the file or 10 seconds, whichever is less
        target_time = min(10.0, original.length * 0.2)
        log(f"Target seeking position: {target_time:.2f}s")
        
        # Implement the fixed temp file creation
        temp_path = create_fixed_temp_file(original, target_time, test_file)
        
        if temp_path and os.path.exists(temp_path):
            log(f"\n=== TEMP FILE VERIFICATION ===")
            
            # Verify temp file
            temp_mid = mido.MidiFile(temp_path)
            log(f"✓ Temp file loads successfully")
            log(f"  Duration: {temp_mid.length:.3f} seconds")
            
            # Count temp file content
            temp_notes = 0
            for track in temp_mid.tracks:
                for msg in track:
                    if msg.type == 'note_on' and msg.velocity > 0:
                        temp_notes += 1
            log(f"  Notes in temp file: {temp_notes}")
            
            # Critical checks
            if temp_notes == 0:
                log("⚠ CRITICAL: Temp file has no notes!")
            
            if temp_mid.length < 0.1:
                log(f"⚠ CRITICAL: Temp file very short ({temp_mid.length:.3f}s)")
            
            # Test temp file with pygame
            log("\n=== TEMP FILE PYGAME TEST ===")
            try:
                pygame.mixer.music.load(temp_path)
                log("✓ pygame can load temp file")
                
                pygame.mixer.music.play()
                time.sleep(0.2)
                
                if pygame.mixer.music.get_busy():
                    log("✓ SUCCESS: Temp file plays correctly in pygame!")
                    pygame.mixer.music.stop()
                    
                    # Compare with original
                    log(f"\n=== COMPARISON ===")
                    log(f"Original: {original_notes} notes, {original.length:.2f}s")
                    log(f"Temp: {temp_notes} notes, {temp_mid.length:.3f}s")
                    log(f"Reduction: {((original_notes - temp_notes) / original_notes * 100):.1f}% notes")
                    
                    log("✓ TEMP FILE FIX SUCCESSFUL!")
                    
                else:
                    log("✗ FAILED: Temp file doesn't play in pygame")
                    log("This suggests the temp file is still malformed")
                
            except Exception as e:
                log(f"✗ Temp file pygame error: {e}")
            
            # Clean up
            os.unlink(temp_path)
            log("✓ Temp file cleaned up")
            
        else:
            log("✗ Temp file creation failed")
            return False
        
        log("\n=== TEST COMPLETE ===")
        return True
        
    except Exception as e:
        log(f"✗ Test failed with error: {e}")
        log("Traceback:")
        log(traceback.format_exc())
        return False

def create_fixed_temp_file(original_mid, start_time_seconds, original_filename):
    """Create a fixed temp MIDI file using the corrected logic"""
    
    import tempfile
    import mido
    
    log(f"Creating temp file starting at {start_time_seconds:.2f}s...")
    
    try:
        # Determine target tempo
        initial_tempo = 500000
        target_tempo = initial_tempo
        
        # Scan for tempo changes before target position
        current_time = 0.0
        current_tempo = initial_tempo
        
        for msg in original_mid.tracks[0]:
            if msg.time > 0:
                delta_time = mido.tick2second(msg.time, original_mid.ticks_per_beat, current_tempo)
                current_time += delta_time
            
            if msg.type == 'set_tempo':
                if current_time <= start_time_seconds:
                    current_tempo = msg.tempo
                    target_tempo = msg.tempo
                    log(f"  Found tempo change at {current_time:.2f}s: {60e6/msg.tempo:.1f} BPM")
                else:
                    break
        
        log(f"  Target tempo: {60e6/target_tempo:.1f} BPM")
        
        # Create new MIDI file
        new_mid = mido.MidiFile(ticks_per_beat=original_mid.ticks_per_beat, type=original_mid.type)
        
        total_messages = 0
        total_notes = 0
        
        for track_idx, track in enumerate(original_mid.tracks):
            new_track = mido.MidiTrack()
            current_time = 0.0
            current_tempo = initial_tempo
            first_message_added = False
            previous_temp_time = 0.0
            track_notes = 0
            track_messages = 0
            
            # Add initial tempo if needed
            if track_idx == 0 and target_tempo != initial_tempo:
                tempo_msg = mido.MetaMessage('set_tempo', tempo=target_tempo, time=0)
                new_track.append(tempo_msg)
                track_messages += 1
            
            for msg in track:
                # Update timing
                if msg.time > 0:
                    delta_time = mido.tick2second(msg.time, original_mid.ticks_per_beat, current_tempo)
                    current_time += delta_time
                
                if msg.type == 'set_tempo':
                    current_tempo = msg.tempo
                
                # Add messages at or after start time
                if current_time >= start_time_seconds:
                    if not first_message_added:
                        # First message starts immediately
                        adjusted_msg = msg.copy(time=0)
                        first_message_added = True
                        previous_temp_time = current_time
                        log(f"  Track {track_idx} first message: {msg.type} at {current_time:.3f}s")
                    else:
                        # Calculate proper delta time for temp file
                        temp_delta_seconds = current_time - previous_temp_time
                        
                        # Convert to ticks properly
                        if temp_delta_seconds > 0:
                            temp_delta_ticks = mido.second2tick(temp_delta_seconds, original_mid.ticks_per_beat, current_tempo)
                            # Ensure reasonable tick values
                            temp_delta_ticks = max(0, min(int(temp_delta_ticks), 2000))
                        else:
                            temp_delta_ticks = 0
                        
                        adjusted_msg = msg.copy(time=temp_delta_ticks)
                        previous_temp_time = current_time
                    
                    new_track.append(adjusted_msg)
                    track_messages += 1
                    
                    if msg.type == 'note_on' and msg.velocity > 0:
                        track_notes += 1
            
            # Ensure track has end_of_track
            if track_messages > 0:
                if not new_track or new_track[-1].type != 'end_of_track':
                    end_msg = mido.MetaMessage('end_of_track', time=0)
                    new_track.append(end_msg)
                    track_messages += 1
            
            new_mid.tracks.append(new_track)
            total_messages += track_messages
            total_notes += track_notes
            
            if track_notes > 0:
                log(f"  Track {track_idx}: {track_messages} messages, {track_notes} notes")
        
        log(f"  Total temp file: {total_messages} messages, {total_notes} notes")
        
        # Save temp file
        temp_fd, temp_path = tempfile.mkstemp(suffix='.mid', prefix='fixed_temp_')
        os.close(temp_fd)
        
        new_mid.save(temp_path)
        
        if os.path.exists(temp_path):
            file_size = os.path.getsize(temp_path)
            log(f"✓ Temp file saved: {temp_path} ({file_size} bytes)")
            return temp_path
        else:
            log("✗ Temp file was not created")
            return None
        
    except Exception as e:
        log(f"✗ Error creating temp file: {e}")
        log(traceback.format_exc())
        return None

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✓ Test completed successfully - check temp_fix_test_log.txt for details")
    else:
        print("\n✗ Test failed - check temp_fix_test_log.txt for details")
