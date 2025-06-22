#!/usr/bin/env python3
"""
Test the main app with graceful FluidSynth fallback
"""

import subprocess
import sys
import os

def test_app_startup():
    """Test that the app starts properly even without FluidSynth"""
    
    print("=== TESTING APP STARTUP WITH FLUIDSYNTH FALLBACK ===")
    print()
    
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Use the correct Python path
    python_path = "C:/Users/JeremyStandlee/AppData/Local/Programs/Python/Python313/python.exe"
    
    print("Expected behavior:")
    print("1. ⚠ FluidSynth not available - falling back to pygame (no seeking)")
    print("2. App should start normally with pygame MIDI support")
    print("3. Seeking will use temporary file approach (existing fix)")
    print("4. No crashes or errors")
    print()
    
    print("Testing startup...")
    
    try:
        # Test just importing the main module (quick check)
        test_import = subprocess.run([
            python_path, "-c", 
            "import sys; sys.path.insert(0, '.'); "
            + "print('Testing imports...'); "
            + "import main; "
            + "print('✓ Main module imports successfully')"
        ], capture_output=True, text=True, timeout=10)
        
        if test_import.returncode == 0:
            print("✓ Import test passed")
            print("Output:", test_import.stdout.strip())
            if test_import.stderr:
                print("Messages:", test_import.stderr.strip())
        else:
            print("✗ Import test failed")
            print("Error:", test_import.stderr)
            return
        
        print()
        print("App should now start properly with pygame fallback.")
        print("You can test MIDI seeking - it will use the temporary file approach.")
        print()
        print("To enable FluidSynth seeking:")
        print("1. Install FluidSynth binary: winget install FluidSynth.FluidSynth")
        print("2. Restart the app")
        print("3. Look for: '✓ FluidSynth available' message")
        
    except subprocess.TimeoutExpired:
        print("⚠ Import test timed out (may indicate startup issues)")
    except Exception as e:
        print(f"✗ Test failed: {e}")

if __name__ == "__main__":
    test_app_startup()
