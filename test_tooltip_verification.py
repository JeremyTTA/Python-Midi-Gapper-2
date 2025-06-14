#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from main import MidiGapperGUI
import xml.etree.ElementTree as ET

def parse_xml_notes(xml_content):
    """Parse XML content and extract note information"""
    root = ET.fromstring(xml_content)
    notes = []
    
    for track_elem in root.findall('Track'):
        abs_time = 0
        tempo_us = 500000  # Default tempo
        active_notes = {}  # (channel, note) -> (start_time, start_abs_time)
        
        for msg_elem in track_elem.findall('Message'):
            delta_time = int(msg_elem.get('time', 0))
            abs_time += delta_time
            msg_type = msg_elem.get('type')
            
            if msg_type == 'set_tempo':
                tempo_us = int(msg_elem.get('tempo', tempo_us))
            elif msg_type == 'note_on':
                velocity = int(msg_elem.get('velocity', 0))
                channel = int(msg_elem.get('channel', 0))
                note = int(msg_elem.get('note', 0))
                if velocity > 0:
                    active_notes[(channel, note)] = abs_time
                else:
                    # velocity 0 note_on = note_off
                    key = (channel, note)
                    if key in active_notes:
                        start_time = active_notes[key]
                        duration = abs_time - start_time
                        notes.append({
                            'start_time': start_time,
                            'end_time': abs_time,
                            'duration': duration,
                            'channel': channel,
                            'note': note
                        })
                        del active_notes[key]
            elif msg_type == 'note_off':
                channel = int(msg_elem.get('channel', 0))
                note = int(msg_elem.get('note', 0))
                key = (channel, note)
                if key in active_notes:
                    start_time = active_notes[key]
                    duration = abs_time - start_time
                    notes.append({
                        'start_time': start_time,
                        'end_time': abs_time,
                        'duration': duration,
                        'channel': channel,
                        'note': note
                    })
                    del active_notes[key]
    
    return notes

def test_tooltip_verification():
    print("=== Testing Tooltip Verification After Gap Creation ===")
    
    # Create a root window (required for tkinter)
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    try:
        # Create GUI instance
        app = MidiGapperGUI()
        app.withdraw()  # Hide the GUI window too
        
        # Load the original XML file
        input_file = "A HA.Take on me  K.xml"
        if not os.path.exists(input_file):
            print(f"Error: {input_file} not found")
            return
        
        # Read the original XML content
        with open(input_file, 'r', encoding='utf-8') as f:
            original_xml_content = f.read()
        
        # Parse original notes
        print("=== BEFORE GAP CREATION ===")
        original_notes = parse_xml_notes(original_xml_content)
        
        # Focus on a specific channel/pitch combination for detailed analysis
        test_channel = 4
        test_pitch = 66
        original_test_notes = [note for note in original_notes 
                               if note['channel'] == test_channel and note['note'] == test_pitch]
        original_test_notes.sort(key=lambda x: x['start_time'])
        
        print(f"\nOriginal notes for Channel {test_channel}, Pitch {test_pitch} ({len(original_test_notes)} notes):")
        for i, note in enumerate(original_test_notes[:5]):  # Show first 5 notes
            if i > 0:
                prev_note = original_test_notes[i-1]
                gap = note['start_time'] - prev_note['end_time']
                print(f"  Note {i}: start={note['start_time']}, dur={note['duration']}, end={note['end_time']}, gap_from_prev={gap}")
            else:
                print(f"  Note {i}: start={note['start_time']}, dur={note['duration']}, end={note['end_time']}, gap_from_prev=N/A")
        
        # Put the XML content into the text editor
        app.text.delete('1.0', 'end')
        app.text.insert('1.0', f'Loaded XML file: {input_file}\n')
        app.text.insert('end', original_xml_content)
        
        # Set up MIDI properties
        app.tempo_us = 500000
        class MockMidiData:
            def __init__(self):
                self.ticks_per_beat = 480
        app.midi_data = MockMidiData()
        
        # Create gaps
        gap_ms = 10
        app.gap_var.set(str(gap_ms))
        print(f"\n=== CREATING GAPS OF {gap_ms}ms ===")
        
        # Suppress the detailed debug output for cleaner analysis
        import io
        import contextlib
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            app.create_gaps()
        
        # Get the modified XML content
        modified_content = app.text.get('1.0', 'end')
        # Extract just the XML part (skip the first line which has the file path)
        lines = modified_content.split('\n')
        xml_start_line = None
        for i, line in enumerate(lines):
            if line.strip().startswith('<MidiFile'):
                xml_start_line = i
                break
        
        if xml_start_line is not None:
            modified_xml_content = '\n'.join(lines[xml_start_line:])
        else:
            print("Error: Could not find XML content in modified text")
            return
        
        # Parse modified notes
        print("\n=== AFTER GAP CREATION ===")
        modified_notes = parse_xml_notes(modified_xml_content)
        
        # Get the same test notes after modification
        modified_test_notes = [note for note in modified_notes 
                               if note['channel'] == test_channel and note['note'] == test_pitch]
        modified_test_notes.sort(key=lambda x: x['start_time'])
        
        print(f"\nModified notes for Channel {test_channel}, Pitch {test_pitch} ({len(modified_test_notes)} notes):")
        
        # Calculate required gap in ticks
        ticks_per_second = app.midi_data.ticks_per_beat * (1e6 / app.tempo_us)
        gap_ticks = int((gap_ms / 1000.0) * ticks_per_second)
        print(f"Required gap: {gap_ticks} ticks ({gap_ms}ms)")
        
        gaps_correct = 0
        gaps_incorrect = 0
        
        for i, note in enumerate(modified_test_notes[:5]):  # Show first 5 notes
            if i > 0:
                prev_note = modified_test_notes[i-1]
                gap = note['start_time'] - prev_note['end_time']
                gap_ms_actual = (gap / ticks_per_second) * 1000
                status = "✓ CORRECT" if gap >= gap_ticks else "✗ INCORRECT"
                if gap >= gap_ticks:
                    gaps_correct += 1
                else:
                    gaps_incorrect += 1
                print(f"  Note {i}: start={note['start_time']}, dur={note['duration']}, end={note['end_time']}, gap={gap} ({gap_ms_actual:.1f}ms) {status}")
            else:
                print(f"  Note {i}: start={note['start_time']}, dur={note['duration']}, end={note['end_time']}, gap=N/A")
        
        print(f"\nSummary for Channel {test_channel}, Pitch {test_pitch} (first 5 notes):")
        print(f"  Gaps meeting requirement: {gaps_correct}")
        print(f"  Gaps still too small: {gaps_incorrect}")
        
        # Compare original vs modified durations to see what changed
        print(f"\n=== DURATION CHANGES ===")
        for i in range(min(5, len(original_test_notes), len(modified_test_notes))):
            orig = original_test_notes[i]
            mod = modified_test_notes[i]
            if orig['duration'] != mod['duration']:
                change = mod['duration'] - orig['duration']
                print(f"  Note {i}: duration {orig['duration']} → {mod['duration']} (change: {change})")
            else:
                print(f"  Note {i}: duration unchanged ({orig['duration']})")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        root.destroy()

if __name__ == "__main__":
    test_tooltip_verification()
