"""
Quick test to verify keyboard highlighting during playback
"""
import subprocess
import sys
import os

def test_playback_highlighting():
    """Test keyboard highlighting during playback"""
    print("=" * 60)
    print("TESTING KEYBOARD HIGHLIGHTING DURING PLAYBACK")
    print("=" * 60)
    
    print("\nDEBUG VERSION ENABLED:")
    print("- Added debug prints to get_actual_audio_position()")
    print("- Added debug prints to update_keyboard_highlighting()")
    print("- Added debug prints to update_playback_timer()")
    
    print("\nTEST PROCEDURE:")
    print("1. Load a MIDI file (test_melody.mid or test_chords.mid)")
    print("2. Start playback from the beginning")
    print("3. Watch console output for debug messages")
    print("4. Observe keyboard highlighting")
    
    print("\nEXPECTED DEBUG OUTPUT:")
    print("- Timer messages every 50ms with position updates")
    print("- Audio position calculations")
    print("- Highlighting status with note counts")
    
    print("\nLOOK FOR THESE ISSUES:")
    print("- Timer not running (no timer debug messages)")
    print("- Audio position returning -1 (highlighting disabled)")
    print("- Notes found = 0 (no notes in time range)")
    print("- Missing keyboard_keys or keyboard_canvas")
    
    print("\nStarting main application with debug output...")
    
    try:
        # Get the directory containing this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_py_path = os.path.join(script_dir, "main.py")
        
        # Run the main application
        subprocess.run([sys.executable, main_py_path], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error running main application: {e}")
    except KeyboardInterrupt:
        print("\nApplication closed by user")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_playback_highlighting()
