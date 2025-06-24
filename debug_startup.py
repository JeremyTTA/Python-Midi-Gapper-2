#!/usr/bin/env python3
"""Debug script to test main.py startup step by step"""

import sys
import traceback

def test_step_by_step():
    print("Step 1: Testing basic imports...")
    try:
        import tkinter as tk
        print("✓ tkinter imported")
        
        import mido
        print("✓ mido imported")
        
        import pygame
        print("✓ pygame imported")
        
        import xml.etree.ElementTree as ET
        print("✓ xml.etree.ElementTree imported")
        
        print("Step 2: Testing main module import...")
        import main
        print("✓ main module imported")
        
        print("Step 3: Testing MidiNotePlayer class...")
        note_player = main.MidiNotePlayer()
        print("✓ MidiNotePlayer created")
        
        print("Step 4: Testing MidiGapperGUI creation...")
        
        # Add error handling to the GUI creation
        app = main.MidiGapperGUI()
        print("✓ MidiGapperGUI created successfully")
        
        print("Step 5: Testing that GUI has required attributes...")
        required_attrs = ['canvas', 'text', 'led_clock', 'keyboard_canvas', 'midi_output_dropdown']
        for attr in required_attrs:
            if hasattr(app, attr):
                print(f"✓ {attr} exists")
            else:
                print(f"✗ {attr} missing!")
                
        print("Step 6: Starting main loop for 2 seconds...")
        app.after(2000, app.destroy)  # Auto-close after 2 seconds
        app.mainloop()
        print("✓ GUI loop completed successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Error at step: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Debug Test for main.py ===")
    success = test_step_by_step()
    print(f"\nResult: {'SUCCESS' if success else 'FAILED'}")
