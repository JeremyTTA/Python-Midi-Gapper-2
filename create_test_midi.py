#!/usr/bin/env python3
"""
Create a simple test MIDI file for testing playback
"""
import mido
import os

def create_test_midi():
    """Create a simple test MIDI file"""
    # Create a new MIDI file with one track
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # Add some basic settings
    track.append(mido.MetaMessage('set_tempo', tempo=500000))  # 120 BPM
    track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4))
    
    # Create a simple melody: C major scale going up and down
    notes = [60, 62, 64, 65, 67, 69, 71, 72, 71, 69, 67, 65, 64, 62, 60]  # C4 to C5 and back
    velocity = 64
    duration = 480  # quarter note at 480 ticks per beat
    
    # Add note events
    for note in notes:
        # Note on
        track.append(mido.Message('note_on', channel=0, note=note, velocity=velocity, time=0))
        # Note off after duration
        track.append(mido.Message('note_off', channel=0, note=note, velocity=velocity, time=duration))
    
    # Add end of track
    track.append(mido.MetaMessage('end_of_track', time=0))
    
    # Save the file
    filename = 'test_melody.mid'
    mid.save(filename)
    print(f"Created test MIDI file: {filename}")
    print(f"Duration: {mid.length:.2f} seconds")
    print(f"Tracks: {len(mid.tracks)}")
    
    return filename

def create_chord_progression():
    """Create a test MIDI file with chord progression"""
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # Add settings
    track.append(mido.MetaMessage('set_tempo', tempo=500000))  # 120 BPM
    
    # Chord progression: C - Am - F - G
    chords = [
        [60, 64, 67],  # C major (C-E-G)
        [57, 60, 64],  # A minor (A-C-E)
        [53, 57, 60],  # F major (F-A-C)
        [55, 59, 62],  # G major (G-B-D)
    ]
    
    velocity = 80
    chord_duration = 1920  # whole note
    
    for chord in chords:
        # Start all notes in chord
        for i, note in enumerate(chord):
            time = 0 if i == 0 else 0  # All notes start simultaneously
            track.append(mido.Message('note_on', channel=0, note=note, velocity=velocity, time=time))
        
        # End all notes in chord after duration
        for i, note in enumerate(chord):
            time = chord_duration if i == 0 else 0  # First note gets the duration
            track.append(mido.Message('note_off', channel=0, note=note, velocity=velocity, time=time))
    
    track.append(mido.MetaMessage('end_of_track', time=0))
    
    filename = 'test_chords.mid'
    mid.save(filename)
    print(f"Created chord progression MIDI file: {filename}")
    print(f"Duration: {mid.length:.2f} seconds")
    
    return filename

if __name__ == "__main__":
    print("Creating test MIDI files...")
    
    melody_file = create_test_midi()
    chord_file = create_chord_progression()
    
    print(f"\nTest files created:")
    print(f"1. {melody_file} - Simple melody")
    print(f"2. {chord_file} - Chord progression")
    print("\nYou can now load these files in the MIDI Gapper to test playback!")
