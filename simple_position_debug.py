#!/usr/bin/env python3
"""
Simple test to understand the position calculation issue
"""

import os
import sys

def check_files():
    workspace_dir = r"g:\My Drive\Programming Projects\Player Piano\Jeremys Code\Python Midi Gapper 2"
    print(f"Working directory: {workspace_dir}")
    print(f"Files in directory:")
    
    try:
        files = os.listdir(workspace_dir)
        midi_files = [f for f in files if f.lower().endswith(('.mid', '.midi'))]
        
        print(f"All files ({len(files)}):")
        for f in sorted(files):
            print(f"  {f}")
        
        print(f"\nMIDI files ({len(midi_files)}):")
        for f in midi_files:
            print(f"  {f}")
            
        return midi_files
    except Exception as e:
        print(f"Error listing files: {e}")
        return []

def test_mido():
    print("\n=== Testing mido library ===")
    try:
        import mido
        print("mido imported successfully")
        
        midi_files = check_files()
        if midi_files:
            test_file = midi_files[0]
            print(f"Testing with: {test_file}")
            
            try:
                mid = mido.MidiFile(test_file)
                print(f"Successfully loaded MIDI file")
                print(f"  Type: {mid.type}")
                print(f"  Ticks per beat: {mid.ticks_per_beat}")
                print(f"  Number of tracks: {len(mid.tracks)}")
                
                # Calculate duration
                total_time = 0.0
                tempo = 500000  # Default tempo
                
                for track in mid.tracks:
                    track_time = 0.0
                    current_tempo = tempo
                    for msg in track:
                        if msg.time > 0:
                            delta_time = mido.tick2second(msg.time, mid.ticks_per_beat, current_tempo)
                            track_time += delta_time
                        if msg.type == 'set_tempo':
                            current_tempo = msg.tempo
                    total_time = max(total_time, track_time)
                
                print(f"  Duration: {total_time:.2f} seconds")
                
                return True, test_file, total_time
                
            except Exception as e:
                print(f"Error loading MIDI file {test_file}: {e}")
                
        else:
            print("No MIDI files found to test")
            
    except ImportError:
        print("mido library not available")
        return False, None, 0
    except Exception as e:
        print(f"Error with mido: {e}")
        return False, None, 0
    
    return False, None, 0

def analyze_position_calculation():
    print("\n=== Analyzing position calculation logic ===")
    
    # Simulate the current logic from main.py
    max_time = 120.0  # Example: 2 minute file
    
    # Test different scroll positions
    test_scroll_positions = [
        (0.0, 1.0),   # At bottom (should be time=0)
        (0.0, 0.5),   # Middle (should be time=60)
        (0.0, 0.0),   # At top (should be time=120)
        (0.5, 1.0),   # Bottom half visible (should be time=0)
        (0.25, 0.75), # Middle section (should be time=30)
    ]
    
    print("Current calculation: time_position = (1.0 - scroll_bottom) * max_time")
    print(f"Max time: {max_time}s")
    print("\nScroll position → Calculated time:")
    
    for scroll_top, scroll_bottom in test_scroll_positions:
        time_position = (1.0 - scroll_bottom) * max_time
        print(f"  scroll_bottom={scroll_bottom:.2f} → time={time_position:.1f}s")
    
    print("\nThis shows the current calculation logic.")

if __name__ == "__main__":
    print("=== PLAYBACK POSITION DEBUG ===")
    
    check_files()
    mido_ok, test_file, duration = test_mido()
    analyze_position_calculation()
    
    if mido_ok:
        print(f"\n=== Analysis complete ===")
        print(f"Test file: {test_file}")
        print(f"Duration: {duration:.2f}s")
        print("mido library is working correctly")
    else:
        print("\n=== Issues found ===")
        print("mido library issues - temp file creation may fail")
