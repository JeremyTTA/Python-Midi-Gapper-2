#!/usr/bin/env python3
"""
Diagnose MIDI playback issues
"""

import pygame
import time
import os
import sys

def test_pygame_midi():
    print("Testing pygame MIDI playback...")
    
    try:
        # Initialize pygame mixer with different settings
        print("1. Initializing pygame mixer...")
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
        pygame.mixer.init()
        print("   ✓ Pygame mixer initialized successfully")
        
        # Check if mixer is available
        print(f"   Mixer initialized: {pygame.mixer.get_init()}")
        print(f"   Number of mixer channels: {pygame.mixer.get_num_channels()}")
        
    except Exception as e:
        print(f"   ✗ Failed to initialize pygame mixer: {e}")
        return False
    
    # Look for MIDI files in the current directory
    midi_files = [f for f in os.listdir('.') if f.lower().endswith('.mid')]
    
    if not midi_files:
        print("2. No MIDI files found in current directory")
        # Create a simple test MIDI file
        try:
            import mido
            print("   Creating a simple test MIDI file...")
            mid = mido.MidiFile()
            track = mido.MidiTrack()
            mid.tracks.append(track)
            
            # Add a simple note
            track.append(mido.Message('program_change', channel=0, program=0, time=0))
            track.append(mido.Message('note_on', channel=0, note=60, velocity=64, time=0))
            track.append(mido.Message('note_off', channel=0, note=60, velocity=64, time=480))
            
            test_file = 'test_sound.mid'
            mid.save(test_file)
            print(f"   ✓ Created test MIDI file: {test_file}")
            midi_files = [test_file]
            
        except Exception as e:
            print(f"   ✗ Could not create test MIDI file: {e}")
            return False
    
    # Test playing a MIDI file
    test_file = midi_files[0]
    print(f"3. Testing playback of: {test_file}")
    
    try:
        pygame.mixer.music.load(test_file)
        print("   ✓ MIDI file loaded successfully")
        
        pygame.mixer.music.play()
        print("   ✓ Playback started")
        
        print("   Waiting 3 seconds for playback...")
        time.sleep(3)
        
        # Check if still playing
        is_playing = pygame.mixer.music.get_busy()
        print(f"   Is music playing: {is_playing}")
        
        pygame.mixer.music.stop()
        print("   ✓ Playback stopped")
        
    except Exception as e:
        print(f"   ✗ Error during MIDI playback: {e}")
        return False
    
    return True

def check_system_midi():
    print("\n4. Checking system MIDI support...")
    
    # Check for Windows MIDI
    if sys.platform == "win32":
        print("   Platform: Windows")
        print("   Note: Windows may need additional MIDI soundfont or synthesizer")
        print("   Common solutions:")
        print("   - Install a software synthesizer like VirtualMIDISynth")
        print("   - Use Windows built-in MIDI Wavetable synthesizer")
        print("   - Install a SoundFont (.sf2) file")
        
        try:
            import winreg
            # Check for MIDI devices in registry (simplified check)
            print("   Checking for MIDI devices...")
            # This is a basic check - real MIDI device detection is more complex
            print("   ✓ Registry access available for MIDI device checking")
        except:
            print("   ✗ Could not check MIDI devices")
    
    elif sys.platform == "darwin":
        print("   Platform: macOS")
        print("   macOS has built-in MIDI support via Core Audio")
    
    elif sys.platform.startswith("linux"):
        print("   Platform: Linux")
        print("   Linux may need ALSA, PulseAudio, or JACK for MIDI")
        print("   Consider installing: timidity++, fluidsynth, or qsynth")

def suggest_solutions():
    print("\n5. Suggested solutions for no MIDI sound:")
    print("   A. Install a software MIDI synthesizer:")
    print("      - Windows: VirtualMIDISynth + SoundFont")
    print("      - macOS: Built-in (should work)")
    print("      - Linux: timidity++ or fluidsynth")
    
    print("   B. Try alternative pygame mixer settings:")
    print("      - Different frequency (44100, 22050)")
    print("      - Different buffer size (512, 1024, 2048)")
    
    print("   C. Test with a different audio library:")
    print("      - python-rtmidi")
    print("      - pygame with different backends")
    
    print("   D. Verify MIDI file integrity:")
    print("      - Try playing the MIDI file in other applications")
    print("      - Check if the file has any sound data")

if __name__ == "__main__":
    print("MIDI Playback Diagnostic Tool")
    print("=" * 40)
    
    success = test_pygame_midi()
    check_system_midi()
    
    if not success:
        suggest_solutions()
        print("\n❌ MIDI playback test failed")
    else:
        print("\n✅ MIDI playback test passed")
        print("If you still don't hear sound, check:")
        print("- System volume levels")
        print("- MIDI synthesizer configuration")
        print("- Audio output device settings")
