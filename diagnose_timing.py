#!/usr/bin/env python3
"""
Simple diagnostic for MIDI seeking timing
"""
import sys
import os
import mido

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

def diagnose_midi_timing():
    """Diagnose potential timing issues"""
    print("MIDI Timing Diagnostics")
    print("=" * 30)
    
    try:
        # Load test file
        test_file = "test_melody.mid"
        if not os.path.exists(test_file):
            print(f"Test file not found: {test_file}")
            return
        
        midi = mido.MidiFile(test_file)
        print(f"File: {test_file}")
        print(f"Type: {midi.type}")
        print(f"Ticks per beat: {midi.ticks_per_beat}")
        print(f"Total duration: {midi.length:.2f} seconds")
        print(f"Number of tracks: {len(midi.tracks)}")
        
        # Check for tempo changes
        tempo_changes = []
        for track_idx, track in enumerate(midi.tracks):
            abs_tick = 0
            for msg in track:
                abs_tick += msg.time
                if msg.is_meta and msg.type == 'set_tempo':
                    time_seconds = mido.tick2second(abs_tick, midi.ticks_per_beat, 500000)
                    tempo_changes.append((time_seconds, msg.tempo))
        
        print(f"\nTempo changes found: {len(tempo_changes)}")
        for time_s, tempo in tempo_changes[:5]:  # Show first 5
            bpm = 60_000_000 / tempo
            print(f"  {time_s:.2f}s: {bpm:.1f} BPM (tempo={tempo})")
        
        # Test seeking at a specific position
        test_position = 2.0
        print(f"\nTesting seeking to {test_position:.1f}s:")
        
        # Manual calculation of what should happen
        notes_before = []
        notes_after = []
        
        for track in midi.tracks:
            abs_tick = 0
            current_tempo = 500000
            
            for msg in track:
                abs_tick += msg.time
                
                # Update tempo if needed
                if msg.is_meta and msg.type == 'set_tempo':
                    current_tempo = msg.tempo
                
                # Convert to time
                time_s = mido.tick2second(abs_tick, midi.ticks_per_beat, current_tempo)
                
                if msg.type in ['note_on', 'note_off'] and msg.velocity > 0:
                    if time_s < test_position:
                        notes_before.append((time_s, msg.note, msg.type))
                    elif time_s >= test_position and len(notes_after) < 5:
                        notes_after.append((time_s, msg.note, msg.type))
        
        print(f"Last 3 notes before {test_position}s:")
        for time_s, note, msg_type in notes_before[-3:]:
            print(f"  {time_s:.2f}s: Note {note} {msg_type}")
        
        print(f"First 3 notes at/after {test_position}s:")
        for time_s, note, msg_type in notes_after[:3]:
            print(f"  {time_s:.2f}s: Note {note} {msg_type}")
        
        if notes_after:
            first_note_time = notes_after[0][0]
            expected_delay = first_note_time - test_position
            print(f"\nExpected: First note should play {expected_delay:.2f}s after seeking to {test_position}s")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnose_midi_timing()
