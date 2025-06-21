#!/usr/bin/env python3
"""
Launch the MIDI Gapper application for manual testing
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

def launch_app():
    """Launch the MIDI Gapper application"""
    try:
        from main import MidiGapperGUI
        import tkinter as tk
        
        print("Launching MIDI Gapper with MIDI Playback...")
        print("=" * 50)
        print("Features available:")
        print("✓ MIDI file loading and visualization")
        print("✓ Gap creation and XML editing")
        print("✓ Channel controls and soloing")
        print("✓ MIDI playback with pygame")
        print("✓ Playback position sync with visualization")
        print("✓ LED-style position clock")
        print("✓ Synthesia-style keyboard")
        print("✓ Sustain pedal visualization")
        print("✓ Lyrics display")
        print("=" * 50)
        print()
        print("To test MIDI playback:")
        print("1. Click 'Load MIDI' and select 'test_melody.mid' or 'test_chords.mid'")
        print("2. Use the ▶ button to play, ⏸ to pause, ⏹ to stop")
        print("3. Watch the LED clock and visualization sync")
        print("4. Try dragging the scrollbar to seek to different positions")
        print()
        print("Starting application...")
        
        # Create and run the application
        app = MidiGapperGUI()
        app.mainloop()
        
    except Exception as e:
        print(f"Error launching app: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    launch_app()
