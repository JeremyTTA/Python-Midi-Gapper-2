"""
Test timing consistency with different MIDI files and arrow key navigation
"""
import tkinter as tk
from tkinter import ttk, filedialog
import time
import threading
import pygame
import mido
import traceback

class TimingTestGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Timing Consistency Test')
        self.geometry('800x600')
        
        # Initialize pygame
        try:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
            pygame.mixer.init()
            self.midi_available = True
        except:
            self.midi_available = False
        
        # State variables
        self.current_file = None
        self.midi_data = None
        self.notes = []
        self.max_time = 0
        self.playback_position = 0.0
        self.is_playing = False
        self.playback_start_time = None
        self.visual_position_offset = 0.0
        
        self.setup_ui()
        
    def setup_ui(self):
        # File selection
        file_frame = ttk.Frame(self)
        file_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(file_frame, text='Load MIDI File', 
                  command=self.load_midi_file).pack(side='left', padx=5)
        
        self.file_label = ttk.Label(file_frame, text='No file loaded')
        self.file_label.pack(side='left', padx=10)
        
        # Control frame
        control_frame = ttk.Frame(self)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(control_frame, text='Play', command=self.play).pack(side='left', padx=5)
        ttk.Button(control_frame, text='Pause', command=self.pause).pack(side='left', padx=5)
        ttk.Button(control_frame, text='Stop', command=self.stop).pack(side='left', padx=5)
        
        # Position display
        self.position_label = ttk.Label(control_frame, text='Position: 0.0s')
        self.position_label.pack(side='left', padx=20)
        
        # Timing info display
        info_frame = ttk.Frame(self)
        info_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create text widget for timing info
        self.info_text = tk.Text(info_frame, wrap='word')
        scroll = ttk.Scrollbar(info_frame, orient='vertical', command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scroll.set)
        
        self.info_text.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
        
        # Position scale
        scale_frame = ttk.Frame(self)
        scale_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(scale_frame, text='Position:').pack(side='left')
        self.position_scale = ttk.Scale(scale_frame, from_=0, to=100, 
                                       orient='horizontal', 
                                       command=self.on_position_change)
        self.position_scale.pack(side='left', fill='x', expand=True, padx=5)
        
        # Bind arrow keys for navigation
        self.focus_set()
        self.bind('<Left>', lambda e: self.seek_relative(-1.0))
        self.bind('<Right>', lambda e: self.seek_relative(1.0))
        self.bind('<Shift-Left>', lambda e: self.seek_relative(-5.0))
        self.bind('<Shift-Right>', lambda e: self.seek_relative(5.0))
        
        # Start timing update thread
        self.update_thread = threading.Thread(target=self.update_timing_info, daemon=True)
        self.update_thread.start()
        
    def load_midi_file(self):
        """Load a MIDI file for testing"""
        file_path = filedialog.askopenfilename(
            title="Select MIDI file",
            filetypes=[("MIDI files", "*.mid *.midi"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.current_file = file_path
                self.midi_data = mido.MidiFile(file_path)
                self.analyze_midi_file()
                self.file_label.config(text=f'Loaded: {file_path.split("/")[-1]}')
                self.position_scale.config(to=self.max_time)
                self.log_info(f"Loaded MIDI file: {file_path}")
                self.log_info(f"Duration: {self.max_time:.2f}s")
                self.log_info(f"Number of tracks: {len(self.midi_data.tracks)}")
                self.log_info(f"Ticks per beat: {self.midi_data.ticks_per_beat}")
                
            except Exception as e:
                self.log_info(f"Error loading file: {e}")
                
    def analyze_midi_file(self):
        """Analyze MIDI file for timing information"""
        if not self.midi_data:
            return
            
        self.notes = []
        current_time = 0
        tempo_us = 500000  # Default tempo (120 BPM)
        
        # Track active notes for each channel
        active_notes = {}
        
        for msg in self.midi_data:
            # Update time
            delta_time_s = mido.tick2second(msg.time, self.midi_data.ticks_per_beat, tempo_us)
            current_time += delta_time_s
            
            if msg.type == 'set_tempo':
                tempo_us = msg.tempo
                
            elif msg.type == 'note_on' and msg.velocity > 0:
                key = (msg.channel, msg.note)
                active_notes[key] = current_time
                
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                key = (msg.channel, msg.note)
                if key in active_notes:
                    start_time = active_notes[key]
                    duration = current_time - start_time
                    
                    self.notes.append({
                        'channel': msg.channel,
                        'note': msg.note,
                        'start_time': start_time,
                        'duration': duration,
                        'velocity': getattr(msg, 'velocity', 64)
                    })
                    del active_notes[key]
        
        # Handle any remaining active notes
        for key, start_time in active_notes.items():
            self.notes.append({
                'channel': key[0],
                'note': key[1],
                'start_time': start_time,
                'duration': 0.1,  # Default short duration
                'velocity': 64
            })
        
        self.max_time = current_time
        
    def seek_relative(self, delta_seconds):
        """Seek relative to current position"""
        new_position = max(0, min(self.playback_position + delta_seconds, self.max_time))
        self.playback_position = new_position
        self.position_scale.set(new_position)
        
        # If playing, handle seeking
        if self.is_playing:
            self.visual_position_offset = new_position
            self.playback_start_time = time.time()
            
        self.log_info(f"Seek to: {new_position:.2f}s (delta: {delta_seconds:+.1f}s)")
        
    def on_position_change(self, value):
        """Handle position scale change"""
        self.playback_position = float(value)
        
        if self.is_playing:
            self.visual_position_offset = self.playback_position
            self.playback_start_time = time.time()
            
    def play(self):
        """Start playback"""
        if not self.current_file:
            return
            
        if self.midi_available:
            try:
                pygame.mixer.music.load(self.current_file)
                pygame.mixer.music.play(start=self.playback_position)
                self.is_playing = True
                self.playback_start_time = time.time()
                self.visual_position_offset = self.playback_position
                self.log_info(f"Started playback from {self.playback_position:.2f}s")
            except Exception as e:
                self.log_info(f"Playback error: {e}")
        
    def pause(self):
        """Pause playback"""
        if self.is_playing and self.midi_available:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.log_info("Paused playback")
            
    def stop(self):
        """Stop playback"""
        if self.midi_available:
            pygame.mixer.music.stop()
        self.is_playing = False
        self.playback_position = 0.0
        self.position_scale.set(0)
        self.log_info("Stopped playback")
        
    def get_actual_audio_position(self):
        """Calculate actual audio position with pygame seeking limitation"""
        if not self.is_playing or self.playback_start_time is None:
            return self.playback_position
            
        elapsed_time = time.time() - self.playback_start_time
        
        if self.visual_position_offset > 0.1:
            # Seeking: audio starts from 0, visual offset
            audio_position = elapsed_time
            return audio_position if audio_position >= self.visual_position_offset else -1
        else:
            # Normal playback
            return self.playback_position + elapsed_time
            
    def get_notes_at_time(self, time_pos):
        """Get notes playing at given time"""
        playing_notes = []
        for note in self.notes:
            if note['start_time'] <= time_pos <= note['start_time'] + note['duration']:
                playing_notes.append(note)
        return playing_notes
        
    def update_timing_info(self):
        """Update timing information display"""
        while True:
            try:
                if self.is_playing:
                    # Update position during playback
                    audio_pos = self.get_actual_audio_position()
                    visual_pos = self.playback_position + (time.time() - self.playback_start_time) if self.playback_start_time else self.playback_position
                    
                    # Update scale
                    self.position_scale.set(visual_pos)
                    self.playback_position = visual_pos
                    
                    # Update display
                    self.position_label.config(text=f'Position: {visual_pos:.2f}s')
                    
                    # Get timing info
                    visual_notes = self.get_notes_at_time(visual_pos)
                    audio_notes = self.get_notes_at_time(audio_pos) if audio_pos >= 0 else []
                    
                    # Show timing analysis
                    if audio_pos >= 0:
                        timing_diff = visual_pos - audio_pos
                        timing_info = f"Visual: {visual_pos:.3f}s | Audio: {audio_pos:.3f}s | Diff: {timing_diff:.3f}s\n"
                        timing_info += f"Visual notes: {len(visual_notes)} | Audio notes: {len(audio_notes)}\n"
                        timing_info += f"Offset: {self.visual_position_offset:.3f}s\n"
                    else:
                        timing_info = f"Visual: {visual_pos:.3f}s | Audio: catching up...\n"
                        timing_info += f"Visual notes: {len(visual_notes)} | Audio notes: waiting\n"
                        timing_info += f"Offset: {self.visual_position_offset:.3f}s\n"
                        
                    # Update info display (throttled)
                    if hasattr(self, '_last_info_update'):
                        if time.time() - self._last_info_update > 0.1:  # Update every 100ms
                            self.after(0, lambda: self.info_text.insert('end', timing_info))
                            self.after(0, lambda: self.info_text.see('end'))
                            self._last_info_update = time.time()
                    else:
                        self._last_info_update = time.time()
                        
                else:
                    self.position_label.config(text=f'Position: {self.playback_position:.2f}s')
                
            except Exception as e:
                print(f"Timing update error: {e}")
                
            time.sleep(0.05)  # 20 FPS update
            
    def log_info(self, message):
        """Log information to the text widget"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.after(0, lambda: self.info_text.insert('end', log_message))
        self.after(0, lambda: self.info_text.see('end'))

if __name__ == '__main__':
    app = TimingTestGUI()
    app.mainloop()
