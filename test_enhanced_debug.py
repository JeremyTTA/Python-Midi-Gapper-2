#!/usr/bin/env python3
"""
Test script to run the main app and test the enhanced debugging for temp MIDI file issues
"""

import sys
import os
import subprocess

def test_enhanced_debugging():
    """Test the enhanced debugging version of the app"""
    
    print("=== ENHANCED DEBUGGING TEST ===")
    print("This will launch the main app with enhanced temp file debugging")
    print("Instructions:")
    print("1. Load a MIDI file")
    print("2. Scroll to around 30-60 seconds")
    print("3. Press play")
    print("4. Check the console output for detailed debugging info")
    print("5. Close the app when done")
    print()
    
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Use the correct Python path
    python_path = "C:/Users/JeremyStandlee/AppData/Local/Programs/Python/Python313/python.exe"
    
    try:
        print("Launching main.py with enhanced debugging...")
        print("Watch the console for detailed temp file analysis...")
        print()
        
        # Run the main app
        result = subprocess.run([python_path, "main.py"], 
                              capture_output=False, 
                              text=True)
        
        print(f"App closed with exit code: {result.returncode}")
        
    except Exception as e:
        print(f"Error launching app: {e}")

if __name__ == "__main__":
    test_enhanced_debugging()
