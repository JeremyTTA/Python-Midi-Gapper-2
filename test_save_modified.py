#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from main import MidiGapperGUI

def test_save_modified():
    print("=== Testing Save Modified File ===")
    
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
        
        # Set up MIDI properties
        app.tempo_us = 500000
        class MockMidiData:
            def __init__(self):
                self.ticks_per_beat = 480
        app.midi_data = MockMidiData()
        
        # Set gap and create gaps
        gap_ms = 10
        app.gap_var.set(str(gap_ms))
        print(f"Creating gaps of {gap_ms}ms...")
        
        # Run the gap creation method (suppress debug output)
        app.create_gaps()
        
        # Save the modified content
        output_file = "A HA.Take on me  K-modified.xml"
        modified_content = app.text.get('1.0', 'end')
        
        # Extract just the XML part (skip the first line which has the file path)
        lines = modified_content.split('\n')
        xml_start_line = None
        for i, line in enumerate(lines):
            if line.strip().startswith('<MidiFile'):
                xml_start_line = i
                break
        
        if xml_start_line is not None:
            xml_content = '\n'.join(lines[xml_start_line:])
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            print(f"Modified file saved as: {output_file}")
        else:
            print("Error: Could not find XML content in modified text")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        root.destroy()

if __name__ == "__main__":
    test_save_modified()
