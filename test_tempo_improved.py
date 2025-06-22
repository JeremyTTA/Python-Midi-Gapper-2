#!/usr/bin/env python3
"""
Test script to verify the improved tempo handling for temporary MIDI files.
"""

import sys
import os

# Add the current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def test_tempo_conversion():
    """Test the improved tempo conversion and temp file creation"""
    try:
        import tkinter as tk
        from main import MidiGapperGUI
        import mido
        
        print("Testing improved tempo handling...")
        
        # Create a minimal tkinter setup
        root = tk.Tk()
        root.withdraw()
        
        app = MidiGapperGUI(root)
        
        # Check if we have a MIDI file available for testing
        midi_files = [f for f in os.listdir('.') if f.endswith(('.mid', '.midi'))]
        if not midi_files:
            print("No MIDI files found for testing")
            return False
        
        test_file = midi_files[0]
        print(f"Using test file: {test_file}")
        
        # Set up the app with the test file
        app.current_midi_file = os.path.abspath(test_file)
        
        # Test seconds to ticks conversion
        print("\nTesting _seconds_to_ticks conversion:")
        test_times = [0.0, 2.0, 5.0, 10.0]
        for seconds in test_times:
            try:
                ticks = app._seconds_to_ticks(seconds)
                print(f"  {seconds:.1f}s → {ticks} ticks")
            except Exception as e:
                print(f"  Error converting {seconds}s: {e}")
        
        # Test temp file creation
        print("\nTesting temp file creation:")
        try:
            temp_file = app.create_temp_midi_from_position(5.0)
            if temp_file and os.path.exists(temp_file):
                print(f"✓ Successfully created temp file: {temp_file}")
                
                # Check the temp file properties
                original_midi = mido.MidiFile(app.current_midi_file)
                temp_midi = mido.MidiFile(temp_file)
                
                print(f"  Original: {len(original_midi.tracks)} tracks, {original_midi.ticks_per_beat} TPB")
                print(f"  Temp: {len(temp_midi.tracks)} tracks, {temp_midi.ticks_per_beat} TPB")
                
                # Check if tempo is set correctly in the temp file
                for track_idx, track in enumerate(temp_midi.tracks):
                    for msg_idx, msg in enumerate(track):
                        if msg.type == 'set_tempo':
                            tempo_bpm = mido.tempo2bpm(msg.tempo)
                            print(f"  Tempo in temp file track {track_idx}: {tempo_bpm:.1f} BPM (at time {msg.time})")
                            break
                
                # Clean up
                try:
                    os.unlink(temp_file)
                    print("  ✓ Cleaned up temp file")
                except:
                    pass
                
                return True
            else:
                print("✗ Failed to create temp file")
                return False
                
        except Exception as e:
            print(f"✗ Error creating temp file: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            root.destroy()
        except:
            pass

if __name__ == "__main__":
    success = test_tempo_conversion()
    if success:
        print("\n✓ Tempo handling test passed")
    else:
        print("\n✗ Tempo handling test failed")
