#!/usr/bin/env python3
"""
Test script to simulate the specific error condition and debug the method access issue.
"""

import sys
import os

# Add the current directory to path if needed
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def test_method_call():
    """Test the actual method call that's causing the error"""
    try:
        # Import the required modules
        import tkinter as tk
        from main import MidiGapperGUI
        
        print("Creating tkinter root window...")
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        print("Creating MidiGapperGUI instance...")
        app = MidiGapperGUI(root)
        
        print("Checking if create_temp_midi_from_position method exists...")
        if hasattr(app, 'create_temp_midi_from_position'):
            print("✓ Method exists")
            
            # Check the method type
            method = getattr(app, 'create_temp_midi_from_position')
            print(f"Method type: {type(method)}")
            print(f"Method callable: {callable(method)}")
            
            # Try to inspect the method
            import inspect
            if inspect.ismethod(method):
                print("✓ It's a proper instance method")
                sig = inspect.signature(method)
                print(f"Method signature: {sig}")
            else:
                print(f"✗ Not a proper instance method: {type(method)}")
            
            print("SUCCESS: Method is properly accessible")
            return True
        else:
            print("✗ Method does not exist")
            
            # Debug: list all methods that contain 'temp' or 'midi'
            all_attrs = dir(app)
            relevant_attrs = [attr for attr in all_attrs if 'temp' in attr.lower() or 'midi' in attr.lower()]
            print(f"Relevant attributes: {relevant_attrs}")
            
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
    success = test_method_call()
    if success:
        print("\n✓ Test passed - method should be accessible")
    else:
        print("\n✗ Test failed - method access issue confirmed")
