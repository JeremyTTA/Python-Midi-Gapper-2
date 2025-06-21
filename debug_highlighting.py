"""
Diagnostic test for keyboard highlighting during playback
"""
import tkinter as tk
from tkinter import ttk, filedialog
import time
import threading
import os

class HighlightingDiagnostic(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Highlighting Diagnostic')
        self.geometry('600x400')
        
        # Import main app
        import sys
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, script_dir)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Instructions
        instruction_text = """
        KEYBOARD HIGHLIGHTING DIAGNOSTIC
        
        This tool will help diagnose why keyboard highlighting
        only works during manual scrolling but not during playback.
        
        Test Process:
        1. Load main application
        2. Load a MIDI file
        3. Start playback from beginning
        4. Observe if keyboard highlights appear
        5. Try manual scrolling - verify highlights work
        6. Check timing values in console
        
        Expected Behavior:
        - Highlighting should work during both playback AND manual scrolling
        - Audio position should match visual position during normal playback
        - Notes should highlight when they're playing
        
        Suspected Issues:
        - get_actual_audio_position() may return wrong values during playback
        - visual_position_offset logic may be incorrect for normal playback
        - Timer may not be calling update_keyboard_highlighting() properly
        """
        
        text_widget = tk.Text(self, wrap='word', padx=10, pady=10)
        text_widget.pack(fill='both', expand=True)
        text_widget.insert('1.0', instruction_text)
        text_widget.config(state='disabled')
        
        # Control frame
        control_frame = ttk.Frame(self)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(control_frame, text='Launch Main App', 
                  command=self.launch_main_app).pack(side='left', padx=5)
        
        ttk.Button(control_frame, text='Show Debug Console', 
                  command=self.show_debug_console).pack(side='left', padx=5)
        
    def launch_main_app(self):
        """Launch the main application"""
        import subprocess
        import sys
        
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_py_path = os.path.join(script_dir, "main.py")
            subprocess.Popen([sys.executable, main_py_path])
            print("Main application launched")
        except Exception as e:
            print(f"Error launching main app: {e}")
            
    def show_debug_console(self):
        """Show debug information"""
        debug_window = tk.Toplevel(self)
        debug_window.title('Debug Console')
        debug_window.geometry('500x300')
        
        debug_text = tk.Text(debug_window, wrap='word', font=('Courier', 10))
        debug_text.pack(fill='both', expand=True)
        
        debug_info = """
        DEBUG CHECKLIST FOR HIGHLIGHTING ISSUE:
        
        1. Check update_playback_timer() execution:
           - Add print statements to verify it's running
           - Verify self.is_playing is True during playback
           - Check if update_keyboard_highlighting() is called
        
        2. Check get_actual_audio_position() return values:
           - Should return elapsed_time during normal playback
           - Should NOT return -1 during normal playback
           - Compare with self.playback_position
        
        3. Check visual_position_offset logic:
           - Should be 0.0 when starting from beginning
           - Should only be > 0.1 when seeking to a position
        
        4. Check notes_for_visualization data:
           - Verify notes exist in the time range
           - Check start_time and duration values
           - Ensure channels are not in deleted_channels
        
        DEBUGGING CODE TO ADD TO main.py:
        
        In update_playback_timer():
        print(f"Timer: position={self.playback_position:.3f}, playing={self.is_playing}")
        
        In get_actual_audio_position():
        print(f"Audio pos: elapsed={elapsed_time:.3f}, offset={self.visual_position_offset:.3f}")
        
        In update_keyboard_highlighting():
        print(f"Highlighting: audio_pos={audio_position:.3f}, notes_found={len(currently_playing_notes)}")
        """
        
        debug_text.insert('1.0', debug_info)
        debug_text.config(state='disabled')

if __name__ == '__main__':
    app = HighlightingDiagnostic()
    app.mainloop()
