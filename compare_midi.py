#!/usr/bin/env python3
"""
Direct comparison tool for MIDI files
"""

import mido
import os

def compare_midi_files(original_file, reconstructed_file):
    """Compare two MIDI files and show differences"""
    print(f"=== Comparing MIDI Files ===")
    print(f"Original: {original_file}")
    print(f"Reconstructed: {reconstructed_file}")
    
    if not os.path.exists(original_file):
        print(f"ERROR: Original file {original_file} not found")
        return
    
    if not os.path.exists(reconstructed_file):
        print(f"ERROR: Reconstructed file {reconstructed_file} not found")
        return
    
    try:
        orig_midi = mido.MidiFile(original_file)
        recon_midi = mido.MidiFile(reconstructed_file)
        
        print(f"\nFile-level comparison:")
        print(f"  Ticks per beat: {orig_midi.ticks_per_beat} vs {recon_midi.ticks_per_beat}")
        print(f"  Track count: {len(orig_midi.tracks)} vs {len(recon_midi.tracks)}")
        
        if orig_midi.ticks_per_beat != recon_midi.ticks_per_beat:
            print("  ❌ MISMATCH: Ticks per beat differ")
        else:
            print("  ✅ Ticks per beat match")
            
        if len(orig_midi.tracks) != len(recon_midi.tracks):
            print("  ❌ MISMATCH: Track count differs")
        else:
            print("  ✅ Track count matches")
        
        # Compare each track
        for i, (orig_track, recon_track) in enumerate(zip(orig_midi.tracks, recon_midi.tracks)):
            print(f"\nTrack {i} comparison:")
            print(f"  Message count: {len(orig_track)} vs {len(recon_track)}")
            
            if len(orig_track) != len(recon_track):
                print("  ❌ MISMATCH: Message count differs")
            else:
                print("  ✅ Message count matches")
            
            # Compare first few messages
            print(f"  First 5 messages:")
            for j, (orig_msg, recon_msg) in enumerate(zip(orig_track[:5], recon_track[:5])):
                print(f"    Message {j}:")
                print(f"      Original:     {orig_msg}")
                print(f"      Reconstructed: {recon_msg}")
                
                if orig_msg.dict() == recon_msg.dict():
                    print(f"      ✅ Match")
                else:
                    print(f"      ❌ MISMATCH")
                    orig_dict = orig_msg.dict()
                    recon_dict = recon_msg.dict()
                    
                    for key in set(orig_dict.keys()) | set(recon_dict.keys()):
                        orig_val = orig_dict.get(key, '<missing>')
                        recon_val = recon_dict.get(key, '<missing>')
                        if orig_val != recon_val:
                            print(f"        {key}: {orig_val} → {recon_val}")
            
            # Check if track contains specific problematic message types
            orig_types = set(msg.type for msg in orig_track)
            recon_types = set(msg.type for msg in recon_track)
            
            if orig_types != recon_types:
                print(f"  ❌ MISMATCH: Message types differ")
                print(f"    Original types: {sorted(orig_types)}")
                print(f"    Reconstructed types: {sorted(recon_types)}")
                print(f"    Missing from reconstruction: {orig_types - recon_types}")
                print(f"    Extra in reconstruction: {recon_types - orig_types}")
            else:
                print(f"  ✅ Message types match: {sorted(orig_types)}")
        
        # Check for timing issues
        print(f"\nTiming analysis:")
        for i, (orig_track, recon_track) in enumerate(zip(orig_midi.tracks, recon_midi.tracks)):
            orig_times = [msg.time for msg in orig_track]
            recon_times = [msg.time for msg in recon_track]
            
            if orig_times != recon_times:
                print(f"  Track {i}: ❌ Timing differs")
                print(f"    Original first 10 times: {orig_times[:10]}")
                print(f"    Reconstructed first 10 times: {recon_times[:10]}")
            else:
                print(f"  Track {i}: ✅ Timing matches")
        
    except Exception as e:
        print(f"ERROR comparing files: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    # Look for MIDI files to compare
    midi_files = [f for f in os.listdir('.') if f.endswith('.mid') or f.endswith('.midi')]
    
    if len(midi_files) >= 2:
        orig_file = midi_files[0]
        modified_files = [f for f in midi_files if 'modified' in f.lower() or 'output' in f.lower()]
        
        if modified_files:
            recon_file = modified_files[0]
        else:
            recon_file = midi_files[1]
        
        compare_midi_files(orig_file, recon_file)
    else:
        print("Need at least 2 MIDI files to compare")
        print(f"Found files: {midi_files}")
