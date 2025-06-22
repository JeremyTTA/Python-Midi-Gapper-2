#!/usr/bin/env python3
"""
Simplified FluidSynth test to diagnose the string encoding issue
"""

import sys

try:
    import fluidsynth
    print("✓ FluidSynth imported successfully")
    
    # Test 1: Basic settings creation
    settings = fluidsynth.new_fluid_settings()
    if settings:
        print("✓ FluidSynth settings created")
        
        # Test 2: Try different string encoding approaches
        print("Testing string encoding methods...")
        
        # Method 1: Plain strings (this is causing the error)
        try:
            fluidsynth.fluid_settings_setnum(settings, 'synth.gain', 0.5)
            print("✓ Method 1 (plain strings) works")
        except Exception as e:
            print(f"✗ Method 1 failed: {e}")
        
        # Method 2: Byte strings
        try:
            fluidsynth.fluid_settings_setnum(settings, b'synth.sample-rate', 44100)
            print("✓ Method 2 (byte strings) works")
        except Exception as e:
            print(f"✗ Method 2 failed: {e}")
        
        # Method 3: ctypes c_char_p
        try:
            import ctypes
            key = ctypes.c_char_p(b'synth.polyphony')
            fluidsynth.fluid_settings_setint(settings, key, 256)
            print("✓ Method 3 (ctypes c_char_p) works")
        except Exception as e:
            print(f"✗ Method 3 failed: {e}")
        
        # Test 3: Synthesizer creation
        try:
            synth = fluidsynth.new_fluid_synth(settings)
            if synth:
                print("✓ Synthesizer created")
                
                # Test 4: Audio driver creation
                try:
                    audio_driver = fluidsynth.new_fluid_audio_driver(settings, synth)
                    if audio_driver:
                        print("✓ Audio driver created - FluidSynth is fully functional!")
                        fluidsynth.delete_fluid_audio_driver(audio_driver)
                    else:
                        print("✗ Audio driver creation failed")
                except Exception as e:
                    print(f"✗ Audio driver failed: {e}")
                
                fluidsynth.delete_fluid_synth(synth)
            else:
                print("✗ Synthesizer creation failed")
        except Exception as e:
            print(f"✗ Synthesizer creation error: {e}")
        
        fluidsynth.delete_fluid_settings(settings)
    else:
        print("✗ FluidSynth settings creation failed")

except ImportError:
    print("✗ FluidSynth not available")
except Exception as e:
    print(f"✗ FluidSynth error: {e}")

print("\n=== Test complete ===")
print("If all tests pass, FluidSynth should work properly in the main application.")
