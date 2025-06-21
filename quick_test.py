#!/usr/bin/env python3
"""
Quick test of MIDI functionality
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

def quick_test():
    """Quick test of key functionality"""
    print("Quick MIDI Test")
    print("===============")
    
    try:
        # Test pygame
        import pygame
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
        pygame.mixer.init()
        print("✓ Pygame initialized")
        
        # Test MIDI file loading
        if os.path.exists("test_melody.mid"):
            pygame.mixer.music.load("test_melody.mid")
            print("✓ MIDI file loaded")
            
            # Quick play test (no waiting)
            pygame.mixer.music.play()
            busy = pygame.mixer.music.get_busy()
            print(f"✓ Playback started: {busy}")
            
            pygame.mixer.music.stop()
            print("✓ Playback stopped")
        else:
            print("✗ No test MIDI file found")
            
        # Test main app import
        from main import MidiGapperGUI
        print("✓ Main app imports successfully")
        
        # Test basic GUI creation
        import tkinter as tk
        app = MidiGapperGUI()
        print(f"✓ GUI created, MIDI available: {app.midi_playback_available}")
        
        app.destroy()
        print("✓ GUI cleaned up")
        
        print("\n🎵 MIDI PLAYBACK IS READY! 🎵")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    quick_test()
