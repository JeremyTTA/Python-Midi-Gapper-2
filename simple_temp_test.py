#!/usr/bin/env python3
"""
Simple test to verify temp MIDI file issue
"""

import os
import sys

def main():
    print("Starting temp MIDI debug...")
    
    # Check if we can import required modules
    try:
        import mido
        print(f"✓ mido available: {mido.__version__}")
    except ImportError as e:
        print(f"✗ mido not available: {e}")
        return
    
    try:
        import pygame
        print(f"✓ pygame available")
    except ImportError as e:
        print(f"✗ pygame not available: {e}")
        return
    
    # Find a test file
    test_files = [f for f in os.listdir('.') if f.endswith(('.mid', '.midi'))]
    if not test_files:
        print("✗ No MIDI files found")
        return
    
    test_file = test_files[0]
    print(f"Using test file: {test_file}")
    
    # Load and check the file
    try:
        mid = mido.MidiFile(test_file)
        print(f"✓ Loaded file: {len(mid.tracks)} tracks, duration {mid.length:.2f}s")
        
        # Count actual notes
        total_notes = 0
        for track in mid.tracks:
            for msg in track:
                if msg.type == 'note_on' and msg.velocity > 0:
                    total_notes += 1
        
        print(f"Total notes in original: {total_notes}")
        
        # Test seeking to 5 seconds
        seek_time = min(5.0, mid.length * 0.3)
        print(f"Testing seek to {seek_time:.2f}s...")
        
        # Create a very simple temp file - just copy everything after seek time
        new_mid = mido.MidiFile(ticks_per_beat=mid.ticks_per_beat)
        
        for track in mid.tracks:
            new_track = mido.MidiTrack()
            current_time = 0.0
            current_tempo = 500000
            first_added = False
            notes_added = 0
            
            for msg in track:
                if msg.time > 0:
                    delta_time = mido.tick2second(msg.time, mid.ticks_per_beat, current_tempo)
                    current_time += delta_time
                
                if msg.type == 'set_tempo':
                    current_tempo = msg.tempo
                
                if current_time >= seek_time:
                    if not first_added:
                        # First message gets time=0 to start immediately
                        new_msg = msg.copy(time=0)
                        first_added = True
                    else:
                        new_msg = msg.copy()
                    
                    new_track.append(new_msg)
                    
                    if msg.type == 'note_on' and msg.velocity > 0:
                        notes_added += 1
            
            new_mid.tracks.append(new_track)
            print(f"Track: {notes_added} notes added after {seek_time:.2f}s")
        
        # Save temp file
        temp_path = "simple_temp_test.mid"
        new_mid.save(temp_path)
        
        if os.path.exists(temp_path):
            size = os.path.getsize(temp_path)
            print(f"✓ Temp file created: {size} bytes")
            
            # Verify it can be loaded
            check_mid = mido.MidiFile(temp_path)
            print(f"✓ Temp file loadable: {check_mid.length:.2f}s duration")
            
            # Count notes in temp file
            temp_notes = 0
            for track in check_mid.tracks:
                for msg in track:
                    if msg.type == 'note_on' and msg.velocity > 0:
                        temp_notes += 1
            
            print(f"Notes in temp file: {temp_notes}")
            
            if temp_notes == 0:
                print("⚠ WARNING: No notes in temp file!")
            
            # Test pygame
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(temp_path)
                print("✓ pygame can load temp file")
                
                pygame.mixer.music.play()
                import time
                time.sleep(0.2)
                
                if pygame.mixer.music.get_busy():
                    print("✓ pygame is playing temp file")
                    pygame.mixer.music.stop()
                else:
                    print("⚠ pygame reports not busy - file may be empty or very short")
                
            except Exception as e:
                print(f"✗ pygame error: {e}")
            
            # Clean up
            os.unlink(temp_path)
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
