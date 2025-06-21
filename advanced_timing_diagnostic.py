"""
Advanced MIDI Timing Diagnostic Tool
Analyzes timing discrepancies between visual and audio positions
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import mido
import pygame
import time
import threading
import os

class MidiTimingDiagnostic(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('MIDI Timing Diagnostic Tool')
        self.geometry('900x700')
        
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
        self.is_paused = False
        self.playback_start_time = None
        self.visual_position_offset = 0.0
        
        # Timing analysis data
        self.timing_log = []
        self.tempo_changes = []
        
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
        ttk.Button(control_frame, text='Analyze Timing', command=self.analyze_timing).pack(side='left', padx=20)
        
        # Position display
        pos_frame = ttk.Frame(control_frame)
        pos_frame.pack(side='left', padx=20)
        
        self.visual_pos_label = ttk.Label(pos_frame, text='Visual: 0.0s', foreground='blue')
        self.visual_pos_label.pack()
        
        self.audio_pos_label = ttk.Label(pos_frame, text='Audio: 0.0s', foreground='green')
        self.audio_pos_label.pack()
        
        self.offset_label = ttk.Label(pos_frame, text='Offset: 0.0s', foreground='red')
        self.offset_label.pack()
        
        # Position scale
        scale_frame = ttk.Frame(self)
        scale_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(scale_frame, text='Position:').pack(side='left')
        self.position_scale = ttk.Scale(scale_frame, from_=0, to=100, 
                                       orient='horizontal', 
                                       command=self.on_position_change)
        self.position_scale.pack(side='left', fill='x', expand=True, padx=5)
        
        # Create notebook for different views
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Timing Analysis Tab
        timing_frame = ttk.Frame(notebook)
        notebook.add(timing_frame, text='Timing Analysis')
        
        self.timing_text = tk.Text(timing_frame, wrap='word', font=('Courier', 10))
        timing_scroll = ttk.Scrollbar(timing_frame, orient='vertical', command=self.timing_text.yview)
        self.timing_text.configure(yscrollcommand=timing_scroll.set)
        
        self.timing_text.pack(side='left', fill='both', expand=True)
        timing_scroll.pack(side='right', fill='y')
        
        # MIDI Structure Tab
        struct_frame = ttk.Frame(notebook)
        notebook.add(struct_frame, text='MIDI Structure')
        
        self.struct_text = tk.Text(struct_frame, wrap='word', font=('Courier', 10))
        struct_scroll = ttk.Scrollbar(struct_frame, orient='vertical', command=self.struct_text.yview)
        self.struct_text.configure(yscrollcommand=struct_scroll.set)
        
        self.struct_text.pack(side='left', fill='both', expand=True)
        struct_scroll.pack(side='right', fill='y')
        
        # Live Timing Tab
        live_frame = ttk.Frame(notebook)
        notebook.add(live_frame, text='Live Timing')
        
        self.live_text = tk.Text(live_frame, wrap='word', font=('Courier', 10))
        live_scroll = ttk.Scrollbar(live_frame, orient='vertical', command=self.live_text.yview)
        self.live_text.configure(yscrollcommand=live_scroll.set)
        
        self.live_text.pack(side='left', fill='both', expand=True)
        live_scroll.pack(side='right', fill='y')
        
        # Start timing monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_timing, daemon=True)
        self.monitor_thread.start()
        
    def load_midi_file(self):
        """Load a MIDI file for analysis"""
        file_path = filedialog.askopenfilename(
            title="Select MIDI file",
            filetypes=[("MIDI files", "*.mid *.midi"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.current_file = file_path
                self.midi_data = mido.MidiFile(file_path)
                self.analyze_midi_structure()
                self.file_label.config(text=f'Loaded: {os.path.basename(file_path)}')
                self.position_scale.config(to=self.max_time)
                
            except Exception as e:
                messagebox.showerror("Error", f"Error loading file: {e}")
                
    def analyze_midi_structure(self):
        """Analyze MIDI file structure and timing"""
        if not self.midi_data:
            return
            
        self.notes = []
        self.tempo_changes = []
        current_time = 0
        tempo_us = 500000  # Default tempo (120 BPM)
        
        # Track active notes for each channel
        active_notes = {}
        
        # Analyze each message
        analysis = []
        analysis.append(f"MIDI File Analysis: {os.path.basename(self.current_file)}")
        analysis.append(f"Ticks per beat: {self.midi_data.ticks_per_beat}")
        analysis.append(f"Number of tracks: {len(self.midi_data.tracks)}")
        analysis.append("=" * 60)
        
        for track_idx, track in enumerate(self.midi_data.tracks):
            analysis.append(f"\nTrack {track_idx}: {track.name or 'Unnamed'}")
            analysis.append(f"Messages: {len(track)}")
            
            track_time = 0
            track_tempo = tempo_us
            
            for msg in track:
                # Calculate time
                delta_time_s = mido.tick2second(msg.time, self.midi_data.ticks_per_beat, track_tempo)
                track_time += delta_time_s
                current_time = max(current_time, track_time)
                
                if msg.type == 'set_tempo':
                    old_tempo = track_tempo
                    track_tempo = msg.tempo
                    tempo_us = msg.tempo  # Update global tempo
                    bpm = mido.tempo2bpm(msg.tempo)
                    self.tempo_changes.append({
                        'time': track_time,
                        'tempo_us': msg.tempo,
                        'bpm': bpm
                    })
                    analysis.append(f"  {track_time:.3f}s: Tempo change from {mido.tempo2bpm(old_tempo):.1f} to {bpm:.1f} BPM")
                    
                elif msg.type == 'note_on' and msg.velocity > 0:
                    key = (msg.channel, msg.note)
                    active_notes[key] = track_time
                    
                elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                    key = (msg.channel, msg.note)
                    if key in active_notes:
                        start_time = active_notes[key]
                        duration = track_time - start_time
                        
                        self.notes.append({
                            'channel': msg.channel,
                            'note': msg.note,
                            'start_time': start_time,
                            'duration': duration,
                            'velocity': getattr(msg, 'velocity', 64)
                        })
                        del active_notes[key]
        
        # Handle remaining active notes
        for key, start_time in active_notes.items():
            self.notes.append({
                'channel': key[0],
                'note': key[1],
                'start_time': start_time,
                'duration': 0.1,
                'velocity': 64
            })
        
        self.max_time = current_time
        
        analysis.append(f"\nTotal duration: {self.max_time:.3f} seconds")
        analysis.append(f"Total notes: {len(self.notes)}")
        analysis.append(f"Tempo changes: {len(self.tempo_changes)}")
        
        if self.tempo_changes:
            analysis.append("\nTempo Change Summary:")
            for i, tempo in enumerate(self.tempo_changes):
                analysis.append(f"  {i+1}. {tempo['time']:.3f}s: {tempo['bpm']:.1f} BPM")
        
        # Display structure analysis
        self.struct_text.delete('1.0', 'end')
        self.struct_text.insert('1.0', '\n'.join(analysis))
        
    def analyze_timing(self):
        """Perform detailed timing analysis"""
        if not self.notes:
            messagebox.showwarning("Warning", "No MIDI file loaded")
            return
            
        analysis = []
        analysis.append("DETAILED TIMING ANALYSIS")
        analysis.append("=" * 50)
        
        # Check for potential timing issues
        if len(self.tempo_changes) > 0:
            analysis.append(f"\n⚠️  TEMPO CHANGES DETECTED: {len(self.tempo_changes)}")
            analysis.append("This can cause timing discrepancies if not handled properly.")
            
            max_tempo_diff = 0
            if len(self.tempo_changes) > 1:
                for i in range(1, len(self.tempo_changes)):
                    diff = abs(self.tempo_changes[i]['bpm'] - self.tempo_changes[i-1]['bpm'])
                    max_tempo_diff = max(max_tempo_diff, diff)
                analysis.append(f"Maximum tempo change: {max_tempo_diff:.1f} BPM")
                
            if max_tempo_diff > 50:
                analysis.append("⚠️  LARGE TEMPO CHANGES detected - high risk of timing issues")
        else:
            analysis.append("✓ No tempo changes - timing should be stable")
            
        # Analyze note distribution
        notes_per_second = len(self.notes) / self.max_time if self.max_time > 0 else 0
        analysis.append(f"\nNote density: {notes_per_second:.1f} notes/second")
        
        if notes_per_second > 20:
            analysis.append("⚠️  HIGH NOTE DENSITY - may affect performance")
            
        # Check for very short or very long notes
        durations = [note['duration'] for note in self.notes]
        min_duration = min(durations) if durations else 0
        max_duration = max(durations) if durations else 0
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        analysis.append(f"\nNote durations:")
        analysis.append(f"  Minimum: {min_duration:.3f}s")
        analysis.append(f"  Maximum: {max_duration:.3f}s")
        analysis.append(f"  Average: {avg_duration:.3f}s")
        
        if min_duration < 0.01:
            analysis.append("⚠️  VERY SHORT NOTES detected - may cause highlighting issues")
            
        # Calculate expected timing accuracy
        analysis.append(f"\nExpected timing accuracy:")
        if len(self.tempo_changes) == 0:
            analysis.append("✓ EXCELLENT - No tempo changes, should be very accurate")
        elif len(self.tempo_changes) <= 5:
            analysis.append("✓ GOOD - Few tempo changes, should be accurate")
        else:
            analysis.append("⚠️  MODERATE - Many tempo changes, potential for drift")
            
        # Check MIDI file characteristics
        ticks_per_beat = self.midi_data.ticks_per_beat
        analysis.append(f"\nMIDI Resolution: {ticks_per_beat} ticks/beat")
        
        if ticks_per_beat < 96:
            analysis.append("⚠️  LOW RESOLUTION - may affect timing precision")
        elif ticks_per_beat >= 480:
            analysis.append("✓ HIGH RESOLUTION - excellent timing precision")
        else:
            analysis.append("✓ STANDARD RESOLUTION - good timing precision")
            
        self.timing_text.delete('1.0', 'end')
        self.timing_text.insert('1.0', '\n'.join(analysis))
        
    def get_actual_audio_position(self):
        """Calculate actual audio position with pygame limitations"""
        if not self.is_playing or self.playback_start_time is None:
            return self.playback_position
            
        elapsed_time = time.time() - self.playback_start_time
        
        if self.visual_position_offset > 0.1:
            # Seeking case
            audio_position = elapsed_time
            if audio_position < self.visual_position_offset:
                return -1  # Audio hasn't caught up yet
            else:
                return self.visual_position_offset + elapsed_time
        else:
            # Normal playback
            return elapsed_time
            
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
                if self.is_paused:
                    pygame.mixer.music.unpause()
                    self.is_paused = False
                else:
                    pygame.mixer.music.load(self.current_file)
                    pygame.mixer.music.play(start=self.playback_position)
                    self.visual_position_offset = self.playback_position
                
                self.is_playing = True
                self.playback_start_time = time.time()
                
            except Exception as e:
                messagebox.showerror("Error", f"Playback error: {e}")
        
    def pause(self):
        """Pause playback"""
        if self.is_playing and self.midi_available:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.is_paused = True
            
    def stop(self):
        """Stop playback"""
        if self.midi_available:
            pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.playback_position = 0.0
        self.position_scale.set(0)
        
    def monitor_timing(self):
        """Monitor timing in real-time"""
        while True:
            try:
                if self.is_playing:
                    # Calculate positions
                    visual_pos = self.playback_position + (time.time() - self.playback_start_time) if self.playback_start_time else self.playback_position
                    audio_pos = self.get_actual_audio_position()
                    
                    # Update position scale
                    self.position_scale.set(visual_pos)
                    self.playback_position = visual_pos
                    
                    # Update labels
                    self.visual_pos_label.config(text=f'Visual: {visual_pos:.3f}s')
                    if audio_pos >= 0:
                        self.audio_pos_label.config(text=f'Audio: {audio_pos:.3f}s')
                        offset = visual_pos - audio_pos
                        self.offset_label.config(text=f'Offset: {offset:.3f}s')
                        
                        # Color code offset
                        if abs(offset) > 5.0:
                            color = 'red'
                        elif abs(offset) > 1.0:
                            color = 'orange'
                        else:
                            color = 'green'
                        self.offset_label.config(foreground=color)
                        
                        # Log significant offsets
                        if abs(offset) > 1.0:
                            log_entry = f"{time.strftime('%H:%M:%S')} - Large offset: {offset:.3f}s (Visual: {visual_pos:.3f}s, Audio: {audio_pos:.3f}s)\n"
                            self.after(0, lambda: self.live_text.insert('end', log_entry))
                            self.after(0, lambda: self.live_text.see('end'))
                    else:
                        self.audio_pos_label.config(text='Audio: catching up...')
                        self.offset_label.config(text='Offset: waiting...')
                else:
                    self.visual_pos_label.config(text=f'Visual: {self.playback_position:.3f}s')
                    self.audio_pos_label.config(text='Audio: stopped')
                    self.offset_label.config(text='Offset: N/A')
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                
            time.sleep(0.1)

if __name__ == '__main__':
    app = MidiTimingDiagnostic()
    app.mainloop()
