#!/usr/bin/env python3
"""
Comprehensive MIDI seeking test with audio playback
"""
import sys
import os
import time

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

def test_seeking_with_audio():
    """Test MIDI seeking with actual audio playback"""
    print("🎵 MIDI Seeking Test with Audio Playback")
    print("=" * 50)
    
    try:
        from main import MidiGapperGUI
        
        # Create app and load test file
        app = MidiGapperGUI()
        test_file = "test_melody.mid"
        
        if not os.path.exists(test_file):
            print(f"Test file not found: {test_file}")
            print("Run: python create_test_midi.py")
            return
        
        app.process_midi(test_file)
        print(f"✓ Loaded {test_file} (duration: {app.max_time:.1f}s)")
        
        # Test positions to try
        test_positions = [0.0, 2.0, 4.0]
        
        for pos in test_positions:
            if pos >= app.max_time:
                continue
                
            print(f"\n🎯 Testing playback from {pos:.1f}s")
            print("   (You should hear audio starting from this position)")
            
            # Set position and play
            app.playback_position = pos
            
            # Create temp file manually to test
            temp_file = app.create_temp_midi_from_position(pos)
            if temp_file:
                print(f"   ✓ Created temp file: {os.path.basename(temp_file)}")
                
                # Test playing the temp file directly
                try:
                    import pygame
                    pygame.mixer.music.load(temp_file)
                    pygame.mixer.music.play()
                    
                    print(f"   ▶ Playing for 3 seconds...")
                    time.sleep(3)
                    
                    pygame.mixer.music.stop()
                    print(f"   ⏹ Stopped")
                    
                except Exception as e:
                    print(f"   ✗ Playback error: {e}")
                
                # Clean up this temp file
                try:
                    os.unlink(temp_file)
                except:
                    pass
            else:
                print("   ✗ Failed to create temp file")
            
            time.sleep(1)  # Brief pause between tests
        
        print(f"\n🏁 Test complete!")
        print(f"Did the audio start from the correct positions?")
        print(f"- Position 0s should start with the beginning of the melody")
        print(f"- Position 2s should start partway through")
        print(f"- Position 4s should start even later in the melody")
        
        app.destroy()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_seeking_with_audio()
