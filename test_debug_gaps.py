#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from main import MidiGapperGUI

def test_gap_creation():
    print("=== Testing Gap Creation with Debug Output ===")
    
    # Create a root window (required for tkinter)
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    try:
        # Create GUI instance
        app = MidiGapperGUI()
        app.withdraw()  # Hide the GUI window too
        
        # Load the XML file directly
        input_file = "A HA.Take on me  K.xml"
        if not os.path.exists(input_file):
            print(f"Error: {input_file} not found")
            return
        
        # Read the XML content
        with open(input_file, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        
        # Put the XML content into the text editor
        app.text.delete('1.0', 'end')
        app.text.insert('1.0', f'Loaded XML file: {input_file}\n')
        app.text.insert('end', xml_content)
        
        print(f"Successfully loaded {input_file}")
        print(f"XML content loaded into text editor")
        
        # We need to set up some basic MIDI properties for the gap calculation
        # Set default tempo and ticks per beat
        app.tempo_us = 500000  # Default tempo (120 BPM)
        
        # Create a minimal midi_data object with ticks_per_beat
        class MockMidiData:
            def __init__(self):
                self.ticks_per_beat = 480  # Default value
        
        app.midi_data = MockMidiData()
        
        # Set a small gap for testing
        gap_ms = 10
        app.gap_var.set(str(gap_ms))
        print(f"\nTesting with gap = {gap_ms}ms")
        
        # Run the gap creation method
        app.create_gaps()
        
        print("\n=== Gap creation completed ===")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        root.destroy()

if __name__ == "__main__":
    test_gap_creation()
