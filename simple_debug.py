#!/usr/bin/env python3
"""
Simple debug test
"""
print("Starting test...")

try:
    import mido
    print("mido imported successfully")
except Exception as e:
    print(f"mido import error: {e}")

try:
    import main
    print("main.py imported successfully") 
    print(f"MidiGapperGUI class exists: {hasattr(main, 'MidiGapperGUI')}")
except Exception as e:
    print(f"main.py import error: {e}")

print("Test complete.")
