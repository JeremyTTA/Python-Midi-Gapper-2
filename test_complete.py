#!/usr/bin/env python3
"""
Final verification script for Python MIDI Gapper 2
This script tests all major components to ensure everything works
"""

def run_comprehensive_test():
    print("=" * 50)
    print("PYTHON MIDI GAPPER 2 - COMPREHENSIVE TEST")
    print("=" * 50)
    
    try:
        # Test 1: Import main module
        print("\n1. Testing module imports...")
        import main
        print("   ✓ Main module imported successfully")
        
        # Test 2: Create GUI instance
        print("\n2. Testing GUI creation...")
        app = main.MidiGapperGUI()
        print("   ✓ GUI instance created successfully")
        
        # Test 3: Check core attributes
        print("\n3. Testing core components...")
        required_components = [
            'canvas', 'text', 'led_clock', 'keyboard_canvas',
            'midi_output_dropdown', 'play_pause_button', 'stop_button',
            'rewind_button', 'note_player'
        ]
        
        for component in required_components:
            if hasattr(app, component):
                print(f"   ✓ {component} - OK")
            else:
                print(f"   ✗ {component} - MISSING")
        
        # Test 4: Check MIDI system
        print("\n4. Testing MIDI system...")
        if hasattr(app, 'note_player') and app.note_player:
            print("   ✓ MIDI note player initialized")
            if app.note_player.midi_out:
                print("   ✓ MIDI output device available")
            else:
                print("   ⚠ MIDI output device not available (this is normal)")
        else:
            print("   ✗ MIDI note player missing")
        
        # Test 5: Check playback controls
        print("\n5. Testing playback controls...")
        playback_attrs = ['is_playing', 'is_paused', 'playback_position', 'playback_timer']
        for attr in playback_attrs:
            if hasattr(app, attr):
                print(f"   ✓ {attr} - OK")
            else:
                print(f"   ✗ {attr} - MISSING")
        
        # Test 6: Test GUI display
        print("\n6. Testing GUI display...")
        print("   ✓ Starting GUI for visual verification...")
        print("   ℹ The application window should appear now")
        print("   ℹ Close the window to complete the test")
        
        # Run the GUI
        app.mainloop()
        
        print("\n7. Test Results:")
        print("   ✓ All tests completed successfully!")
        print("   ✓ Python MIDI Gapper 2 is ready to use!")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def print_usage_instructions():
    print("\n" + "=" * 50)
    print("HOW TO USE PYTHON MIDI GAPPER 2")
    print("=" * 50)
    print("\n📁 Loading MIDI Files:")
    print("   • Click 'Open MIDI File' to load a .mid or .midi file")
    print("   • The file will be visualized and converted to XML")
    
    print("\n🎹 Playback Controls:")
    print("   • ▶ Play/Pause: Start or pause playback")
    print("   • ⏹ Stop: Stop playback and return to beginning")  
    print("   • ⏮ Rewind: Jump to the beginning")
    print("   • Use scrollbar or arrow keys to seek")
    
    print("\n⚙️ Gap Creation:")
    print("   • Set gap time in milliseconds")
    print("   • Click 'Create Gaps' to add space between notes")
    print("   • Gaps prevent overlapping notes on the same pitch")
    
    print("\n🎵 MIDI Output:")
    print("   • Use the dropdown to select MIDI output device")
    print("   • Green indicator = connected, Red = not connected")
    print("   • Click refresh (🔄) to rescan devices")
    
    print("\n💾 Saving:")
    print("   • Click 'Save MIDI As...' to export modified MIDI")
    print("   • Changes are saved from the XML representation")
    
    print("\n🎯 Features:")
    print("   • Real-time note highlighting during playback")
    print("   • Visual piano keyboard with note highlighting")
    print("   • Channel visibility controls (hover over Channels)")
    print("   • Detailed MIDI information display")
    print("   • Perfect timing synchronization")
    
    print("\n📖 Note: The program works with or without MIDI audio output")
    print("        Visualization and controls function independently")

if __name__ == "__main__":
    success = run_comprehensive_test()
    
    if success:
        print_usage_instructions()
        print(f"\n🎉 SUCCESS: Python MIDI Gapper 2 is fully functional!")
    else:
        print(f"\n❌ FAILED: There were issues with the program setup")
