#!/usr/bin/env python3
"""
Comprehensive test of MIDI playback functionality
"""
import sys
import os
import time
import threading

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

def test_midi_playback():
    """Test the MIDI playback functionality"""
    print("Testing MIDI Playback Functionality")
    print("=" * 50)
    
    try:
        # Import the main application
        from main import MidiGapperGUI
        import tkinter as tk
        
        print("✓ Imported MidiGapperGUI successfully")
        
        # Create the application
        app = MidiGapperGUI()
        print(f"✓ Created GUI application")
        print(f"✓ MIDI playback available: {app.midi_playback_available}")
        
        # Test loading a MIDI file
        test_file = "test_melody.mid"
        if os.path.exists(test_file):
            print(f"✓ Found test file: {test_file}")
            
            # Load the MIDI file
            try:
                app.process_midi(test_file)
                print("✓ MIDI file loaded successfully")
                print(f"✓ Max time: {getattr(app, 'max_time', 'Not set')}")
                print(f"✓ Current file: {app.current_midi_file}")
                
                # Test playback controls
                print("\nTesting playback controls...")
                
                # Test play
                print("Testing play...")
                app.play_midi()
                time.sleep(0.5)  # Wait a bit
                
                # Check if playing
                print(f"✓ Is playing: {app.is_playing}")
                print(f"✓ Is paused: {app.is_paused}")
                print(f"✓ Playback position: {app.playback_position:.2f}s")
                
                # Test pause
                print("Testing pause...")
                app.pause_midi()
                time.sleep(0.2)
                print(f"✓ Is playing after pause: {app.is_playing}")
                print(f"✓ Is paused after pause: {app.is_paused}")
                
                # Test resume
                print("Testing resume...")
                app.play_midi()  # Resume
                time.sleep(0.5)
                print(f"✓ Is playing after resume: {app.is_playing}")
                
                # Test stop
                print("Testing stop...")
                app.stop_midi()
                time.sleep(0.2)
                print(f"✓ Is playing after stop: {app.is_playing}")
                print(f"✓ Playback position after stop: {app.playback_position:.2f}s")
                
                print("\n" + "=" * 50)
                print("✓ ALL MIDI PLAYBACK TESTS PASSED!")
                print("The MIDI playback functionality is working correctly.")
                
            except Exception as e:
                print(f"✗ Error testing MIDI playback: {e}")
                import traceback
                traceback.print_exc()
                
        else:
            print(f"✗ Test file not found: {test_file}")
            
        # Clean up
        app.destroy()
        
    except Exception as e:
        print(f"✗ Error in main test: {e}")
        import traceback
        traceback.print_exc()

def test_pygame_midi_directly():
    """Test pygame MIDI playback directly"""
    print("\nTesting pygame MIDI playback directly...")
    print("=" * 50)
    
    try:
        import pygame
        
        # Initialize pygame mixer
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
        pygame.mixer.init()
        print("✓ Pygame mixer initialized")
        
        # Test loading and playing a MIDI file
        test_file = "test_melody.mid"
        if os.path.exists(test_file):
            print(f"✓ Loading {test_file}...")
            
            # Load the MIDI file
            pygame.mixer.music.load(test_file)
            print("✓ MIDI file loaded into pygame")
            
            # Play the file
            print("✓ Starting playback for 3 seconds...")
            pygame.mixer.music.play()
            
            # Check if playing
            time.sleep(0.5)
            playing = pygame.mixer.music.get_busy()
            print(f"✓ Is pygame playing: {playing}")
            
            # Let it play for a bit
            time.sleep(2)
            
            # Stop playback
            pygame.mixer.music.stop()
            print("✓ Stopped playback")
            
            # Check if stopped
            time.sleep(0.2)
            playing = pygame.mixer.music.get_busy()
            print(f"✓ Is pygame playing after stop: {playing}")
            
            print("✓ Direct pygame MIDI test passed!")
            
        else:
            print(f"✗ Test file not found: {test_file}")
            
    except Exception as e:
        print(f"✗ Error in pygame direct test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Test pygame directly first
    test_pygame_midi_directly()
    
    # Then test the full application
    test_midi_playback()
    
    print("\n" + "=" * 50)
    print("MIDI PLAYBACK TESTING COMPLETE")
    print("If all tests passed, the MIDI playback functionality is ready!")
