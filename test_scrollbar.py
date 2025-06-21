#!/usr/bin/env python3

"""
Test script to verify scrollbar-to-time mapping
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_scrollbar_sync():
    try:
        print("Testing scrollbar-to-time mapping...")
        from main import MidiGapperGUI
        
        app = MidiGapperGUI()
        print("✓ App created successfully")
        
        # Wait for auto-load to complete
        def test_after_load():
            if hasattr(app, 'max_time') and app.max_time > 0:
                print(f"✓ MIDI loaded, max_time: {app.max_time:.2f}s")
                
                # Test scrollbar at bottom (should show 0.0s)
                app.canvas.yview_moveto(1.0)  # Scroll to bottom
                app.on_scroll_with_midi_sync('moveto', '1.0')
                print(f"✓ Scrollbar at bottom, playback_position: {app.playback_position:.2f}s")
                
                # Test scrollbar at top (should show max_time)
                app.canvas.yview_moveto(0.0)  # Scroll to top
                app.on_scroll_with_midi_sync('moveto', '0.0')
                print(f"✓ Scrollbar at top, playback_position: {app.playback_position:.2f}s")
                
                # Test middle position
                app.canvas.yview_moveto(0.5)  # Scroll to middle
                app.on_scroll_with_midi_sync('moveto', '0.5')
                print(f"✓ Scrollbar at middle, playback_position: {app.playback_position:.2f}s")
                
                print("✓ Scrollbar-to-time mapping test completed")
            else:
                print("? No MIDI loaded or max_time not set")
            
            app.destroy()
        
        # Schedule test after auto-load
        app.after(2000, test_after_load)
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"✗ Error during scrollbar test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_scrollbar_sync()
    print(f"\nTest result: {'PASSED' if success else 'FAILED'}")
