#!/usr/bin/env python3
"""
Clean launcher for MIDI Gapper with reduced debug output
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def launch_app():
    try:
        from main import MidiGapperGUI
        
        print("🎵 Starting MIDI Gapper...")
        app = MidiGapperGUI()
        
        # Ensure the window is visible and focused
        app.lift()
        app.focus_force()
        app.attributes('-topmost', True)
        app.after(100, lambda: app.attributes('-topmost', False))
        
        print("✅ Application ready! Window should be visible.")
        print("📝 Note: If a MIDI file was auto-loaded, it may start playing automatically.")
        print("🎮 Use the player controls to pause/stop if needed.")
        print("\n--- Application Running ---")
        
        app.mainloop()
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    launch_app()
