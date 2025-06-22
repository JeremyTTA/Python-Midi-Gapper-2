#!/usr/bin/env python3
"""
Debug script to examine temporary MIDI files and diagnose playback issues
"""

import os
import sys

def debug_temp_midi_file():
    """Test and debug temporary MIDI file creation"""
    
    # Add the main directory to path to import the app
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, script_dir)
    
    try:
        import mido
        print("✓ mido library available")
    except ImportError:
        print("✗ mido library not available")
        return
    
    # Find a MIDI file to test with
    midi_files = [f for f in os.listdir('.') if f.endswith('.mid') or f.endswith('.midi')]
    
    if not midi_files:
        print("✗ No MIDI files found in current directory")
        return
    
    test_file = midi_files[0]
    print(f"Using test file: {test_file}")
    
    # Test loading the original file
    try:
        print(f"\n=== ORIGINAL FILE ANALYSIS ===")
        original = mido.MidiFile(test_file)
        print(f"✓ Loaded original file")
        print(f"  Tracks: {len(original.tracks)}")
        print(f"  Type: {original.type}")
        print(f"  Ticks per beat: {original.ticks_per_beat}")
        
        # Analyze tracks
        total_messages = 0
        for i, track in enumerate(original.tracks):
            note_on_count = sum(1 for msg in track if msg.type == 'note_on' and msg.velocity > 0)
            note_off_count = sum(1 for msg in track if msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0))
            tempo_count = sum(1 for msg in track if msg.type == 'set_tempo')
            total_messages += len(track)
            print(f"  Track {i}: {len(track)} messages, {note_on_count} note_on, {note_off_count} note_off, {tempo_count} tempo")
        
        print(f"  Total messages: {total_messages}")
        
        # Calculate total length
        length = original.length
        print(f"  Duration: {length:.2f} seconds")
        
    except Exception as e:
        print(f"✗ Error loading original file: {e}")
        return
    
    # Test creating a temp file at 30 seconds
    test_position = min(30.0, length * 0.5)  # Use 30s or halfway point
    print(f"\n=== TEMP FILE CREATION TEST ===")
    print(f"Creating temp file starting at {test_position:.2f}s...")
    
    try:
        # Simulate the temp file creation logic
        initial_tempo = 500000  # Default MIDI tempo
        target_tempo = initial_tempo
        
        # Scan for tempo changes
        current_time = 0.0
        current_tempo = initial_tempo
        for msg in original.tracks[0]:
            if msg.time > 0:
                delta_time = mido.tick2second(msg.time, original.ticks_per_beat, current_tempo)
                current_time += delta_time
            
            if msg.type == 'set_tempo':
                if current_time <= test_position:
                    current_tempo = msg.tempo
                    target_tempo = msg.tempo
                    print(f"  Found tempo at {current_time:.2f}s: {60e6/msg.tempo:.1f} BPM")
                else:
                    break
        
        print(f"  Target tempo: {60e6/target_tempo:.1f} BPM")
        
        # Create new MIDI file
        new_mid = mido.MidiFile(ticks_per_beat=original.ticks_per_beat, type=original.type)
        
        total_new_messages = 0
        note_messages_added = 0
        
        for track_idx, track in enumerate(original.tracks):
            new_track = mido.MidiTrack()
            current_time = 0.0
            current_tempo = initial_tempo
            messages_added = 0
            first_message_added = False
            
            # Add initial tempo if needed
            if track_idx == 0 and target_tempo != initial_tempo:
                tempo_msg = mido.MetaMessage('set_tempo', tempo=target_tempo, time=0)
                new_track.append(tempo_msg)
                messages_added += 1
            
            for msg in track:
                if msg.time > 0:
                    delta_time = mido.tick2second(msg.time, original.ticks_per_beat, current_tempo)
                    current_time += delta_time
                
                if msg.type == 'set_tempo':
                    current_tempo = msg.tempo
                
                # Add messages at or after the target position
                if current_time >= test_position:
                    if not first_message_added:
                        if msg.type in ['set_tempo', 'time_signature', 'key_signature', 'program_change']:
                            adjusted_msg = msg.copy(time=1)
                        else:
                            adjusted_msg = msg.copy(time=0)
                        first_message_added = True
                    else:
                        adjusted_msg = msg.copy()
                    
                    new_track.append(adjusted_msg)
                    messages_added += 1
                    
                    if msg.type in ['note_on', 'note_off']:
                        note_messages_added += 1
            
            new_mid.tracks.append(new_track)
            print(f"  Track {track_idx}: {messages_added} messages added")
            total_new_messages += messages_added
        
        print(f"  Total messages in temp file: {total_new_messages}")
        print(f"  Note messages in temp file: {note_messages_added}")
        
        # Save the temp file
        temp_path = "debug_temp.mid"
        new_mid.save(temp_path)
        
        if os.path.exists(temp_path):
            file_size = os.path.getsize(temp_path)
            print(f"✓ Temp file created: {file_size} bytes")
            
            # Try to reload and verify
            print(f"\n=== TEMP FILE VERIFICATION ===")
            temp_check = mido.MidiFile(temp_path)
            print(f"✓ Temp file can be reloaded")
            print(f"  Tracks: {len(temp_check.tracks)}")
            print(f"  Duration: {temp_check.length:.2f} seconds")
            
            # Check for actual note content
            total_notes = 0
            for track in temp_check.tracks:
                for msg in track:
                    if msg.type == 'note_on' and msg.velocity > 0:
                        total_notes += 1
            
            print(f"  Total note_on events: {total_notes}")
            
            if total_notes == 0:
                print("⚠ WARNING: Temp file has no note_on events!")
            
            # Test if pygame can load it
            print(f"\n=== PYGAME TEST ===")
            try:
                import pygame
                pygame.mixer.init()
                pygame.mixer.music.load(temp_path)
                print(f"✓ pygame can load temp file")
                
                # Try playing for a short time
                pygame.mixer.music.play()
                import time
                time.sleep(0.1)  # Let it start
                
                if pygame.mixer.music.get_busy():
                    print(f"✓ pygame is playing temp file")
                    pygame.mixer.music.stop()
                else:
                    print(f"⚠ pygame reports not playing (could be very short or no content)")
                
            except Exception as e:
                print(f"✗ pygame error: {e}")
            
            # Clean up
            os.unlink(temp_path)
            
        else:
            print(f"✗ Temp file was not created")
        
    except Exception as e:
        print(f"✗ Error in temp file creation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_temp_midi_file()
