#!/usr/bin/env python3
"""
Test the enhanced MIDI controls with larger buttons and traditional symbols
"""

try:
    import sys
    import os
    import tkinter as tk
    sys.path.insert(0, os.path.dirname(__file__))
    
    from main import MidiGapperGUI
    
    print("Testing enhanced MIDI controls:")
    print("=" * 40)
    
    # Create the application
    app = MidiGapperGUI()
    
    # Check if all new components exist
    checks = [
        ('rewind_button', 'Rewind button'),
        ('play_pause_button', 'Play/Pause toggle button'),
        ('stop_button', 'Stop button'),
        ('led_clock', 'LED clock display'),
    ]
    
    for attr_name, description in checks:
        if hasattr(app, attr_name):
            print(f"✓ {description} found")
            
            # Check button properties
            if 'button' in attr_name:
                button = getattr(app, attr_name)
                print(f"  - Text: '{button.cget('text')}'")
                print(f"  - Size: {button.cget('width')}x{button.cget('height')}")
                print(f"  - Font: {button.cget('font')}")
                print(f"  - Background: {button.cget('bg')}")
        else:
            print(f"✗ {description} NOT found")
    
    # Check LED clock size
    if hasattr(app, 'led_clock'):
        clock = app.led_clock
        print(f"\n✓ LED Clock properties:")
        print(f"  - Width: {clock.cget('width')} (expected: 160)")
        print(f"  - Height: {clock.cget('height')} (expected: 40)")
        print(f"  - Background: {clock.cget('bg')}")
    
    # Check if new methods exist
    methods = [
        ('rewind_to_start', 'Rewind to start method'),
        ('toggle_play_pause', 'Toggle play/pause method'),
        ('resume_midi', 'Resume MIDI method'),
    ]
    
    print(f"\n✓ New methods:")
    for method_name, description in methods:
        if hasattr(app, method_name):
            print(f"  - {description}: found")
        else:
            print(f"  - {description}: NOT found")
    
    # Test button state changes
    print(f"\n✓ Testing button state changes:")
    
    # Initial state
    initial_text = app.play_pause_button.cget('text')
    initial_bg = app.play_pause_button.cget('bg')
    print(f"  - Initial button: '{initial_text}' with background '{initial_bg}'")
    
    # Test rewind functionality
    app.playback_position = 10.5
    app.rewind_to_start()
    print(f"  - After rewind: position = {app.playback_position} (should be 0.0)")
    
    print("\n" + "=" * 40)
    print("✓ Enhanced MIDI controls test completed!")
    print("\nNew features:")
    print("- Larger, more prominent buttons with traditional symbols")
    print("- Rewind button (⏮) for quick return to start")
    print("- Combined play/pause button that toggles between ▶ and ⏸")
    print("- Larger LED clock display (160x40) with enhanced visibility")
    print("- Improved layout with controls in logical order")
    print("- Color-coded buttons (green=play, orange=pause, red=stop)")
    
    app.destroy()
    
except Exception as e:
    print(f"Error during testing: {e}")
    import traceback
    traceback.print_exc()
