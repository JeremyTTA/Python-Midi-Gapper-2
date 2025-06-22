#!/usr/bin/env python3
"""
Test the fixed temp MIDI file creation
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_temp_file_fix():
    """Test the fixed temp MIDI file creation logic"""
    
    print("=== TESTING TEMP MIDI FILE FIX ===")
    
    # Check for required modules
    try:
        import mido
        print(f"✓ mido available")
    except ImportError:
        print("✗ mido not available")
        return
    
    try:
        import pygame
        pygame.mixer.init()
        print(f"✓ pygame available and initialized")
    except ImportError:
        print("✗ pygame not available")
        return
    
    # Find a test MIDI file
    test_files = [f for f in os.listdir('.') if f.endswith(('.mid', '.midi'))]
    if not test_files:
        print("✗ No MIDI files found")
        return
    
    test_file = test_files[0]
    print(f"Using test file: {test_file}")
    
    # Load the test file
    try:
        mid = mido.MidiFile(test_file)
        print(f"✓ Loaded: {len(mid.tracks)} tracks, {mid.length:.2f}s duration")
    except Exception as e:
        print(f"✗ Error loading test file: {e}")
        return
    
    # Test the new temp file creation logic directly
    try:
        print(f"\n=== CREATING TEMP FILE ===")
        
        # Simulate creating temp file at 5 seconds (or 25% through the file)
        start_time_seconds = min(5.0, mid.length * 0.25)
        print(f"Target position: {start_time_seconds:.2f}s")
        
        # Simulate the fixed logic
        initial_tempo = 500000
        target_tempo = initial_tempo
        
        # Scan for tempo changes (simplified)
        current_time = 0.0
        current_tempo = initial_tempo
        for msg in mid.tracks[0]:
            if msg.time > 0:
                delta_time = mido.tick2second(msg.time, mid.ticks_per_beat, current_tempo)
                current_time += delta_time
            if msg.type == 'set_tempo':
                if current_time <= start_time_seconds:
                    current_tempo = msg.tempo
                    target_tempo = msg.tempo
                else:
                    break
        
        print(f"Target tempo: {60e6/target_tempo:.1f} BPM")
        
        # Create new MIDI file with fixed timing logic
        new_mid = mido.MidiFile(ticks_per_beat=mid.ticks_per_beat, type=mid.type)
        
        total_notes_added = 0
        total_messages_added = 0
        
        for track_idx, track in enumerate(mid.tracks):
            new_track = mido.MidiTrack()
            current_time = 0.0
            current_tempo = initial_tempo
            first_message_added = False
            previous_temp_time = 0.0
            notes_in_track = 0
            
            # Add initial tempo if needed
            if track_idx == 0 and target_tempo != initial_tempo:
                tempo_msg = mido.MetaMessage('set_tempo', tempo=target_tempo, time=0)
                new_track.append(tempo_msg)
                total_messages_added += 1
            
            for msg in track:
                # Update timing
                if msg.time > 0:
                    delta_time = mido.tick2second(msg.time, mid.ticks_per_beat, current_tempo)
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
                    else:
                        # Calculate proper delta time for temp file
                        temp_delta_seconds = current_time - previous_temp_time
                        temp_delta_ticks = mido.second2tick(temp_delta_seconds, mid.ticks_per_beat, current_tempo)
                        temp_delta_ticks = max(0, min(temp_delta_ticks, 1000))
                        
                        adjusted_msg = msg.copy(time=int(temp_delta_ticks))
                        previous_temp_time = current_time
                    
                    new_track.append(adjusted_msg)
                    total_messages_added += 1
                    
                    if msg.type == 'note_on' and msg.velocity > 0:
                        notes_in_track += 1
                        total_notes_added += 1
            
            # Add end_of_track if we added messages
            if len(new_track) > 0:
                if not new_track or new_track[-1].type != 'end_of_track':
                    end_msg = mido.MetaMessage('end_of_track', time=0)
                    new_track.append(end_msg)
                    total_messages_added += 1
            
            new_mid.tracks.append(new_track)
            if notes_in_track > 0:
                print(f"Track {track_idx}: {notes_in_track} notes added")
        
        print(f"Total: {total_messages_added} messages, {total_notes_added} notes")
        
        # Save and test the temp file
        temp_path = "test_temp_fix.mid"
        new_mid.save(temp_path)
        
        if os.path.exists(temp_path):
            file_size = os.path.getsize(temp_path)
            print(f"✓ Temp file saved: {file_size} bytes")
            
            # Verify it loads
            verify_mid = mido.MidiFile(temp_path)
            print(f"✓ Temp file verified: {verify_mid.length:.3f}s duration")
            
            if total_notes_added == 0:
                print(f"⚠ WARNING: No notes in temp file!")
            else:
                print(f"✓ Temp file contains {total_notes_added} notes")
            
            # Test pygame
            try:
                pygame.mixer.music.load(temp_path)
                print(f"✓ pygame can load temp file")
                
                pygame.mixer.music.play()
                import time
                time.sleep(0.1)
                
                if pygame.mixer.music.get_busy():
                    print(f"✓ pygame is playing temp file successfully!")
                    pygame.mixer.music.stop()
                else:
                    print(f"⚠ pygame reports not busy - checking file duration...")
                    if verify_mid.length < 0.1:
                        print(f"⚠ File too short: {verify_mid.length:.3f}s")
                    elif total_notes_added == 0:
                        print(f"⚠ File has no notes to play")
                    else:
                        print(f"⚠ Unknown issue with playback")
                
            except Exception as e:
                print(f"✗ pygame error: {e}")
            
            # Clean up
            os.unlink(temp_path)
            print(f"✓ Test temp file cleaned up")
        
    except Exception as e:
        print(f"✗ Error in temp file test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_temp_file_fix()
