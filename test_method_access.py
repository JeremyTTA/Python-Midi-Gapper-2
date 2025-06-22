#!/usr/bin/env python3
"""
Test script to verify that the create_temp_midi_from_position method is properly accessible.
"""

import tkinter as tk
from main import MidiGapperGUI

def test_method_access():
    """Test that the create_temp_midi_from_position method exists and is callable"""
    try:
        # Create a root window (required for tkinter)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Create the GUI instance
        app = MidiGapperGUI(root)
        
        # Check if the method exists
        if hasattr(app, 'create_temp_midi_from_position'):
            print("✓ Method 'create_temp_midi_from_position' exists on MidiGapperGUI instance")
            
            # Check if it's callable
            if callable(getattr(app, 'create_temp_midi_from_position')):
                print("✓ Method 'create_temp_midi_from_position' is callable")
                
                # Try to get the method signature (without calling it)
                import inspect
                sig = inspect.signature(app.create_temp_midi_from_position)
                print(f"✓ Method signature: create_temp_midi_from_position{sig}")
                
                print("SUCCESS: Method is properly defined and accessible")
                return True
            else:
                print("✗ Method exists but is not callable")
                return False
        else:
            print("✗ Method 'create_temp_midi_from_position' does not exist on MidiGapperGUI instance")
            
            # List available methods for debugging
            methods = [method for method in dir(app) if not method.startswith('_') and callable(getattr(app, method))]
            print(f"Available methods: {methods[:10]}...")  # Show first 10 methods
            return False
            
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up
        try:
            root.destroy()
        except:
            pass

if __name__ == "__main__":
    test_method_access()
