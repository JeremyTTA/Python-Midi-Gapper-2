#!/usr/bin/env python3
"""
Simple test to verify the method access issue is fixed.
This will try to import and check basic functionality.
"""

def test_basic_import():
    """Test basic import and method access"""
    try:
        print("Testing basic import...")
        
        # Try to import main module
        import main
        print("✓ Successfully imported main module")
        
        # Try to access the class
        MidiGapperGUI = main.MidiGapperGUI
        print("✓ Successfully accessed MidiGapperGUI class")
        
        # Check if the method exists on the class
        if hasattr(MidiGapperGUI, 'create_temp_midi_from_position'):
            print("✓ Method 'create_temp_midi_from_position' exists on class")
        else:
            print("✗ Method 'create_temp_midi_from_position' does not exist on class")
            return False
            
        # Check syntax by compiling
        import py_compile
        py_compile.compile('main.py', doraise=True)
        print("✓ main.py compiles without syntax errors")
        
        return True
        
    except SyntaxError as e:
        print(f"✗ Syntax error in main.py: {e}")
        print(f"   Line {e.lineno}: {e.text}")
        return False
    except Exception as e:
        print(f"✗ Error during import test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_import()
    if success:
        print("\n✓ Basic import test passed - method should be accessible")
    else:
        print("\n✗ Basic import test failed - there may still be syntax issues")
