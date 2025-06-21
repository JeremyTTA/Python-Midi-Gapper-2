#!/usr/bin/env python3
"""
Debug the MIDI file to understand the duration issue
"""
import mido

def debug_midi_file():
    """Debug the test MIDI file to understand why seeking is off"""
    
    test_file = "test_melody.mid"
    if not os.path.exists(test_file):
        print("Test file not found")
        return
    
    print(f"Debugging {test_file}")
    print("=" * 30)
    
    midi = mido.MidiFile(test_file)
    print(f"Type: {midi.type}")
    print(f"Ticks per beat: {midi.ticks_per_beat}")
    print(f"Length: {midi.length:.2f}s")
    print(f"Tracks: {len(midi.tracks)}")
    
    # Check each track
    for i, track in enumerate(midi.tracks):
        print(f"\nTrack {i}:")
        print(f"  Messages: {len(track)}")
        
        abs_time = 0
        note_count = 0
        
        for msg in track:
            abs_time += msg.time
            time_s = mido.tick2second(abs_time, midi.ticks_per_beat, 500000)
            
            if msg.type in ['note_on', 'note_off']:
                note_count += 1
                if note_count <= 5:  # Show first 5 notes
                    print(f"    {time_s:.2f}s: {msg}")
        
        print(f"  Total note events: {note_count}")
        track_length = mido.tick2second(abs_time, midi.ticks_per_beat, 500000)
        print(f"  Track duration: {track_length:.2f}s")

if __name__ == "__main__":
    import os
    debug_midi_file()
