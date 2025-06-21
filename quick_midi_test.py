#!/usr/bin/env python3
"""
Quick MIDI sound test
"""

import pygame
import time
import os

print("Quick MIDI Sound Test")
print("=" * 20)

try:
    # Initialize pygame mixer
    pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
    pygame.mixer.init()
    print("✓ Pygame mixer initialized")
    
    # Find a MIDI file
    midi_files = [f for f in os.listdir('.') if f.lower().endswith('.mid')]
    if midi_files:
        test_file = midi_files[0]
        print(f"✓ Testing with: {test_file}")
        
        # Try to play it
        pygame.mixer.music.load(test_file)
        pygame.mixer.music.play()
        print("✓ Playback started")
        
        # Quick test
        time.sleep(1)
        is_playing = pygame.mixer.music.get_busy()
        print(f"Is playing: {is_playing}")
        
        pygame.mixer.music.stop()
        
        if is_playing:
            print("✅ MIDI playback is working (check system volume/MIDI synth)")
        else:
            print("❌ MIDI playback failed - likely no MIDI synthesizer")
            
    else:
        print("❌ No MIDI files found")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\nOn Windows, you may need:")
print("1. A software MIDI synthesizer (VirtualMIDISynth)")
print("2. A SoundFont file (.sf2)")
print("3. Or use Windows built-in MIDI Wavetable Synth")
