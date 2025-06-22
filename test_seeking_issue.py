#!/usr/bin/env python3
"""
Test script to diagnose seeking issue
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from main import MidiGapperGUI
    import tkinter as tk
    import time

    print("=== Testing MIDI Seeking Issue ===")
    
    # Create app without showing UI
    app = MidiGapperGUI()
    app.withdraw()  # Hide window
    
    # Find test file
    test_files = ['test_melody.mid', 'A HA.Take on me  K.xml']
    midi_file = None
    for f in test_files:
        if os.path.exists(f) and f.endswith('.mid'):
            midi_file = f
            break
    
    if midi_file:
        print(f"Loading test file: {midi_file}")
        app.process_midi(midi_file)
        print(f"Max time: {app.max_time:.2f}s")
        
        # Test 1: Check if scrollbar seeking sets playback_position
        print(f"\nTest 1: Setting playback position to 3.0s")
        original_pos = app.playback_position
        app.playback_position = 3.0
        print(f"  Original position: {original_pos:.2f}s")
        print(f"  New position: {app.playback_position:.2f}s")
        
        # Test 2: Test temporary file creation
        print(f"\nTest 2: Creating temp file from 3.0s")
        temp_file = app.create_temp_midi_from_position(3.0)
        if temp_file:
            if os.path.exists(temp_file):
                print(f"  ✓ Temp file created: {os.path.basename(temp_file)}")
                print(f"  ✓ Temp file size: {os.path.getsize(temp_file)} bytes")
                print(f"  ✓ Temp file path: {temp_file}")
            else:
                print(f"  ✗ Temp file path returned but file does not exist")
        else:
            print(f"  ✗ Temp file creation failed (returned None)")
        
        # Test 3: Check playback method selection
        print(f"\nTest 3: Checking playback system")
        if hasattr(app, 'fluidsynth_ready'):
            print(f"  FluidSynth ready: {app.fluidsynth_ready}")
        print(f"  MIDI playback available: {app.midi_playback_available}")
        
        # Test 4: Simulate what happens when play is pressed with position > 0.1
        print(f"\nTest 4: Simulating playback from position 3.0s")
        app.playback_position = 3.0
        print(f"  Playback position set to: {app.playback_position:.2f}s")
        
        # Check which playback method would be used
        if app.playback_position > 0.1:
            print(f"  ✓ Position > 0.1s, should trigger temp file creation")
            temp_file2 = app.create_temp_midi_from_position(app.playback_position)
            if temp_file2 and os.path.exists(temp_file2):
                print(f"  ✓ Temp file would be created: {os.path.basename(temp_file2)}")
            else:
                print(f"  ✗ Temp file creation would fail")
        else:
            print(f"  Position <= 0.1s, would use original file")
        
        # Test 5: Check what happens if we call start_midi_playback directly
        print(f"\nTest 5: Testing start_midi_playback logic")
        try:
            # Don't actually start playback, just check the logic
            if hasattr(app, 'fluidsynth_ready') and app.fluidsynth_ready:
                print(f"  Would use FluidSynth playback")
            else:
                print(f"  Would use pygame playback")
                
                # Check the pygame logic
                if app.playback_position > 0.1:
                    print(f"  Would create temp file for seeking")
                    temp_test = app.create_temp_midi_from_position(app.playback_position)
                    if temp_test and os.path.exists(temp_test):
                        print(f"  ✓ Temp file creation successful")
                    else:
                        print(f"  ✗ Temp file creation failed")
                else:
                    print(f"  Would use original file")
        except Exception as e:
            print(f"  Error in playback logic test: {e}")
        
        app.cleanup_temp_files()
        print(f"\nTest completed. Cleaning up temporary files.")
        
    else:
        print("No test MIDI file found. Please ensure 'test_melody.mid' exists.")
        print("You can create one by running: python create_test_midi.py")
    
    app.destroy()
    print("\n=== Test Complete ===")
    
except Exception as e:
    print(f"Error during test: {e}")
    import traceback
    traceback.print_exc()
