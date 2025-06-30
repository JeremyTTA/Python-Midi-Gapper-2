#!/usr/bin/env python3
"""
Simple test to verify the duration fix in the main.py application
by loading a MIDI file and checking the duration calculation.
"""

import sys
import os
import mido

# Add the current directory to the path so we can import from main.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_main_duration_fix():
    """Test that the main.py duration calculation is working correctly."""
    
    # Import the MidiGapperGUI class from main.py
    try:
        from main import MidiGapperGUI
        print("✓ Successfully imported MidiGapperGUI from main.py")
    except ImportError as e:
        print(f"✗ Failed to import MidiGapperGUI: {e}")
        return False
    
    # Find a test MIDI file
    test_files = ['test_melody.mid', 'test_chords.mid', 'temp_midi_2000.mid']
    test_file = None
    
    for filename in test_files:
        if os.path.exists(filename):
            test_file = filename
            break
    
    if not test_file:
        print("✗ No test MIDI files found. Available files:")
        for f in os.listdir('.'):
            if f.endswith(('.mid', '.midi')):
                print(f"  - {f}")
        return False
    
    print(f"✓ Using test file: {test_file}")
    
    # Get the reference duration using mido directly
    try:
        mf = mido.MidiFile(test_file)
        reference_duration = mf.length
        print(f"✓ Reference duration (mido): {reference_duration:.3f}s")
    except Exception as e:
        print(f"✗ Failed to get reference duration: {e}")
        return False
    
    # Create a mock tkinter root (needed for MidiViewer)
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    try:
        # Create a MidiGapperGUI instance
        app = MidiGapperGUI()
        
        # Load the MIDI file (this will trigger our duration calculation)
        print(f"Loading MIDI file through MidiGapperGUI...")
        app.process_midi(test_file)
        
        # Get the calculated duration
        calculated_duration = app.max_time
        print(f"✓ Calculated duration: {calculated_duration:.3f}s")
        
        # Compare durations
        difference = abs(reference_duration - calculated_duration)
        print(f"✓ Difference: {difference:.3f}s")
        
        # Check if they match within a reasonable tolerance (0.1 seconds)
        if difference < 0.1:
            print("✅ SUCCESS: Duration calculation is correct!")
            return True
        else:
            print(f"❌ FAILURE: Duration calculation differs by {difference:.3f}s")
            return False
            
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if 'app' in locals():
            app.destroy()

if __name__ == "__main__":
    print("Testing duration fix in main.py...")
    print("=" * 50)
    
    success = test_main_duration_fix()
    
    print("=" * 50)
    if success:
        print("✅ All tests passed! The duration fix is working correctly.")
    else:
        print("❌ Tests failed. The duration calculation may still have issues.")
