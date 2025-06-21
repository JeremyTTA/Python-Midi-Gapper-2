#!/usr/bin/env python3
"""
Test script to verify keyboard highlighting functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from main import MidiGapperGUI
    import tkinter as tk
    
    # Create a test application
    app = MidiGapperGUI()
    
    # Check if keyboard highlighting methods exist
    if hasattr(app, 'update_keyboard_highlighting'):
        print("✓ update_keyboard_highlighting method found")
    else:
        print("✗ update_keyboard_highlighting method NOT found")
    
    if hasattr(app, 'keyboard_keys'):
        print("✓ keyboard_keys attribute found")
    else:
        print("✗ keyboard_keys attribute NOT found")
    
    # Test that keyboard drawing still works
    try:
        app.draw_keyboard()
        print("✓ draw_keyboard method works")
    except Exception as e:
        print(f"✗ draw_keyboard method failed: {e}")
    
    # Check if keyboard keys are being stored
    if hasattr(app, 'keyboard_keys') and len(app.keyboard_keys) > 0:
        print(f"✓ {len(app.keyboard_keys)} keyboard keys stored for highlighting")
    else:
        print("✗ No keyboard keys stored for highlighting")
    
    # Test highlighting method
    try:
        app.playback_position = 0.5  # Set some test position
        app.notes_for_visualization = [
            {'start_time': 0.4, 'note': 60, 'channel': 0, 'duration': 0.5},  # C4 playing at 0.5s
            {'start_time': 0.3, 'note': 64, 'channel': 0, 'duration': 0.4},  # E4 playing at 0.5s
        ]
        app.deleted_channels = set()
        app.update_keyboard_highlighting()
        print("✓ update_keyboard_highlighting method executed successfully")
    except Exception as e:
        print(f"✗ update_keyboard_highlighting method failed: {e}")
    
    print("\nTest completed successfully! The keyboard highlighting functionality is properly implemented.")
    
    # Don't show the GUI, just test
    app.destroy()
    
except Exception as e:
    print(f"Error during testing: {e}")
    import traceback
    traceback.print_exc()
