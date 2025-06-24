#!/usr/bin/env python3
"""Test the MIDI device selector functionality"""

import sys
import os

# Add the project directory to the path
project_dir = "g:/My Drive/Programming Projects/Player Piano/Jeremys Code/Python Midi Gapper 2"
sys.path.insert(0, project_dir)

# Change to project directory
os.chdir(project_dir)

# Import and run the main application
try:
    from main import MidiGapperGUI
    
    print("🎹 Testing MIDI Device Selector")
    print("Features to test:")
    print("1. MIDI output dropdown appears under player controls")
    print("2. Dropdown shows available MIDI devices")
    print("3. Green/red circle shows connection status")
    print("4. Device selection persists on restart")
    print("5. Refresh button rescans devices")
    print("=" * 50)
    
    app = MidiGapperGUI()
    
    print("\n✓ Application started with MIDI device selector!")
    print("Look for the 'MIDI Output:' dropdown under the player controls")
    
    app.mainloop()
    
except Exception as e:
    print(f"❌ Error starting application: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")
