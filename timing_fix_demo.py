"""
Demonstration script showing before/after timing behavior
"""
import time
import tkinter as tk
from tkinter import ttk

class TimingDemo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Timing Fix Demonstration')
        self.geometry('600x400')
        
        # Variables
        self.start_time = None
        self.is_running = False
        
        # Create UI
        self.setup_ui()
        
    def setup_ui(self):
        title_label = ttk.Label(self, text='MIDI Timing Fix Demonstration', 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Old method demo
        old_frame = ttk.LabelFrame(self, text='OLD METHOD (Incremental - Causes Drift)', padding=10)
        old_frame.pack(fill='x', padx=10, pady=5)
        
        self.old_position = 0.0
        self.old_display = ttk.Label(old_frame, text='Position: 0.000s', font=('Courier', 12))
        self.old_display.pack()
        
        old_desc = ttk.Label(old_frame, text='Updates position += 0.1 every 100ms → Accumulates error over time', 
                            foreground='red')
        old_desc.pack()
        
        # New method demo
        new_frame = ttk.LabelFrame(self, text='NEW METHOD (Elapsed Time - Accurate)', padding=10)
        new_frame.pack(fill='x', padx=10, pady=5)
        
        self.new_display = ttk.Label(new_frame, text='Position: 0.000s', font=('Courier', 12))
        self.new_display.pack()
        
        new_desc = ttk.Label(new_frame, text='Calculates actual elapsed time from start → Always accurate', 
                            foreground='green')
        new_desc.pack()
        
        # Error comparison
        error_frame = ttk.LabelFrame(self, text='Timing Error Comparison', padding=10)
        error_frame.pack(fill='x', padx=10, pady=5)
        
        self.error_display = ttk.Label(error_frame, text='Error: 0.000s', font=('Courier', 12))
        self.error_display.pack()
        
        error_desc = ttk.Label(error_frame, text='Shows how much the old method drifts from actual time')
        error_desc.pack()
        
        # Controls
        control_frame = ttk.Frame(self)
        control_frame.pack(pady=20)
        
        self.start_button = ttk.Button(control_frame, text='Start Demo', command=self.start_demo)
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = ttk.Button(control_frame, text='Stop Demo', command=self.stop_demo)
        self.stop_button.pack(side='left', padx=5)
        
        self.reset_button = ttk.Button(control_frame, text='Reset', command=self.reset_demo)
        self.reset_button.pack(side='left', padx=5)
        
        # Info
        info_text = """
ARROW KEY NAVIGATION ADDED:
• Left/Right arrows: Seek ±1 second
• Shift+Left/Right: Seek ±5 seconds  
• Up/Down arrows: Scroll visualization
• All navigation methods update highlighting immediately
        """
        
        info_label = ttk.Label(self, text=info_text, font=('Arial', 10), 
                              background='lightyellow', relief='ridge', padding=10)
        info_label.pack(fill='x', padx=10, pady=10)
        
    def start_demo(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = time.time()
            self.old_position = 0.0
            self.update_displays()
            
    def stop_demo(self):
        self.is_running = False
        
    def reset_demo(self):
        self.stop_demo()
        self.old_position = 0.0
        self.start_time = None
        self.old_display.config(text='Position: 0.000s')
        self.new_display.config(text='Position: 0.000s')
        self.error_display.config(text='Error: 0.000s')
        
    def update_displays(self):
        if self.is_running and self.start_time:
            # OLD METHOD: Incremental (causes drift)
            self.old_position += 0.1  # This accumulates error
            
            # NEW METHOD: Elapsed time (accurate)
            elapsed_time = time.time() - self.start_time
            
            # Calculate error
            error = abs(self.old_position - elapsed_time)
            
            # Update displays
            self.old_display.config(text=f'Position: {self.old_position:.3f}s')
            self.new_display.config(text=f'Position: {elapsed_time:.3f}s')
            self.error_display.config(text=f'Error: {error:.3f}s')
            
            # Color code the error
            if error > 0.5:
                color = 'red'
            elif error > 0.1:
                color = 'orange'
            else:
                color = 'green'
            self.error_display.config(foreground=color)
            
            # Schedule next update
            self.after(100, self.update_displays)

if __name__ == '__main__':
    demo = TimingDemo()
    demo.mainloop()
