#!/usr/bin/env python3
"""
Quick test of the MIDI player functionality
"""
import sys
import os

# Add the main directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    import mido
    print("Testing MIDI output...")
    
    # Test MIDI output availability
    output_names = mido.get_output_names()
    print(f"Available MIDI outputs: {output_names}")
    
    if not output_names:
        print("⚠ No MIDI output devices found")
        print("This might be why the play button doesn't work.")
        print("Solutions:")
        print("1. Install a virtual MIDI device (e.g., loopMIDI, Windows built-in)")
        print("2. Connect a MIDI device")
        print("3. Use a software synthesizer")
    else:
        print("✓ MIDI output devices available")
        
        # Test creating the note player
        try:
            from main import MidiNotePlayer
            player = MidiNotePlayer()
            if player.midi_out:
                print("✓ MidiNotePlayer created successfully")
                print("✓ MIDI output initialized")
                
                # Test a single note
                print("Testing note playback...")
                player._note_on(0, 60, 64)  # Middle C
                import time
                time.sleep(0.5)
                player._note_off(0, 60)
                print("✓ Note test completed")
                
                player.close()
            else:
                print("⚠ MidiNotePlayer created but no MIDI output")
        except Exception as e:
            print(f"✗ Error creating MidiNotePlayer: {e}")
            import traceback
            traceback.print_exc()

except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\nTest completed.")
