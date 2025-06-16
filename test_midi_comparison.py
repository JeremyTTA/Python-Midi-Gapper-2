#!/usr/bin/env python3
"""
Test script to compare original and saved MIDI files
"""
import mido
import sys
import os

def analyze_midi_file(filepath):
    """Analyze a MIDI file and return key information"""
    try:
        midi = mido.MidiFile(filepath)
        print(f"\n=== Analysis of {os.path.basename(filepath)} ===")
        print(f"Format: {midi.type}")
        print(f"Ticks per beat: {midi.ticks_per_beat}")
        print(f"Length in seconds: {midi.length:.3f}")
        print(f"Number of tracks: {len(midi.tracks)}")
        
        # Analyze each track
        for i, track in enumerate(midi.tracks):
            print(f"\nTrack {i} ({track.name or 'Unnamed'}):")
            print(f"  Messages: {len(track)}")
            
            # Count message types
            msg_types = {}
            tempo_changes = []
            notes = []
            current_time = 0
            current_tempo = 500000  # Default tempo
            
            for msg in track:
                current_time += mido.tick2second(msg.time, midi.ticks_per_beat, current_tempo)
                
                if msg.type not in msg_types:
                    msg_types[msg.type] = 0
                msg_types[msg.type] += 1
                
                if msg.type == 'set_tempo':
                    current_tempo = msg.tempo
                    bpm = round(60000000 / msg.tempo)
                    tempo_changes.append((current_time, bpm))
                    
                elif msg.type == 'note_on' and getattr(msg, 'velocity', 0) > 0:
                    notes.append((current_time, msg.note, msg.channel))
            
            # Show message type counts
            for msg_type, count in sorted(msg_types.items()):
                print(f"    {msg_type}: {count}")
            
            # Show tempo changes
            if tempo_changes:
                print(f"  Tempo changes: {len(tempo_changes)}")
                for time, bpm in tempo_changes[:5]:  # Show first 5
                    print(f"    {time:.3f}s: {bpm} BPM")
                if len(tempo_changes) > 5:
                    print(f"    ... and {len(tempo_changes) - 5} more")
            
            # Show first few notes
            if notes:
                print(f"  Notes: {len(notes)} total")
                for time, note, channel in notes[:3]:
                    print(f"    {time:.3f}s: Note {note} (Ch{channel})")
                if len(notes) > 3:
                    print(f"    ... and {len(notes) - 3} more")
        
        return midi
        
    except Exception as e:
        print(f"Error analyzing {filepath}: {e}")
        return None

def compare_midi_files(original_path, modified_path):
    """Compare two MIDI files"""
    print("=" * 60)
    print("MIDI FILE COMPARISON")
    print("=" * 60)
    
    orig = analyze_midi_file(original_path)
    mod = analyze_midi_file(modified_path)
    
    if orig and mod:
        print(f"\n=== COMPARISON SUMMARY ===")
        print(f"Format: {'SAME' if orig.type == mod.type else 'DIFFERENT'} ({orig.type} vs {mod.type})")
        print(f"Ticks per beat: {'SAME' if orig.ticks_per_beat == mod.ticks_per_beat else 'DIFFERENT'} ({orig.ticks_per_beat} vs {mod.ticks_per_beat})")
        print(f"Length: {'SAME' if abs(orig.length - mod.length) < 0.001 else 'DIFFERENT'} ({orig.length:.3f}s vs {mod.length:.3f}s)")
        print(f"Tracks: {'SAME' if len(orig.tracks) == len(mod.tracks) else 'DIFFERENT'} ({len(orig.tracks)} vs {len(mod.tracks)})")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        original = sys.argv[1]
        if len(sys.argv) >= 3:
            modified = sys.argv[2]
            compare_midi_files(original, modified)
        else:
            analyze_midi_file(original)
    else:
        print("Usage: python test_midi_comparison.py <original.mid> [modified.mid]")
        print("  With one file: analyze the file")
        print("  With two files: compare them")
