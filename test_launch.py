#!/usr/bin/env python3

"""
Test script to verify the application can launch
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_app_launch():
    try:
        print("Testing application launch...")
        from main import MidiGapperGUI
        print("✓ MidiGapperGUI imported successfully")
        
        app = MidiGapperGUI()
        print("✓ MidiGapperGUI instance created successfully")
        
        # Test that key attributes exist
        required_attrs = ['canvas', 'text', 'led_clock', 'keyboard_canvas']
        for attr in required_attrs:
            if hasattr(app, attr):
                print(f"✓ {attr} attribute exists")
            else:
                print(f"✗ {attr} attribute missing")
        
        # Close the app after a brief moment
        app.after(1000, app.destroy)
        app.mainloop()
        
        print("✓ Application launched and closed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error during app launch test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_app_launch()
    print(f"\nTest result: {'PASSED' if success else 'FAILED'}")
