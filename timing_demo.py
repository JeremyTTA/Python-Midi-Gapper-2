#!/usr/bin/env python3
"""
Manual test for resume timing - demonstrates the improved timing logic.
Run this, then pause and resume to test timing accuracy.
"""

import tkinter as tk
from tkinter import messagebox
import pygame
import time

class SimpleTimingDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Resume Timing Test")
        self.root.geometry("400x200")
        
        self.is_playing = False
        self.is_paused = False
        self.playback_start_time = None
        self.playback_position = 0.0
        
        # Initialize pygame mixer
        try:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
            pygame.mixer.init()
            self.mixer_available = True
        except:
            self.mixer_available = False
        
        self.create_widgets()
        self.update_display()
    
    def create_widgets(self):
        # Status display
        self.status_label = tk.Label(self.root, text="Not playing", font=("Arial", 14))
        self.status_label.pack(pady=10)
        
        self.position_label = tk.Label(self.root, text="Position: 0.00s", font=("Arial", 12))
        self.position_label.pack(pady=5)
        
        # Control buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        self.play_button = tk.Button(button_frame, text="Start Simulation", command=self.start_simulation)
        self.play_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = tk.Button(button_frame, text="Pause", command=self.pause_simulation)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.resume_button = tk.Button(button_frame, text="Resume", command=self.resume_simulation)
        self.resume_button.pack(side=tk.LEFT, padx=5)
        
        # Instructions
        instructions = tk.Label(self.root, 
                               text="This simulates the improved resume timing logic.\nWatch for smooth position updates when resuming.",
                               font=("Arial", 10), justify=tk.CENTER)
        instructions.pack(pady=10)
        
        # Space bar binding
        self.root.bind('<space>', lambda e: self.toggle_play_pause())
        self.root.focus_set()
    
    def get_current_position(self):
        """Calculate current position using the improved timing logic"""
        if not self.is_playing or self.playback_start_time is None:
            return self.playback_position
        
        elapsed_time = time.time() - self.playback_start_time
        return elapsed_time
    
    def start_simulation(self):
        """Start the timing simulation"""
        self.playback_start_time = time.time()
        self.playback_position = 0.0
        self.is_playing = True
        self.is_paused = False
        print("Started simulation")
    
    def pause_simulation(self):
        """Pause the simulation"""
        if self.is_playing and not self.is_paused:
            self.playback_position = self.get_current_position()
            self.is_playing = False
            self.is_paused = True
            print(f"Paused at {self.playback_position:.2f}s")
    
    def resume_simulation(self):
        """Resume simulation with improved timing compensation"""
        if self.is_paused:
            # IMPROVED TIMING LOGIC - calculate timing BEFORE any delay
            current_time = time.time()
            
            # Calculate what the start time should be based on current position
            adjusted_start_time = current_time - self.playback_position
            
            # Add compensation for typical resume latency
            unpause_compensation = 0.015  # 15ms compensation
            adjusted_start_time += unpause_compensation
            
            # Apply the timing immediately
            self.playback_start_time = adjusted_start_time
            self.is_playing = True
            self.is_paused = False
            
            print(f"Resumed from {self.playback_position:.2f}s with compensation")
    
    def toggle_play_pause(self):
        """Toggle between play and pause (space bar)"""
        if self.is_paused:
            self.resume_simulation()
        elif self.is_playing:
            self.pause_simulation()
        else:
            self.start_simulation()
    
    def update_display(self):
        """Update the display with current status"""
        if self.is_playing:
            status = "Playing"
        elif self.is_paused:
            status = "Paused"
        else:
            status = "Stopped"
        
        self.status_label.config(text=status)
        
        current_pos = self.get_current_position()
        self.position_label.config(text=f"Position: {current_pos:.2f}s")
        
        # Schedule next update
        self.root.after(50, self.update_display)  # Update every 50ms
    
    def run(self):
        """Run the demo"""
        self.root.mainloop()

if __name__ == "__main__":
    demo = SimpleTimingDemo()
    demo.run()
