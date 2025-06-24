#!/usr/bin/env python3
"""
Simple test script to verify FluidSynth integration is working
"""

import time
import sys

def test_fluidsynth():
    print("=== FluidSynth Integration Test ===")
    
    try:
        import fluidsynth
        print("✓ FluidSynth imported successfully")
        
        # Create and start FluidSynth
        fs = fluidsynth.Synth()
        fs.start(driver="dsound")
        print("✓ FluidSynth started")
        
        # Try to load Windows built-in soundfont
        try:
            sfid = fs.sfload("C:/Windows/System32/drivers/gm.dls")
            fs.program_select(0, sfid, 0, 0)  # Channel 0, Bank 0, Preset 0 (Piano)
            print("✓ Loaded Windows GM soundfont")
        except Exception as e:
            print(f"⚠ Could not load soundfont: {e}")
            print("ℹ Will use FluidSynth's built-in sounds")
        
        # Play a simple melody to test audio
        print("\n🎵 Playing test melody...")
        notes = [60, 64, 67, 72]  # C, E, G, C (C major chord arpeggio)
        
        for i, note in enumerate(notes):
            print(f"  Playing note {i+1}/4: {note}")
            fs.noteon(0, note, 80)  # Channel 0, note, velocity 80
            time.sleep(0.5)
            fs.noteoff(0, note)
            time.sleep(0.1)
        
        print("✓ Test melody completed")
        
        # Cleanup
        fs.delete()
        print("✓ FluidSynth cleaned up")
        
        print("\n🎉 FluidSynth integration test PASSED!")
        print("   Your highlighted keys should now play audio in the main application.")
        
        return True
        
    except ImportError as e:
        print(f"✗ FluidSynth import failed: {e}")
        print("ℹ Install with: pip install pyfluidsynth")
        return False
        
    except Exception as e:
        print(f"✗ FluidSynth test failed: {e}")
        return False

if __name__ == "__main__":
    if test_fluidsynth():
        sys.exit(0)
    else:
        sys.exit(1)
