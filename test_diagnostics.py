#!/usr/bin/env python3
"""
Test script to run diagnostic functions on MIDI/XML conversion
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from main import MidiGapperGUI
import mido
from mido import MidiFile

def test_midi_xml_conversion():
    """Test the MIDI to XML and back conversion without GUI"""
    
    # Create a test instance (but don't start GUI)
    app = MidiGapperGUI()
    app.withdraw()  # Hide the window
    
    # Load the existing MIDI file mentioned in config
    config_file = "config.json"
    if os.path.exists(config_file):
        import json
        with open(config_file, 'r') as f:
            config = json.load(f)
            last_midi = config.get('last_midi')
            if last_midi and os.path.exists(last_midi):
                print(f"Testing with MIDI file: {last_midi}")
                
                # Load and process the MIDI file
                try:
                    app.midi_data = MidiFile(last_midi)
                    app.current_midi_file = last_midi
                    
                    # Process the MIDI file (simulate what load_midi_file does)
                    app.process_midi(last_midi)
                    
                    print("\n" + "="*50)
                    print("RUNNING DIAGNOSTICS")
                    print("="*50)
                    
                    # Run the comparison
                    app.compare_midi_and_xml()
                    
                    print("\n" + "="*50)
                    print("TESTING ROUND-TRIP CONVERSION")
                    print("="*50)
                    
                    # Test round-trip conversion
                    app.test_roundtrip_conversion()
                    
                except Exception as e:
                    print(f"Error processing MIDI file: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print(f"MIDI file not found: {last_midi}")
    else:
        print("No config file found")
    
    # Don't start the GUI mainloop
    app.destroy()

if __name__ == "__main__":
    test_midi_xml_conversion()
