#!/usr/bin/env python3
"""
Basic functionality test for the updated MIDI player
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

try:
    print("Testing imports...")
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    import mido
    from mido import MidiFile, Message
    import pygame
    import json
    import threading
    import time
    import math
    
    print("✓ All imports successful")
    
    # Test basic MIDI functionality
    print("Testing MIDI functionality...")
    
    # Check if we can create a MIDI output port
    try:
        output_names = mido.get_output_names()
        print(f"✓ Available MIDI outputs: {output_names}")
    except Exception as e:
        print(f"⚠ MIDI output check failed: {e}")
    
    # Test pygame initialization
    print("Testing pygame initialization...")
    try:
        pygame.init()
        pygame.mixer.init()
        print("✓ Pygame initialized successfully")
    except Exception as e:
        print(f"⚠ Pygame init failed: {e}")
    
    print("Testing main application import...")
    try:
        # Import just the core classes without running the GUI
        exec(open("main.py").read().replace("if __name__ == '__main__':", "if False:"))
        print("✓ Main application code compiled successfully")
    except Exception as e:
        print(f"✗ Main application import failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nBasic functionality test completed!")
    
except Exception as e:
    print(f"✗ Test failed: {e}")
    import traceback
    traceback.print_exc()
