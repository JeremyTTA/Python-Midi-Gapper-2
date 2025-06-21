#!/usr/bin/env python3
"""
Test MIDI timing accuracy
"""
import sys
import os
import mido

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

def test_timing_accuracy():
    """Test if the timing calculations are accurate"""
    print("Testing MIDI Timing Accuracy")
    print("=" * 40)
    
    try:
        # Load test file
        test_file = "test_melody.mid"
        if not os.path.exists(test_file):
            print(f"Test file not found: {test_file}")
            return
        
        midi = mido.MidiFile(test_file)
        print(f"Original MIDI: {midi.length:.2f} seconds")
        
        # Test at different positions
        test_positions = [0.0, 1.0, 2.0, 3.0]
        
        for start_time in test_positions:
            if start_time >= midi.length:
                continue
                
            print(f"\nTesting position {start_time:.1f}s:")
            
            # Create new MIDI from position using improved method
            new_midi = mido.MidiFile(ticks_per_beat=midi.ticks_per_beat)
            
            for track_idx, track in enumerate(midi.tracks):
                new_track = mido.MidiTrack()
                
                # Convert to absolute time and filter
                abs_time = 0
                for msg in track:
                    abs_time += msg.time
                    abs_time_seconds = mido.tick2second(abs_time, midi.ticks_per_beat, 500000)
                    
                    if abs_time_seconds >= start_time:
                        new_msg = msg.copy()
                        if new_track:  # Not first message
                            # Keep relative timing
                            pass
                        else:  # First message
                            new_msg.time = 0
                        new_track.append(new_msg)
                
                # Add end of track
                if not new_track or new_track[-1].type != 'end_of_track':
                    new_track.append(mido.MetaMessage('end_of_track', time=0))
                
                new_midi.tracks.append(new_track)
            
            expected_duration = midi.length - start_time
            actual_duration = new_midi.length
            
            print(f"  Expected duration: {expected_duration:.2f}s")
            print(f"  Actual duration: {actual_duration:.2f}s")
            print(f"  Difference: {abs(expected_duration - actual_duration):.2f}s")
            
            if abs(expected_duration - actual_duration) < 0.5:  # Allow 0.5s tolerance
                print("  ✓ Timing looks good")
            else:
                print("  ✗ Timing seems off")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_timing_accuracy()
