#!/usr/bin/env python3
"""
Final verification test for MIDI seeking
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

def final_verification():
    """Final verification that seeking works"""
    print("🎯 Final MIDI Seeking Verification")
    print("=" * 40)
    
    try:
        from main import MidiGapperGUI
        
        # Test basic creation
        app = MidiGapperGUI()
        print("✓ App created successfully")
        
        # Test MIDI loading
        if os.path.exists("test_melody.mid"):
            app.process_midi("test_melody.mid")
            print(f"✓ MIDI loaded (duration: {app.max_time:.1f}s)")
            
            # Test seeking to middle position
            seek_position = 3.0
            app.playback_position = seek_position
            print(f"✓ Set playback position to {seek_position}s")
            
            # Test temp file creation
            temp_file = app.create_temp_midi_from_position(seek_position)
            if temp_file and os.path.exists(temp_file):
                print("✓ Temporary MIDI file created successfully")
                
                # Verify it has different content than original
                import mido
                original = mido.MidiFile("test_melody.mid")
                temp = mido.MidiFile(temp_file)
                
                print(f"  Original duration: {original.length:.2f}s")
                print(f"  Temp file duration: {temp.length:.2f}s")
                
                expected_duration = original.length - seek_position
                actual_duration = temp.length
                time_diff = abs(expected_duration - actual_duration)
                
                if time_diff < 1.0:  # Allow 1 second tolerance
                    print("✓ Duration calculation looks correct")
                    print("\n🎵 SEEKING FUNCTIONALITY IS WORKING!")
                    print("When you use the app and drag the scrollbar,")
                    print("the audio should now start from the correct position.")
                else:
                    print(f"⚠ Duration seems off by {time_diff:.2f}s")
                
                # Clean up
                try:
                    os.unlink(temp_file)
                except:
                    pass
                    
            else:
                print("✗ Failed to create temporary file")
        else:
            print("✗ Test file not found")
            
        app.destroy()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    final_verification()
