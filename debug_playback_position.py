#!/usr/bin/env python3
"""
Debug script to analyze the playback position calculation and tempo handling.
This will help identify why playback doesn't start at the correct position.
"""

import mido
import time
import os

def analyze_midi_timing(midi_file_path, target_position_seconds):
    """Analyze the MIDI file timing to understand the position calculation"""
    print(f"\n=== ANALYZING MIDI TIMING ===")
    print(f"File: {midi_file_path}")
    print(f"Target position: {target_position_seconds:.2f}s")
    
    try:
        mid = mido.MidiFile(midi_file_path)
        print(f"MIDI file info:")
        print(f"  - Type: {mid.type}")
        print(f"  - Ticks per beat: {mid.ticks_per_beat}")
        print(f"  - Number of tracks: {len(mid.tracks)}")
        
        # Analyze timing through the file
        total_analysis_time = 0.0
        initial_tempo = 500000  # Default MIDI tempo (120 BPM)
        
        print(f"\n=== TRACK ANALYSIS ===")
        
        for track_idx, track in enumerate(mid.tracks):
            print(f"\nTrack {track_idx}:")
            current_time = 0.0
            current_tempo = initial_tempo
            message_count = 0
            tempo_changes = []
            position_messages = []
            
            for msg in track:
                # Calculate timing for this message
                if msg.time > 0:
                    delta_time = mido.tick2second(msg.time, mid.ticks_per_beat, current_tempo)
                    current_time += delta_time
                
                # Track tempo changes
                if msg.type == 'set_tempo':
                    old_tempo = current_tempo
                    current_tempo = msg.tempo
                    tempo_changes.append({
                        'time': current_time,
                        'old_tempo': old_tempo,
                        'new_tempo': current_tempo,
                        'old_bpm': 60e6 / old_tempo,
                        'new_bpm': 60e6 / current_tempo
                    })
                
                # Track messages around our target position
                if abs(current_time - target_position_seconds) <= 2.0:  # Within 2 seconds
                    position_messages.append({
                        'time': current_time,
                        'msg_type': msg.type,
                        'msg_time_ticks': msg.time,
                        'msg_time_seconds': mido.tick2second(msg.time, mid.ticks_per_beat, current_tempo) if msg.time > 0 else 0
                    })
                
                message_count += 1
            
            print(f"  - Total messages: {message_count}")
            print(f"  - Total duration: {current_time:.2f}s")
            print(f"  - Tempo changes: {len(tempo_changes)}")
            
            if tempo_changes:
                print(f"  - Tempo changes in this track:")
                for tc in tempo_changes[:5]:  # Show first 5
                    print(f"    {tc['time']:.2f}s: {tc['old_bpm']:.1f} → {tc['new_bpm']:.1f} BPM")
                if len(tempo_changes) > 5:
                    print(f"    ... and {len(tempo_changes) - 5} more")
            
            if position_messages:
                print(f"  - Messages around target position ({target_position_seconds:.2f}s):")
                for pm in position_messages[:10]:  # Show first 10
                    print(f"    {pm['time']:.3f}s: {pm['msg_type']} (delta: {pm['msg_time_seconds']:.3f}s, {pm['msg_time_ticks']} ticks)")
                if len(position_messages) > 10:
                    print(f"    ... and {len(position_messages) - 10} more")
            
            total_analysis_time = max(total_analysis_time, current_time)
        
        print(f"\n=== SUMMARY ===")
        print(f"Total file duration: {total_analysis_time:.2f}s")
        print(f"Target position as percentage: {(target_position_seconds / total_analysis_time * 100):.1f}%")
        
        return total_analysis_time
        
    except Exception as e:
        print(f"Error analyzing MIDI file: {e}")
        return None

