"""
Test script to verify timing accuracy and arrow key navigation fixes
"""
import subprocess
import sys
import os

def test_main_app():
    """Test the main application with timing and navigation fixes"""
    print("=" * 60)
    print("TESTING MIDI GAPPER WITH TIMING AND NAVIGATION FIXES")
    print("=" * 60)
    
    print("\nKey Features to Test:")
    print("1. Load a MIDI file and start playback")
    print("2. Observe keyboard highlighting timing accuracy")
    print("3. Test arrow key navigation:")
    print("   - Up/Down arrows: Scroll visualization")
    print("   - Left/Right arrows: Seek backward/forward 1 second")
    print("   - Shift+Left/Right: Seek backward/forward 5 seconds")
    print("4. Test manual scrollbar position changes")
    print("5. Test seeking during playback")
    print("\nFixed Issues:")
    print("- Timing is now calculated from actual elapsed time (not incremental)")
    print("- Keyboard highlighting uses accurate audio position")
    print("- Arrow keys now support time-based navigation")
    print("- Update frequency increased to 50ms for smoother highlighting")
    
    print("\nStarting main application...")
    
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
    test_main_app()
