#!/usr/bin/env python3
"""
Test script to verify the duration calculation fix.
"""

import mido
import os

def test_duration_calculation(midi_file_path):
    """Test both the old (incorrect) and new (correct) duration calculation methods."""
    
    if not os.path.exists(midi_file_path):
        print(f"MIDI file not found: {midi_file_path}")
        return
    
    try:
        mf = mido.MidiFile(midi_file_path)
        print(f"\nTesting: {os.path.basename(midi_file_path)}")
        print(f"Ticks per beat: {mf.ticks_per_beat}")
        print(f"Number of tracks: {len(mf.tracks)}")
        
        # Method 1: OLD (incorrect) - treating msg.time as absolute time
        print("\n=== OLD METHOD (Incorrect) ===")
        old_notes = []
        old_active_on = {}
        
        for msg in mf:
            abs_time = msg.time  # WRONG: treating delta as absolute
            
            if hasattr(msg, 'channel') and hasattr(msg, 'note'):
                if msg.type == 'note_on' and getattr(msg, 'velocity', 0) > 0:
                    old_active_on[(msg.channel, msg.note)] = abs_time
                elif msg.type == 'note_off' or (msg.type == 'note_on' and getattr(msg, 'velocity', 0) == 0):
                    key = (msg.channel, msg.note)
                    if key in old_active_on:
                        start_time = old_active_on.pop(key)
                        duration = abs_time - start_time
                        old_notes.append((start_time, duration))
        
        old_max_time = max((start + dur for start, dur in old_notes), default=0)
        old_minutes = int(old_max_time // 60)
        old_seconds = int(old_max_time % 60)
        old_milliseconds = int((old_max_time % 1) * 1000)
        print(f"Old method duration: {old_max_time:.3f}s = {old_minutes}:{old_seconds:02d}.{old_milliseconds:03d}")
        
        # Method 2: NEW (correct) - accumulating delta times
        print("\n=== NEW METHOD (Correct) ===")
        new_notes = []
        new_active_on = {}
        abs_time = 0.0  # Accumulate delta times
        
        for msg in mf:
            abs_time += msg.time  # CORRECT: accumulate deltas
            
            if hasattr(msg, 'channel') and hasattr(msg, 'note'):
                if msg.type == 'note_on' and getattr(msg, 'velocity', 0) > 0:
                    new_active_on[(msg.channel, msg.note)] = abs_time
                elif msg.type == 'note_off' or (msg.type == 'note_on' and getattr(msg, 'velocity', 0) == 0):
                    key = (msg.channel, msg.note)
                    if key in new_active_on:
                        start_time = new_active_on.pop(key)
                        duration = abs_time - start_time
                        new_notes.append((start_time, duration))
        
        new_max_time = max((start + dur for start, dur in new_notes), default=abs_time)
        new_max_time = max(new_max_time, abs_time)  # Include total MIDI duration
        new_minutes = int(new_max_time // 60)
        new_seconds = int(new_max_time % 60)
        new_milliseconds = int((new_max_time % 1) * 1000)
        print(f"New method duration: {new_max_time:.3f}s = {new_minutes}:{new_seconds:02d}.{new_milliseconds:03d}")
        print(f"Total MIDI time: {abs_time:.3f}s")
        
        # Method 3: Use mido's built-in length calculation
        print("\n=== MIDO BUILT-IN ===")
        mido_length = mf.length
        mido_minutes = int(mido_length // 60)
        mido_seconds = int(mido_length % 60)
        mido_milliseconds = int((mido_length % 1) * 1000)
        print(f"Mido length: {mido_length:.3f}s = {mido_minutes}:{mido_seconds:02d}.{mido_milliseconds:03d}")
        
        print(f"\nProcessed {len(old_notes)} notes (old), {len(new_notes)} notes (new)")
        
        # Check if we have significant differences
        if abs(old_max_time - new_max_time) > 1.0:
            print(f"\n⚠️  SIGNIFICANT DIFFERENCE: {abs(old_max_time - new_max_time):.3f} seconds!")
            print("The fix should resolve this.")
        else:
            print("\nDifferences are minimal.")
        
    except Exception as e:
        print(f"Error processing {midi_file_path}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Test with any MIDI files in the current directory
    import glob
    
    midi_files = glob.glob("*.mid") + glob.glob("*.midi")
    
    if midi_files:
        print(f"Found {len(midi_files)} MIDI files to test:")
        for midi_file in midi_files:
            test_duration_calculation(midi_file)
    else:
        print("No MIDI files found in current directory.")
        print("Please add some MIDI files to test the duration calculation.")