def test_temp_file_creation(midi_file_path, target_position_seconds):
    """Test the temporary file creation logic"""
    print(f"\n=== TESTING TEMP FILE CREATION ===")
    
    try:
        mid = mido.MidiFile(midi_file_path)
        initial_tempo = 500000
        
        print(f"Creating temp file for position {target_position_seconds:.2f}s")
        
        # Create a new MIDI file with the same properties
        new_mid = mido.MidiFile(ticks_per_beat=mid.ticks_per_beat, type=mid.type)
        
        # Process each track
        total_messages_original = 0
        total_messages_new = 0
        
        for track_idx, track in enumerate(mid.tracks):
            new_track = mido.MidiTrack()
            current_time = 0.0
            current_tempo = initial_tempo
            messages_added = 0
            messages_before_target = 0
            
            # Convert messages and track timing
            for msg in track:
                total_messages_original += 1
                
                # Update timing using current tempo
                if msg.time > 0:
                    delta_time = mido.tick2second(msg.time, mid.ticks_per_beat, current_tempo)
                    current_time += delta_time
                
                # Update tempo if this is a tempo change message
                if msg.type == 'set_tempo':
                    current_tempo = msg.tempo
                
                # Count messages before target
                if current_time < target_position_seconds:
                    messages_before_target += 1
                
                # If we've reached or passed the start time, add this message
                if current_time >= target_position_seconds:
                    # For the first message after start time, adjust timing
                    if len(new_track) == 0:
                        # Calculate how much to offset the first message
                        time_offset = current_time - target_position_seconds
                        # Convert back to ticks using current tempo
                        tick_offset = mido.second2tick(time_offset, mid.ticks_per_beat, current_tempo)
                        # Ensure we don't create negative time
                        new_time = max(0, msg.time - tick_offset)
                        adjusted_msg = msg.copy(time=new_time)
                        print(f"Track {track_idx}: First message at {current_time:.3f}s, offset by {time_offset:.3f}s")
                        print(f"  Original time: {msg.time} ticks, adjusted to: {new_time} ticks")
                    else:
                        # Keep original delta time for subsequent messages
                        adjusted_msg = msg.copy()
                    
                    new_track.append(adjusted_msg)
                    messages_added += 1
                    total_messages_new += 1
            
            # Add the track
            new_mid.tracks.append(new_track)
            print(f"Track {track_idx}: {messages_before_target} messages before target, {messages_added} messages added")
        
        print(f"Original file: {total_messages_original} messages")
        print(f"New file: {total_messages_new} messages")
        print(f"Reduction: {((total_messages_original - total_messages_new) / total_messages_original * 100):.1f}%")
        
        # Calculate expected duration of new file
        new_duration = 0.0
        for track in new_mid.tracks:
            track_time = 0.0
            current_tempo = initial_tempo
            for msg in track:
                if msg.time > 0:
                    delta_time = mido.tick2second(msg.time, mid.ticks_per_beat, current_tempo)
                    track_time += delta_time
                if msg.type == 'set_tempo':
                    current_tempo = msg.tempo
            new_duration = max(new_duration, track_time)
        
        print(f"Expected new file duration: {new_duration:.2f}s")
        
        return new_mid
        
    except Exception as e:
        print(f"Error testing temp file creation: {e}")
        return None

def main():
    # Test with a sample MIDI file from the workspace
    midi_files = []
    
    # Look for MIDI files in the workspace
    workspace_dir = r"g:\My Drive\Programming Projects\Player Piano\Jeremys Code\Python Midi Gapper 2"
    
    for file in os.listdir(workspace_dir):
        if file.lower().endswith(('.mid', '.midi')):
            midi_files.append(os.path.join(workspace_dir, file))
    
    if not midi_files:
        print("No MIDI files found in workspace. Looking for XML files to analyze...")
        for file in os.listdir(workspace_dir):
            if file.lower().endswith('.xml'):
                print(f"Found XML file: {file}")
        return
    
    print(f"Found MIDI files: {[os.path.basename(f) for f in midi_files]}")
    
    # Test with the first MIDI file
    test_file = midi_files[0]
    
    # Test different target positions
    test_positions = [5.0, 10.0, 30.0, 60.0]  # Test at 5s, 10s, 30s, 60s
    
    for pos in test_positions:
        duration = analyze_midi_timing(test_file, pos)
        if duration and pos < duration:
            print(f"\n" + "="*50)
            test_temp_file_creation(test_file, pos)
        else:
            print(f"Position {pos}s is beyond file duration ({duration:.2f}s)")

if __name__ == "__main__":
    main()
