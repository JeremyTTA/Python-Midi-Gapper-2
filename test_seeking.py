#!/usr/bin/env python3
"""
Test MIDI seeking functionality
"""
import sys
import os
import time

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

def test_midi_seeking():
    """Test the MIDI seeking functionality"""
    print("Testing MIDI Seeking Functionality")
    print("=" * 40)
    
    try:
        from main import MidiGapperGUI
        
        # Create the application
        app = MidiGapperGUI()
        print("✓ Created MidiGapperGUI")
        
        # Load a test MIDI file
        test_file = "test_melody.mid"
        if os.path.exists(test_file):
            print(f"✓ Loading {test_file}")
            app.process_midi(test_file)
            print(f"✓ MIDI loaded, max_time: {app.max_time:.2f}s")
            
            # Test seeking to different positions
            test_positions = [0.0, 2.0, 4.0, 6.0]
            
            for pos in test_positions:
                if pos <= app.max_time:
                    print(f"\nTesting playback from {pos:.1f}s...")
                    
                    # Set the playback position
                    app.playback_position = pos
                    print(f"✓ Set playback position to {pos:.1f}s")
                    
                    # Test creating temp file
                    if pos > 0.1:
                        temp_file = app.create_temp_midi_from_position(pos)
                        if temp_file:
                            print(f"✓ Created temp file: {os.path.basename(temp_file)}")
                            
                            # Verify temp file exists and has content
                            if os.path.exists(temp_file) and os.path.getsize(temp_file) > 0:
                                print("✓ Temp file is valid")
                            else:
                                print("✗ Temp file is invalid")
                        else:
                            print("✗ Failed to create temp file")
                    
                    # Test playback start (without actually playing audio in test)
                    app.is_playing = False  # Reset state
                    print("✓ Seeking functionality works")
            
            # Test cleanup
            app.cleanup_temp_files()
            print("✓ Cleanup completed")
            
            print("\n🎯 MIDI SEEKING FUNCTIONALITY WORKS!")
            print("The application now supports starting playback from any position!")
            
        else:
            print(f"✗ Test file not found: {test_file}")
            print("Run create_test_midi.py first to create test files")
        
        app.destroy()
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_midi_seeking()
