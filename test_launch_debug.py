#!/usr/bin/env python3
"""
Test if main.py can be imported and run without errors
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

def test_main_launch():
    """Test launching the main application"""
    try:
        print("Testing main.py import...")
        import main
        print("✓ main.py imported successfully")
        
        print("Testing MidiGapperGUI creation...")
        app = main.MidiGapperGUI()
        print("✓ MidiGapperGUI created successfully")
        print(f"✓ MIDI playback available: {app.midi_playback_available}")
        
        # Test basic functionality
        print("Testing basic methods...")
        app.update_led_clock()
        print("✓ LED clock update works")
        
        # Don't start mainloop in test, just verify creation
        app.destroy()
        print("✓ Application cleanup successful")
        
        print("\n🎯 Application should launch correctly!")
        print("Try running: python main.py")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("Testing MIDI Gapper Launch...")
    print("=" * 40)
    success = test_main_launch()
    if not success:
        print("\n❌ Application has issues that prevent launching")
    else:
        print("\n✅ Application is ready to launch!")
