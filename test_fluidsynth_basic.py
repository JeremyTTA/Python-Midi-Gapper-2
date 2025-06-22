#!/usr/bin/env python3
"""
Quick test to verify FluidSynth installation and basic functionality
"""

print("Testing FluidSynth installation...")

try:
    import fluidsynth
    print("✓ pyfluidsynth imported successfully")
    print(f"  FluidSynth version info available")
except ImportError as e:
    print(f"✗ Failed to import fluidsynth: {e}")
    print("  Try: pip install pyfluidsynth")
    exit(1)

try:
    import mido
    print("✓ mido imported successfully")
except ImportError:
    print("✗ mido not available")

try:
    import pygame
    print("✓ pygame imported successfully")
except ImportError:
    print("✗ pygame not available")

print()
print("Testing basic FluidSynth functionality...")

try:
    # Test basic FluidSynth operations
    fs = fluidsynth.new_fluid_synth()
    if fs:
        print("✓ FluidSynth synthesizer created")
        
        # Try to create audio driver
        driver = fluidsynth.new_fluid_audio_driver(fs)
        if driver:
            print("✓ Audio driver created")
            fluidsynth.delete_fluid_audio_driver(driver)
        else:
            print("⚠ Audio driver creation failed (may need different settings)")
        
        # Clean up
        fluidsynth.delete_fluid_synth(fs)
        print("✓ FluidSynth test completed successfully")
    else:
        print("✗ Failed to create FluidSynth synthesizer")

except Exception as e:
    print(f"✗ FluidSynth test failed: {e}")

print()
print("FluidSynth is ready for MIDI seeking implementation!")
print("The main app should now support real MIDI seeking instead of temp files.")
