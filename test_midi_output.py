#!/usr/bin/env python3
"""Test MIDI output capabilities"""

import mido
import time

def test_midi_output():
    """Test if MIDI output is working"""
    print("Testing MIDI output...")
    
    try:
        # Check available MIDI outputs
        output_names = mido.get_output_names()
        print(f"Available MIDI output devices: {output_names}")
        
        if not output_names:
            print("\n⚠ No MIDI output devices found!")
            print("To hear MIDI audio, you need to:")
            print("1. Install a virtual MIDI device (recommended: loopMIDI)")
            print("2. Download from: https://www.tobias-erichsen.de/software/loopmidi.html")
            print("3. Create a virtual MIDI port")
            print("4. Connect it to a software synthesizer (like Windows Media Player, VirtualMIDISynth, or FluidSynth)")
            return False
        
        # Try to open the first available output
        print(f"\nTrying to open: {output_names[0]}")
        with mido.open_output(output_names[0]) as outport:
            print(f"✓ Successfully opened MIDI output: {output_names[0]}")
            
            # Test playing a simple note
            print("Playing test note (C4)...")
            
            # Note on
            note_on = mido.Message('note_on', channel=0, note=60, velocity=64)
            outport.send(note_on)
            print("Note ON sent")
            
            time.sleep(1)
            
            # Note off
            note_off = mido.Message('note_off', channel=0, note=60, velocity=0)
            outport.send(note_off)
            print("Note OFF sent")
            
            print("✓ MIDI test completed successfully!")
            return True
            
    except Exception as e:
        print(f"✗ MIDI test failed: {e}")
        if "No module named 'rtmidi'" in str(e):
            print("The python-rtmidi package is not installed.")
            print("Install it with: pip install python-rtmidi")
        return False

if __name__ == "__main__":
    test_midi_output()
    input("\nPress Enter to exit...")
