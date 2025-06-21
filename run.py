#!/usr/bin/env python3
"""
MIDI Gapper 2 - Application Launcher

This script launches the MIDI Gapper application with all features enabled.
"""
import sys
import os

def launch():
    """Launch the MIDI Gapper application"""
    print("🎵 MIDI Gapper 2 - Professional MIDI Editor & Playback Tool")
    print("=" * 60)
    print()
    print("Features:")
    print("✓ MIDI file loading and gap creation")
    print("✓ Real-time audio playback with pygame")
    print("✓ Synchronized visualization and controls")
    print("✓ Channel management and soloing")
    print("✓ Sustain pedal and timing visualization")
    print("✓ LED position clock and Synthesia keyboard")
    print()
    print("Quick Start:")
    print("1. Click 'Load MIDI' to load a .mid file")
    print("2. Use ▶ ⏸ ⏹ buttons for audio playback")
    print("3. Try the test files: test_melody.mid, test_chords.mid")
    print("4. Adjust gap settings and click 'Create Gaps'")
    print()
    print("Launching application...")
    print("=" * 60)
    
    try:
        # Import and launch the main application
        from main import MidiGapperGUI
        app = MidiGapperGUI()
        app.mainloop()
        
    except KeyboardInterrupt:
        print("\nApplication closed by user.")
    except Exception as e:
        print(f"\nError launching application: {e}")
        print("\nTroubleshooting:")
        print("- Ensure Python 3.7+ is installed")
        print("- Ensure pygame is installed: pip install pygame")
        print("- Ensure mido is installed: pip install mido")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    launch()
