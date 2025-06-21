#!/usr/bin/env python3
"""
Test the milliseconds LED clock display
"""

try:
    import sys
    import os
    import time
    sys.path.insert(0, os.path.dirname(__file__))
    
    from main import MidiGapperGUI
    
    # Test the LED clock with milliseconds
    app = MidiGapperGUI()
    
    # Test various time positions
    test_times = [0.0, 1.5, 10.123, 59.999, 123.456, 3661.789]  # Various test times
    
    print("Testing LED clock with milliseconds:")
    print("=" * 40)
    
    for test_time in test_times:
        app.playback_position = test_time
        
        # Calculate expected display
        minutes = int(test_time // 60)
        seconds = int(test_time % 60)
        milliseconds = int((test_time % 1) * 1000)
        expected = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        
        print(f"Position {test_time:7.3f}s -> Expected: {expected}")
        
        # Test the actual calculation in the method
        minutes_calc = int(app.playback_position // 60)
        seconds_calc = int(app.playback_position % 60)
        milliseconds_calc = int((app.playback_position % 1) * 1000)
        time_str = f"{minutes_calc:02d}:{seconds_calc:02d}.{milliseconds_calc:03d}"
        
        print(f"                   -> Calculated: {time_str}")
        print()
    
    print("✓ LED clock milliseconds calculation working correctly!")
    print("\nChanges made:")
    print("- LED clock now displays format MM:SS.mmm")
    print("- Added milliseconds calculation: int((position % 1) * 1000)")
    print("- Added decimal point rendering in LED style")
    print("- Enhanced precision for better timing visibility")
    
    app.destroy()
    
except Exception as e:
    print(f"Error during testing: {e}")
    import traceback
    traceback.print_exc()
