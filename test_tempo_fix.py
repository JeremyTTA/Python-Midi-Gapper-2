"""
Test script to verify the global tempo handling fix
"""
import subprocess
import sys
import os

def test_tempo_fix():
    """Test the tempo handling fix"""
    print("=" * 60)
    print("TESTING GLOBAL TEMPO HANDLING FIX")
    print("=" * 60)
    
    print("\nIssue Fixed:")
    print("- Previously: Each track processed tempo changes independently")
    print("- Problem: Caused timing offsets of 10+ seconds in complex files")
    print("- Solution: Global tempo change handling across all tracks")
    
    print("\nKey Changes:")
    print("1. First pass: Collect all tempo changes with global timing")
    print("2. Sort tempo changes by time")
    print("3. Second pass: Process notes with correct tempo at each time")
    print("4. Eliminates per-track tempo drift")
    
    print("\nWhat to Test:")
    print("1. Load MIDI files with tempo changes")
    print("2. Check keyboard highlighting accuracy")
    print("3. Verify no 10+ second offsets")
    print("4. Test with complex multi-track files")
    
    print("\nFiles to Test:")
    print("- Simple files (test_melody.mid, test_chords.mid)")
    print("- Complex files with tempo changes")
    print("- Multi-track arrangements")
    
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
    test_tempo_fix()
