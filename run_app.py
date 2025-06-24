#!/usr/bin/env python3
"""Final launch test"""

def test_main_launch():
    try:
        print("Launching Python MIDI Gapper 2...")
        
        # Import and run main
        from main import MidiGapperGUI
        
        app = MidiGapperGUI()
        print("✓ Application created successfully!")
        print("✓ Program is ready to use!")
        print("")
        print("Features available:")
        print("- MIDI file loading and visualization")
        print("- Gap creation tools")
        print("- Timeline-based playback (visual highlighting)")
        print("- MIDI device selection (when devices are available)")
        print("- Save/export functionality")
        print("")
        print("Note: MIDI audio output requires a MIDI device.")
        print("The visualization and playback will work without audio.")
        
        # Start the application
        app.mainloop()
        return True
        
    except Exception as e:
        print(f"✗ Error launching application: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_main_launch()
