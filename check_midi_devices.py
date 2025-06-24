#!/usr/bin/env python3
"""Check available MIDI devices on Windows"""

import mido
import sys

def check_midi_devices():
    print("🔍 MIDI Device Checker")
    print("=" * 40)
    
    try:
        print(f"✓ Mido version: {mido.__version__}")
        print(f"✓ MIDI backend: {mido.backend}")
        
        # Get available devices
        outputs = mido.get_output_names()
        inputs = mido.get_input_names()
        
        print(f"\n📤 MIDI Output Devices ({len(outputs)}):")
        if outputs:
            for i, device in enumerate(outputs):
                print(f"  {i+1}. {device}")
        else:
            print("  ❌ No MIDI output devices found")
            
        print(f"\n📥 MIDI Input Devices ({len(inputs)}):")
        if inputs:
            for i, device in enumerate(inputs):
                print(f"  {i+1}. {device}")
        else:
            print("  ❌ No MIDI input devices found")
            
        # Check Windows-specific devices
        print(f"\n🪟 Windows MIDI Notes:")
        print("  • Windows usually has a built-in 'Microsoft GS Wavetable Synth'")
        print("  • If no devices are shown, try installing loopMIDI:")
        print("    https://www.tobias-erichsen.de/software/loopmidi.html")
        print("  • After installing loopMIDI, create a virtual MIDI port")
        print("  • Then install VirtualMIDISynth or use Windows built-in synth")
        
        return len(outputs) > 0
        
    except ImportError as e:
        print(f"❌ MIDI backend not available: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking MIDI devices: {e}")
        return False

if __name__ == "__main__":
    has_output = check_midi_devices()
    print(f"\n🎵 MIDI Output Available: {'✓ YES' if has_output else '❌ NO'}")
    print("=" * 40)
    
    if not has_output:
        print("\n💡 To get MIDI audio working:")
        print("1. Download loopMIDI: https://www.tobias-erichsen.de/software/loopmidi.html")
        print("2. Install it and create a virtual MIDI port")
        print("3. Download VirtualMIDISynth for high-quality audio")
        print("4. Restart this application")
        print("\n🔄 After setup, the visualization will play with audio!")
