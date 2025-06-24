import tkinter as tk
from tkinter import ttk, filedialog
import os
import json
import mido
import xml.etree.ElementTree as ET
from xml.dom import minidom
import random
import shutil
import traceback
from tkinter import messagebox
from mido import MidiFile, MidiTrack
import tkinter.font as tkfont
import threading
import time

# Predefined distinct colors for channels
DEFAULT_CHANNEL_COLORS = [    '#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4',
    '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff',
    '#9a6324', '#fffac8', '#800000', '#aaffc3'
]

# General MIDI instrument names
GM_INSTRUMENTS = [
    'Acoustic Grand Piano','Bright Acoustic Piano','Electric Grand Piano','Honky-tonk Piano',
    'Electric Piano 1','Electric Piano 2','Harpsichord','Clavinet','Celesta','Glockenspiel',
    'Music Box','Vibraphone','Marimba','Xylophone','Tubular Bells','Dulcimer',
    'Drawbar Organ','Percussive Organ','Rock Organ','Church Organ','Reed Organ','Accordion',
    'Harmonica','Tango Accordion','Acoustic Guitar (nylon)','Acoustic Guitar (steel)',
    'Electric Guitar (jazz)','Electric Guitar (clean)','Electric Guitar (muted)','Overdriven Guitar',
    'Distortion Guitar','Guitar harmonics','Acoustic Bass','Electric Bass (finger)','Electric Bass (pick)',
    'Fretless Bass','Slap Bass 1','Slap Bass 2','Synth Bass 1','Synth Bass 2',
    'Violin','Viola','Cello','Contrabass','Tremolo Strings','Pizzicato Strings','Orchestral Harp','Timpani',
    'String Ensemble 1','String Ensemble 2','SynthStrings 1','SynthStrings 2','Choir Aahs','Voice Oohs','Synth Voice','Orchestra Hit',
    'Trumpet','Trombone','Tuba','Muted Trumpet','French Horn','Brass Section','SynthBrass 1','SynthBrass 2',
    'Soprano Sax','Alto Sax','Tenor Sax','Baritone Sax','Oboe','English Horn','Bassoon','Clarinet',
    'Piccolo','Flute','Recorder','Pan Flute','Blown bottle','Shakuhachi','Whistle','Ocarina',
    'Lead 1 (square)','Lead 2 (sawtooth)','Lead 3 (calliope)','Lead 4 (chiff)','Lead 5 (charang)','Lead 6 (voice)','Lead 7 (fifths)','Lead 8 (bass + lead)',
    'Pad 1 (new age)','Pad 2 (warm)','Pad 3 (polysynth)','Pad 4 (choir)','Pad 5 (bowed)','Pad 6 (metallic)','Pad 7 (halo)','Pad 8 (sweep)',
    'FX 1 (rain)','FX 2 (soundtrack)','FX 3 (crystal)','FX 4 (atmosphere)','FX 5 (brightness)','FX 6 (goblins)','FX 7 (echoes)','FX 8 (sci-fi)',
    'Sitar','Banjo','Shamisen','Koto','Kalimba','Bag pipe','Fiddle','Shanai',
    'Tinkle Bell','Agogo','Steel Drums','Woodblock','Taiko Drum','Melodic Tom','Synth Drum','Reverse Cymbal',
    'Guitar Fret Noise','Breath Noise','Seashore','Bird Tweet','Telephone Ring','Helicopter','Applause','Gunshot'
]

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

class FluidSynthPlayer:
    """MIDI note player using FluidSynth software synthesizer"""
    def __init__(self, soundfont_path=None):
        self.fs = None
        self.midi_out = None  # Keep for compatibility with existing code
        self.soundfont_path = soundfont_path
        self.initialize_fluidsynth()
    
    def initialize_fluidsynth(self):
        """Initialize FluidSynth with comprehensive diagnostics"""
        print("\n=== FluidSynth Setup Diagnostics ===")
        
        try:
            import fluidsynth
            print("✓ FluidSynth imported successfully")
            
            # Create FluidSynth instance
            self.fs = fluidsynth.Synth()
            self.fs.start(driver="dsound")  # Use DirectSound on Windows
            print("✓ FluidSynth synthesizer started")
            
            # Load a soundfont
            soundfont_loaded = False
            
            # Try user-specified soundfont first
            if self.soundfont_path and os.path.exists(self.soundfont_path):
                try:
                    sfid = self.fs.sfload(self.soundfont_path)
                    self.fs.program_select(0, sfid, 0, 0)  # Channel 0, Bank 0, Preset 0
                    print(f"✓ Loaded custom soundfont: {self.soundfont_path}")
                    soundfont_loaded = True
                except Exception as e:
                    print(f"⚠ Failed to load custom soundfont: {e}")
            
            # Try common Windows soundfont locations
            if not soundfont_loaded:
                common_locations = [
                    "C:/Windows/System32/drivers/gm.dls",
                    "C:/Windows/SysWOW64/drivers/gm.dls",
                    "default.sf2",  # FluidSynth might have a default
                ]
                
                for location in common_locations:
                    if os.path.exists(location):
                        try:
                            sfid = self.fs.sfload(location)
                            self.fs.program_select(0, sfid, 0, 0)
                            print(f"✓ Loaded soundfont: {location}")
                            soundfont_loaded = True
                            break
                        except Exception as e:
                            print(f"⚠ Failed to load {location}: {e}")
            
            if not soundfont_loaded:
                print("⚠ No soundfont loaded - will use FluidSynth's built-in sounds")
                # FluidSynth can still work without a soundfont using built-in samples
            
            # Set this as available for compatibility
            self.midi_out = self  # Self-reference to indicate MIDI is available
            
            # Test with a quick note
            try:
                self.fs.noteon(0, 60, 30)  # Channel 0, Middle C, velocity 30
                time.sleep(0.1)
                self.fs.noteoff(0, 60)
                print("✓ FluidSynth test note played successfully")
            except Exception as test_e:
                print(f"⚠ FluidSynth initialized but test failed: {test_e}")
            
            print("✓ FluidSynth MIDI playback ready!")
                
        except ImportError as e:
            print(f"✗ FluidSynth import failed: {e}")
            self._print_fluidsynth_setup_instructions()
            self.fs = None
            self.midi_out = None
        except Exception as e:
            print(f"✗ Failed to initialize FluidSynth: {e}")
            self.fs = None
            self.midi_out = None
            
        print("=====================================\n")
    
    def _print_fluidsynth_setup_instructions(self):
        """Print FluidSynth installation instructions"""
        print("\n📋 FluidSynth Setup Instructions:")
        print("1. Install FluidSynth:")
        print("   pip install pyfluidsynth")
        print("")
        print("2. Optional - Download a soundfont for better audio quality:")
        print("   • Download a General MIDI soundfont (.sf2 file)")
        print("   • Popular free soundfonts: FluidR3_GM.sf2, TimGM6mb.sf2")
        print("   • Place in your project folder or specify path")
        print("")
        print("3. FluidSynth will work with built-in sounds even without a soundfont")
        print("")
        print("🔄 Restart the application after installing pyfluidsynth")
        print("📖 The visualization will still work without MIDI audio")
    
    def _note_on(self, channel, note, velocity=64):
        """Send a note-on message"""
        if self.fs:
            try:
                self.fs.noteon(channel, note, velocity)
            except Exception as e:
                print(f"Error sending note_on: {e}")
    
    def _note_off(self, channel, note):
        """Send a note-off message"""
        if self.fs:
            try:
                self.fs.noteoff(channel, note)
            except Exception as e:
                print(f"Error sending note_off: {e}")
    
    def close(self):
        """Close the FluidSynth synthesizer"""
        if self.fs:
            try:
                self.fs.delete()
            except:
                pass
            self.fs = None
            self.midi_out = None

# Keep the old MidiNotePlayer as an alias for backwards compatibility
MidiNotePlayer = FluidSynthPlayer

class MidiGapperGUI(tk.Tk):
    # Map MIDI note number to note name
    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def __init__(self):
        super().__init__()
        
        # Enable debug timing output for troubleshooting
        self.debug_timing = True
        
        self.title('Python Midi Gapper 2')
          # Initialize MIDI playback systems
        self.init_midi_playback()
        
        # MIDI playback state
        self.playback_start_time = None  # When playback actually started
        
        # Scrolling performance optimization for large MIDI files
        self.scroll_update_timer = None
        self.scroll_throttle_delay = 100  # ms delay for highlighting updates during scroll
        self.last_highlight_time = 0  # Track when highlighting was last updated
        
        # Load window geometry
        self.config_data = load_config()
        # Default tempo in microseconds per quarter note
        self.tempo_us = 500000        # Y-scale multiplier for visualization
        y_scale = self.config_data.get('y_scale', 1.0)
        self.y_scale_var = tk.DoubleVar(value=y_scale)
        
        geometry = self.config_data.get('geometry')
        if geometry:
            self.geometry(geometry)
            
        # Initialize state
        self.current_midi_file = None
        self.midi_data = None
        self.deleted_channels = set()
        self.modifications_applied = False
        self.notes_for_visualization = []
        
        # Keyboard highlighting state
        self.keyboard_keys = {}  # MIDI note number -> canvas object ID for highlighting
        self.notes = []
        self.max_time = 1
        # Variables for channel visibility checkboxes
        self.channel_vars = {}
        # Scroll control: flag to scroll to bottom on next draw
        self.scroll_to_bottom_on_next_draw = False
        # Create UI
        self.create_widgets()
        # Define visualization text font with default size for clarity
        default_font = tkfont.nametofont("TkDefaultFont")
        new_size = default_font.cget("size")  # use standard size
        self.vis_font = tkfont.Font(family=default_font.cget("family"), size=new_size)        # Initialize channel-color and instrument mapping
        self.channel_colors = {}
        self.channel_instruments = {}
        
        # Autoload last MIDI file if available
        last = self.config_data.get('last_midi')
        if last and os.path.exists(last):
            # Delay autoload until GUI is complete and force scroll to bottom
            def delayed_autoload():
                self.process_midi(last)
                # Force scroll to bottom with multiple attempts to ensure it sticks
                def force_scroll():
                    if self.canvas.winfo_width() > 1:  # ensure canvas is sized
                        self.canvas.yview_moveto(1.0)
                        print(f"Scrolled to bottom, yview: {self.canvas.canvasy(0)}")
                    else:
                        self.after(100, force_scroll)  # retry if not ready
                self.after(100, force_scroll)
                self.after(300, force_scroll)
                self.after(500, force_scroll)
            self.after_idle(delayed_autoload)
        
        # Restore window state (maximized/normal) after widgets are created
        window_state = self.config_data.get('window_state', 'normal')
        if window_state == 'zoomed':  # 'zoomed' is Tkinter's term for maximized
            self.state('zoomed')
            
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Force window to come to front
        self.lift()
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))
        self.focus_force()

    def init_midi_playback(self):
        """Initialize MIDI playback system using note-based output"""
        self.midi_playback_available = False
        
        # Initialize note-based MIDI player for highlighting-driven playback
        try:
            # Initialize without a specific device first, will be set later
            self.note_player = MidiNotePlayer()
            if self.note_player.midi_out:
                self.midi_playback_available = True
                print("✓ Note-based MIDI player initialized successfully")
            else:
                print("⚠ Note-based MIDI player available but no output device")
                self.midi_playback_available = False
        except Exception as e:
            print(f"⚠ Could not initialize note-based MIDI player: {e}")
            self.note_player = None
            self.midi_playback_available = False

    def create_widgets(self):
        # Configure default TTK styles (removed black styling)
        style = ttk.Style()
        
        # Combined top section with all controls, MIDI info, and channel list
        top_section = ttk.Frame(self)
        top_section.pack(side='top', fill='x', padx=5, pady=5)
          # Left side: Controls
        controls_frame = ttk.Frame(top_section)
        controls_frame.pack(side='left', anchor='nw', padx=(0, 10))
        
        # Controls label
        controls_label = ttk.Label(controls_frame, text='Controls:')
        controls_label.pack(side='top', anchor='w', pady=(0, 5))
        
        # Open MIDI button
        open_button = ttk.Button(controls_frame, text='Open MIDI File', command=self.load_midi_file)
        open_button.pack(side='top', pady=(0, 3), anchor='w')
          # Save MIDI button
        save_button = ttk.Button(controls_frame, text='Save MIDI As...', command=self.save_midi_file)
        save_button.pack(side='top', pady=(0, 3), anchor='w')
        
        # Gap controls in separate frame
        gap_controls_frame = ttk.LabelFrame(top_section, text='Gap Controls')
        gap_controls_frame.pack(side='left', anchor='nw', padx=(10, 10))
        
        # Gap controls frame
        gap_frame = ttk.Frame(gap_controls_frame)
        gap_frame.pack(side='top', pady=(5, 5), anchor='w')
        ttk.Label(gap_frame, text='Gap (ms):').pack(side='left', padx=(0, 5))
        self.gap_var = tk.StringVar(value='50')
        gap_entry = ttk.Entry(gap_frame, textvariable=self.gap_var, width=6)
        gap_entry.pack(side='left')
          # Create Gaps button
        create_gaps_button = ttk.Button(gap_controls_frame, text='Create Gaps', command=self.create_gaps)
        create_gaps_button.pack(side='top', pady=(0, 5), anchor='w')
          # MIDI Play Controls
        play_controls_frame = ttk.LabelFrame(top_section, text='MIDI Player')
        play_controls_frame.pack(side='left', anchor='nw', padx=(10, 10))
        
        # Play control buttons - larger and more traditional
        buttons_frame = ttk.Frame(play_controls_frame)
        buttons_frame.pack(side='top', pady=(10, 10), anchor='w')
        
        # Rewind to start button (left of play)
        self.rewind_button = tk.Button(buttons_frame, text='⏮', width=4, height=2, 
                                     font=('Arial', 16, 'bold'), command=self.rewind_to_start,
                                     bg='lightgray', relief='raised', bd=3)
        self.rewind_button.pack(side='left', padx=(0, 5))
        
        # Main play/pause button (toggles between play ▶ and pause ⏸)
        self.play_pause_button = tk.Button(buttons_frame, text='▶', width=4, height=2,
                                         font=('Arial', 20, 'bold'), command=self.toggle_play_pause,
                                         bg='lightgreen', relief='raised', bd=3)
        self.play_pause_button.pack(side='left', padx=(0, 5))
        
        # Stop button
        self.stop_button = tk.Button(buttons_frame, text='⏹', width=4, height=2,
                                   font=('Arial', 16, 'bold'), command=self.stop_midi,
                                   bg='lightcoral', relief='raised', bd=3)
        self.stop_button.pack(side='left', padx=(0, 5))
        
        # Enhanced LED-style position clock (larger and to the right)
        clock_frame = ttk.Frame(buttons_frame)
        clock_frame.pack(side='left', padx=(15, 0))
        
        # Position label
        position_label = tk.Label(clock_frame, text='Position:', font=('Arial', 10, 'bold'))
        position_label.pack(side='top', anchor='w')
          # Larger LED display canvas (increased width to accommodate full time string)
        self.led_clock = tk.Canvas(clock_frame, width=200, height=40, bg='black', 
                                 highlightthickness=2, highlightbackground='gray',
                                 relief='sunken', bd=2)
        self.led_clock.pack(side='top', pady=(3, 0))
        
        # Initialize playback variables
        self.is_playing = False
        self.is_paused = False
        self.playback_position = 0.0
        self.playback_timer = None
          # Draw initial LED display
        self.update_led_clock()
        
        # MIDI Output Device Selector (below play controls)
        midi_device_frame = ttk.Frame(play_controls_frame)
        midi_device_frame.pack(side='top', pady=(5, 5), anchor='w')
        
        # Device selector label
        device_label = ttk.Label(midi_device_frame, text='MIDI Output:')
        device_label.pack(side='top', anchor='w', pady=(0, 2))
        
        # Device selection frame with dropdown and status indicator
        device_select_frame = ttk.Frame(midi_device_frame)
        device_select_frame.pack(side='top', anchor='w')
        
        # MIDI output dropdown
        self.midi_output_var = tk.StringVar()
        self.midi_output_dropdown = ttk.Combobox(device_select_frame, textvariable=self.midi_output_var,
                                                width=25, state='readonly')
        self.midi_output_dropdown.pack(side='left', padx=(0, 5))
        self.midi_output_dropdown.bind('<<ComboboxSelected>>', self.on_midi_output_changed)
        
        # Connection status indicator (green/red circle)
        self.status_canvas = tk.Canvas(device_select_frame, width=16, height=16, bg=self.cget('bg'),
                                      highlightthickness=0)
        self.status_canvas.pack(side='left')
        
        # Refresh button to rescan MIDI devices
        refresh_button = ttk.Button(device_select_frame, text='🔄', width=3,
                                   command=self.refresh_midi_devices)
        refresh_button.pack(side='left', padx=(5, 0))
        
        # Initialize MIDI device list and status
        self.refresh_midi_devices()
        
        # Center: MIDI info display
        info_frame = ttk.Frame(top_section)
        info_frame.pack(side='left', expand=True, fill='x', padx=(0, 10))
        
        # MIDI Info title with enhanced styling
        title_label = tk.Label(info_frame, text='MIDI Info:', 
                              font=('Arial', 12, 'bold'), 
                              fg='blue', bg=self.cget('bg'))
        title_label.pack(side='top')
        
        # Container for MIDI info details
        details_frame = ttk.Frame(info_frame)
        details_frame.pack(side='top', fill='x', pady=(5, 0))
        
        # Individual info variables and labels
        self.midi_filename_var = tk.StringVar(value='No MIDI file loaded')
        self.midi_tracks_var = tk.StringVar(value='')
        self.midi_format_var = tk.StringVar(value='')
        self.midi_ticks_var = tk.StringVar(value='')
        self.midi_tempo_var = tk.StringVar(value='')
        self.midi_duration_var = tk.StringVar(value='')
        
        # Create info labels
        filename_label = ttk.Label(details_frame, textvariable=self.midi_filename_var, 
                                  anchor='center', justify='center', font=('Arial', 10, 'bold'))
        filename_label.pack(side='top', fill='x')
        
        tracks_label = ttk.Label(details_frame, textvariable=self.midi_tracks_var, 
                                anchor='center', justify='center')
        tracks_label.pack(side='top', fill='x')
        
        format_label = ttk.Label(details_frame, textvariable=self.midi_format_var, 
                                anchor='center', justify='center')
        format_label.pack(side='top', fill='x')
        
        ticks_label = ttk.Label(details_frame, textvariable=self.midi_ticks_var, 
                               anchor='center', justify='center')
        ticks_label.pack(side='top', fill='x')
        
        tempo_label = ttk.Label(details_frame, textvariable=self.midi_tempo_var, 
                               anchor='center', justify='center')
        tempo_label.pack(side='top', fill='x')
        
        duration_label = ttk.Label(details_frame, textvariable=self.midi_duration_var, 
                                  anchor='center', justify='center')
        duration_label.pack(side='top', fill='x')# Right side: Expandable Channel legend
        self.channel_frame = ttk.LabelFrame(top_section, text='Channels')
        self.channel_frame.pack(side='right', anchor='ne', padx=(0, 100))
        
        # Create a scrollable frame for channels with height limitation
        self.channel_canvas = tk.Canvas(self.channel_frame, highlightthickness=0)
        self.channel_scrollbar = ttk.Scrollbar(self.channel_frame, orient="vertical", command=self.channel_canvas.yview)
        self.channel_scrollable_frame = ttk.Frame(self.channel_canvas)
        
        # Configure the canvas
        self.channel_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.channel_canvas.configure(scrollregion=self.channel_canvas.bbox("all"))
        )
        self.channel_canvas.create_window((0, 0), window=self.channel_scrollable_frame, anchor="nw")
        self.channel_canvas.configure(yscrollcommand=self.channel_scrollbar.set)
          # Set initial collapsed height (for ~3 items, each ~20px)
        self.collapsed_height = 65
        self.expanded_height = 200  # Will be adjusted based on content
        self.channel_canvas.configure(height=self.collapsed_height, width=280)
        
        # Pack canvas and scrollbar
        self.channel_canvas.pack(side="left", fill="both", expand=True)
        self.channel_scrollbar.pack(side="right", fill="y")
        
        # Bind mouse events for hover expansion
        self.bind_hover_events(self.channel_frame)
        self.bind_hover_events(self.channel_canvas)
        self.bind_hover_events(self.channel_scrollable_frame)
        
        # Store reference to actual channel content frame
        self.channel_content_frame = self.channel_scrollable_frame

        # Notebook for tabs
        notebook = ttk.Notebook(self)
        notebook.pack(side='bottom', fill='both', expand=True)        # Visualization tab
        vis_frame = ttk.Frame(notebook)
        notebook.add(vis_frame, text='Visualization')
        # Y-scale control above visualization
        scale_frame = ttk.Frame(vis_frame)
        scale_frame.pack(side='top', fill='x', padx=5, pady=(0,5))
        ttk.Label(scale_frame, text='Y-Scale:').pack(side='left')
        y_entry = ttk.Entry(scale_frame, textvariable=self.y_scale_var, width=5)
        y_entry.pack(side='left')
        # Redraw visualization when Y-scale changes
        self.y_scale_var.trace_add('write', lambda *args: self.draw_visualization(self.notes, self.max_time))
          # Container for canvas and scrollbar
        canvas_container = ttk.Frame(vis_frame)
        canvas_container.pack(fill='both', expand=True)
        
        # Main canvas container (visualization + keyboard)
        main_canvas_frame = ttk.Frame(canvas_container)
        main_canvas_frame.pack(fill='both', expand=True, side='left')
        
        # Visualization canvas with original white background
        self.canvas = tk.Canvas(main_canvas_frame, bg='black', yscrollincrement=1)
        self.canvas.pack(fill='both', expand=True)
          # Keyboard canvas underneath (fixed height, Synthesia style) - 2x scale
        self.keyboard_canvas = tk.Canvas(main_canvas_frame, bg='#2a2a2a', height=200)
        self.keyboard_canvas.pack(fill='x', side='bottom')
          # Vertical scrollbar for visualization with MIDI position sync
        v_scroll = ttk.Scrollbar(canvas_container, orient='vertical', command=self.on_scroll_with_midi_sync)
        v_scroll.pack(fill='y', side='right')
        self.canvas.configure(yscrollcommand=v_scroll.set)
          # Redraw visualization on canvas resize (fix autoload sizing issues)
        def on_canvas_configure(event):
            # Don't scroll to bottom on resize events, only on initial load
            if hasattr(self, 'notes') and self.notes:
                self.draw_visualization(self.notes, self.max_time)
        self.canvas.bind('<Configure>', on_canvas_configure)
        
        # Redraw keyboard on resize
        def on_keyboard_configure(event):
            self.draw_keyboard()
        self.keyboard_canvas.bind('<Configure>', on_keyboard_configure)        # Enable scrolling of visualization with mouse wheel and arrow keys
        self.canvas.bind('<Enter>', lambda e: self.canvas.focus_set())
        
        # Increase scroll speed by using a multiplier for faster scrolling
        scroll_factor = 75  # Increased for better performance with large MIDI files
        self.bind_all('<MouseWheel>', lambda e: self.on_scroll_with_midi_sync('scroll', -scroll_factor * int(e.delta/120), 'units'))
        self.bind_all('<Up>', lambda e: self.on_scroll_with_midi_sync('scroll', -scroll_factor, 'units'))
        self.bind_all('<Down>', lambda e: self.on_scroll_with_midi_sync('scroll', scroll_factor, 'units'))
          # Add left/right arrow keys for time-based seeking
        self.bind_all('<Left>', lambda e: self.seek_relative(-1.0))
        self.bind_all('<Right>', lambda e: self.seek_relative(1.0))
        self.bind_all('<Shift-Left>', lambda e: self.seek_relative(-5.0))
        self.bind_all('<Shift-Right>', lambda e: self.seek_relative(5.0))
        
        # Add space bar for play/pause toggle
        self.bind_all('<space>', lambda e: self.toggle_play_pause())
        
        # Text screen tab
        text_frame = ttk.Frame(notebook)
        notebook.add(text_frame, text='Text Screen')
        # Text widget with vertical scrollbar
        text_container = ttk.Frame(text_frame)
        text_container.pack(fill='both', expand=True)
        self.text = tk.Text(text_container)
        v_scroll_text = ttk.Scrollbar(text_container, orient='vertical', command=self.text.yview)
        self.text.configure(yscrollcommand=v_scroll_text.set)
        self.text.pack(side='left', fill='both', expand=True)
        v_scroll_text.pack(side='right', fill='y')
        # Bind to XML text modifications for live visualization update
        self.text.bind('<<Modified>>', self.on_text_modified)
        # Initialize modified flag state
        self.text.edit_modified(False)

    def bind_hover_events(self, widget):
        """Bind mouse enter/leave events to widget and all its children."""
        widget.bind('<Enter>', self.on_channel_enter)
        widget.bind('<Leave>', self.on_channel_leave)
        
        # Also bind to all children
        try:
            for child in widget.winfo_children():
                self.bind_hover_events(child)
        except:
            pass  # Some widgets might not have children

    def on_channel_enter(self, event=None):
        """Expand channel frame when mouse enters."""
        # Calculate expanded height based on actual content
        self.channel_scrollable_frame.update_idletasks()
        content_height = self.channel_scrollable_frame.winfo_reqheight()
        # Limit to reasonable maximum
        expanded_height = min(content_height + 20, 300)
        self.channel_canvas.configure(height=expanded_height)

    def on_channel_leave(self, event=None):
        """Collapse channel frame when mouse leaves."""
        # Check if mouse is really leaving the channel area
        if event:
            x, y = event.x_root, event.y_root
            # Get the channel frame bounds
            frame_x = self.channel_frame.winfo_rootx()
            frame_y = self.channel_frame.winfo_rooty()
            frame_width = self.channel_frame.winfo_width()
            frame_height = self.channel_frame.winfo_height()
            
            # Only collapse if mouse is actually outside the frame
            if not (frame_x <= x <= frame_x + frame_width and 
                   frame_y <= y <= frame_y + frame_height):                self.channel_canvas.configure(height=self.collapsed_height)
        else:
            self.channel_canvas.configure(height=self.collapsed_height)

    def process_midi(self, file_path):
        # Display path and XML, then visualize notes
        self.text.delete('1.0', 'end')
        self.text.insert('end', f'Loaded MIDI file: {file_path}\n')
        # Load MIDI data
        self.current_midi_file = file_path
        self.midi_data = MidiFile(file_path)
        # Capture initial tempo from first set_tempo meta message if present
        for track in self.midi_data.tracks:
            for msg in track:
                if msg.is_meta and msg.type == 'set_tempo':
                    self.tempo_us = msg.tempo
                    break
            else:
                continue
            break
        mf = self.midi_data
        # Determine instruments per channel from program_change messages
        self.channel_instruments.clear()
        for track in mf.tracks:
            for msg in track:
                if msg.type == 'program_change':
                    self.channel_instruments[msg.channel] = msg.program
        # Assign colors to channels used
        channels = sorted({msg.channel for track in mf.tracks for msg in track if hasattr(msg, 'channel')})
        for idx, ch in enumerate(channels):
            self.channel_colors[ch] = DEFAULT_CHANNEL_COLORS[idx % len(DEFAULT_CHANNEL_COLORS)]
        # Track visibility: show all channels by default
        self.visible_channels = set(channels)
        self.update_channel_legend()
        
        # FIXED: Process all tracks with global tempo handling
        self.notes_for_visualization = []
        
        # First pass: collect all tempo changes with global timing
        tempo_changes = []
        global_time = 0.0
        current_tempo = 500000  # Default tempo
        
        # Process all tracks to find tempo changes
        for track in mf.tracks:
            track_time = 0.0
            for msg in track:
                delta = mido.tick2second(msg.time, mf.ticks_per_beat, current_tempo)
                track_time += delta
                global_time = max(global_time, track_time)
                
                if msg.is_meta and msg.type == 'set_tempo':
                    tempo_changes.append({
                        'time': track_time,
                        'tempo': msg.tempo
                    })
                    current_tempo = msg.tempo  # Update current tempo
        
        # Sort tempo changes by time
        tempo_changes.sort(key=lambda x: x['time'])
        
        # Function to get tempo at specific time
        def get_tempo_at_time(time):
            tempo = 500000  # Default
            for change in tempo_changes:
                if change['time'] <= time:
                    tempo = change['tempo']
                else:
                    break
            return tempo
        
        # Second pass: process notes with correct tempo handling
        for i, track in enumerate(mf.tracks):
            print(f"Processing track {i}: {len(track)} messages")
            abs_time = 0.0
            active_on = {}
            
            for msg in track:
                # Get current tempo for this time point
                current_tempo = get_tempo_at_time(abs_time)
                
                # Calculate delta time with correct tempo
                delta = mido.tick2second(msg.time, mf.ticks_per_beat, current_tempo)
                abs_time += delta
                
                # Handle note events
                if msg.type == 'note_on' and getattr(msg, 'velocity', 0) > 0:
                    active_on[(msg.channel, msg.note)] = abs_time
                elif msg.type == 'note_off' or (msg.type == 'note_on' and getattr(msg, 'velocity', 0) == 0):
                    key = (getattr(msg, 'channel', None), getattr(msg, 'note', None))
                    if key in active_on:
                        start_time = active_on.pop(key)
                        duration = abs_time - start_time
                        self.notes_for_visualization.append({
                            'start_time': start_time, 
                            'note': key[1], 
                            'channel': key[0], 
                            'duration': duration
                        })
        
        # Build XML for display (using simplified approach)
        root = ET.Element('MidiFile', ticks_per_beat=str(mf.ticks_per_beat))
        for i, track in enumerate(mf.tracks):
            tr_elem = ET.SubElement(root, 'Track', name=track.name or f'Track_{i}')
            for msg in track:
                attrs = msg.dict()
                msg_elem = ET.SubElement(tr_elem, 'Message', type=msg.type, time=str(msg.time))
                for attr, value in attrs.items():
                    if attr not in ('type', 'time'):
                        msg_elem.set(attr, str(value))
        
        pretty_xml = minidom.parseString(ET.tostring(root, encoding='utf-8')).toprettyxml(indent="  ")
        self.text.insert('end', pretty_xml)
        
        # Save XML file to same directory as MIDI file
        try:
            base_name = os.path.splitext(file_path)[0]
            xml_file_path = f"{base_name}.xml"
            with open(xml_file_path, 'w', encoding='utf-8') as xml_file:
                xml_file.write(pretty_xml)
            print(f"XML saved to: {xml_file_path}")
        except Exception as e:
            print(f"Failed to save XML file: {e}")
        
        # Populate visualization notes from processed MIDI data
        self.notes = [(d['start_time'], d['note'], d['channel'], d['duration']) for d in self.notes_for_visualization]
        self.max_time = max((d['start_time'] + d['duration'] for d in self.notes_for_visualization), default=1)# Update the MIDI info labels with detailed information
        fname = os.path.basename(file_path)
        
        # Get MIDI format type (0, 1, or 2)
        midi_format = getattr(mf, 'type', 'Unknown')
        
        # Get ticks per beat
        ticks_per_beat = getattr(mf, 'ticks_per_beat', 'Unknown')
        
        # Calculate total duration in minutes:seconds
        duration_minutes = int(self.max_time // 60)
        duration_seconds = int(self.max_time % 60)
        duration_str = f"{duration_minutes}:{duration_seconds:02d}"
          # Get tempo information
        tempos_us = [msg.tempo for track in mf.tracks for msg in track if msg.is_meta and msg.type == 'set_tempo']
        if not tempos_us:
            tempos_us = [self.tempo_us]
        tempos_bpm = [int(round(60e6/t)) for t in tempos_us]
        
        # Remove duplicates while preserving order
        unique_tempos = []
        for tempo in tempos_bpm:
            if tempo not in unique_tempos:
                unique_tempos.append(tempo)
        
        # Create compact tempo display
        if len(unique_tempos) == 1:
            tempo_str = f"Tempo: {unique_tempos[0]} BPM"
        elif len(unique_tempos) == 2:
            tempo_str = f"Tempos: {unique_tempos[0]}-{unique_tempos[1]} BPM"
        elif len(unique_tempos) <= 4:
            tempo_str = f"Tempos: {', '.join(map(str, unique_tempos))} BPM"
        else:
            # For many tempos, show range
            min_tempo = min(unique_tempos)
            max_tempo = max(unique_tempos)
            if min_tempo == max_tempo:
                tempo_str = f"Tempo: {min_tempo} BPM"
            else:
                tempo_str = f"Tempos: {min_tempo}-{max_tempo} BPM ({len(unique_tempos)} changes)"
        
        # Count total notes
        total_notes = len(self.notes_for_visualization)
        
        # Update all info variables
        self.midi_filename_var.set(fname)
        self.midi_tracks_var.set(f"Tracks: {len(mf.tracks)} | Notes: {total_notes}")
        self.midi_format_var.set(f"Format: Type {midi_format}")
        self.midi_ticks_var.set(f"Ticks per Beat: {ticks_per_beat}")
        self.midi_tempo_var.set(tempo_str)
        self.midi_duration_var.set(f"Duration: {duration_str}")
        # Draw visualization and request scroll-to-bottom
        self.scroll_to_bottom_on_next_draw = True
        self.draw_visualization(self.notes, self.max_time)

    def load_midi_file(self):
        file_path = filedialog.askopenfilename(
            title='Select MIDI File',
            filetypes=[('MIDI files', '*.mid *.midi')]
        )
        if file_path:
            self.config_data['last_midi'] = file_path
            save_config(self.config_data)
            self.process_midi(file_path)

    def save_midi_file(self):
        if not hasattr(self, 'midi_data') or self.midi_data is None:
            messagebox.showwarning("No MIDI Data", "Please load a MIDI file first.")
            return
        
        # Get save location with default modified name
        default_name = ""
        if hasattr(self, 'current_midi_file') and self.current_midi_file:
            base_name = os.path.splitext(os.path.basename(self.current_midi_file))[0]
            default_name = f"{base_name}-modified.mid"
        
        file_path = filedialog.asksaveasfilename(
            title='Save MIDI File',
            initialfile=default_name,
            defaultextension='.mid',
            filetypes=[('MIDI files', '*.mid *.midi'), ('All files', '*.*')]
        )
        if not file_path:
            return
            
        try:
            # Parse current XML from text widget to rebuild MIDI
            content = self.text.get('1.0', 'end')
            xml_start = content.find('<MidiFile')
            if xml_start == -1:
                messagebox.showerror("Error", "No valid XML found in text editor.")
                return
                
            xml_content = content[xml_start:]
            root = ET.fromstring(xml_content)
            
            # Debug: check what we're actually parsing
            print(f"XML content preview: {xml_content[:500]}...")
            print(f"Found {len(root.findall('Track'))} tracks in XML")
            print(f"Original MIDI had {len(self.midi_data.tracks)} tracks")
            
            # Debug: Compare original vs XML message counts
            orig_msg_counts = [len(track) for track in self.midi_data.tracks]
            xml_msg_counts = [len(track.findall('Message')) for track in root.findall('Track')]
            print(f"Original message counts per track: {orig_msg_counts}")
            print(f"XML message counts per track: {xml_msg_counts}")
            
            # Debug: Check ticks_per_beat
            orig_tpb = self.midi_data.ticks_per_beat
            xml_tpb = int(root.get('ticks_per_beat', 480))
            print(f"Ticks per beat: Original={orig_tpb}, XML={xml_tpb}")
            if orig_tpb != xml_tpb:
                print("⚠️  WARNING: Ticks per beat mismatch!")
            
            # Create new MIDI file from XML
            ticks_per_beat = int(root.get('ticks_per_beat', 480))
            new_midi = MidiFile(ticks_per_beat=ticks_per_beat)
            
            for track_elem in root.findall('Track'):
                track = MidiTrack()
                track_name = track_elem.get('name', '')
                track.name = track_name
                
                # Debug: track processing
                messages_found = track_elem.findall('Message')
                print(f"Processing track '{track_name}': found {len(messages_found)} messages")
                
                # Count different message types for debugging
                msg_types = {}
                for msg_elem in messages_found:
                    msg_type = msg_elem.get('type')
                    msg_types[msg_type] = msg_types.get(msg_type, 0) + 1
                print(f"  Message types: {dict(sorted(msg_types.items()))}")
                  # Sort messages by time for proper MIDI ordering                # Process messages in their original XML order (don't sort!)
                # The XML already preserves the correct MIDI message order with proper delta times
                for msg_elem in track_elem.findall('Message'):
                    msg_type = msg_elem.get('type')
                    delta_time = int(msg_elem.get('time', 0))  # This is the correct delta time from original MIDI
                    
                    try:
                        # Build kwargs for message creation, excluding XML-specific attributes
                        kwargs = {}
                        for key, value in msg_elem.attrib.items():
                            if key not in ('type', 'time', 'abs_time', 'duration'):
                                # Convert string values back to appropriate types
                                try:
                                    # Try to convert to int first (most MIDI attributes are integers)
                                    if isinstance(value, str) and value.lstrip('-').isdigit():
                                        kwargs[key] = int(value)
                                    elif key == 'data' and isinstance(value, str):
                                        # Handle sysex data conversion
                                        if value.startswith('[') and value.endswith(']'):
                                            kwargs[key] = eval(value)
                                        else:
                                            kwargs[key] = []
                                    else:
                                        # Keep as string (for text, name, key attributes)
                                        kwargs[key] = value
                                except:
                                    # If conversion fails, keep original value
                                    kwargs[key] = value
                        
                        # Create message based on type - use generic approach to preserve all attributes
                        try:
                            # Determine if this is a meta message or regular message
                            is_meta_message = msg_type in [
                                'set_tempo', 'time_signature', 'key_signature', 'track_name', 'text', 
                                'copyright', 'marker', 'cue_marker', 'lyrics', 'midi_port', 'end_of_track',
                                'sequence_number', 'channel_prefix', 'device_name', 'instrument_name', 
                                'program_name', 'smpte_offset', 'sequencer_specific'
                            ]
                            
                            if is_meta_message:
                                # Create MetaMessage with all available kwargs
                                msg = mido.MetaMessage(msg_type, time=delta_time, **kwargs)
                            else:
                                # Create regular Message with all available kwargs
                                msg = mido.Message(msg_type, time=delta_time, **kwargs)
                                
                        except Exception as e:
                            print(f"Failed to create message {msg_type} with kwargs {kwargs}: {e}")
                            print(f"Message element attributes: {dict(msg_elem.attrib)}")
                            # Try to provide more specific error information
                            import traceback
                            traceback.print_exc()
                            continue
                            
                        # Successfully created message
                        track.append(msg)
                        if msg_type not in ['note_on', 'note_off']:  # Don't spam with note messages
                            print(f"Successfully created {msg_type} message: {msg}")
                        
                    except Exception as e:
                        print(f"Error processing message element {msg_elem.attrib}: {e}")
                        continue
                
                # Add the completed track to the MIDI file
                new_midi.tracks.append(track)
                print(f"Added track '{track.name}' with {len(track)} messages to MIDI file")
            
            # Debug: Show how many tracks we created
            print(f"Created MIDI file with {len(new_midi.tracks)} tracks")
            
            # Debug: Final summary of what we're saving
            print("\n=== FINAL SAVE SUMMARY ===")
            for i, track in enumerate(new_midi.tracks):
                print(f"Track {i} ('{track.name}'): {len(track)} messages")
                # Count message types
                msg_types = {}
                for msg in track:
                    msg_types[msg.type] = msg_types.get(msg.type, 0) + 1
                print(f"  Message types: {dict(sorted(msg_types.items()))}")
                
                # Show first few messages
                print(f"  First 3 messages:")
                for j, msg in enumerate(track[:3]):
                    print(f"    {j}: {msg}")
              # Compare with original
            print(f"\nComparison with original:")
            print(f"  Original: {len(self.midi_data.tracks)} tracks")
            print(f"  Reconstructed: {len(new_midi.tracks)} tracks")
            
            for i, (orig_track, new_track) in enumerate(zip(self.midi_data.tracks, new_midi.tracks)):
                print(f"  Track {i}: {len(orig_track)} → {len(new_track)} messages")
            print("==========================")
            
            # Save the MIDI file
            new_midi.save(file_path)
            messagebox.showinfo("Success", f"MIDI file saved to: {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save MIDI file: {str(e)}")
            traceback.print_exc()

    def create_gaps(self):
        """Create gaps using absolute time reconstruction method that properly handles MIDI delta times."""
        if not hasattr(self, 'midi_data') or self.midi_data is None:
            messagebox.showwarning("No MIDI Data", "Please load a MIDI file first.")
            return
        try:
            gap_ms = float(self.gap_var.get())
            if gap_ms <= 0:
                messagebox.showerror("Error", "Gap value must be positive.")
                return
            if gap_ms > 1000:
                messagebox.showwarning("Warning", "Gap value is very large (>1000ms). This may cause significant changes to the music.")
            
            # Calculate gap in ticks
            gap_seconds = gap_ms / 1000.0
            ticks_per_second = self.midi_data.ticks_per_beat * (1e6 / self.tempo_us)
            gap_ticks = int(gap_seconds * ticks_per_second)
            print(f"[ROBUST GAP] Creating gaps of {gap_ms} ms ({gap_ticks} ticks)")

            content = self.text.get('1.0', 'end')
            xml_start = content.find('<MidiFile')
            if xml_start == -1:
                messagebox.showerror("Error", "No valid XML found in text editor.")
                return
            xml_content = content[xml_start:]
            root = ET.fromstring(xml_content)

            total_modifications = 0
            min_duration_ticks = max(10, gap_ticks // 4)  # Minimum note duration
            
            # Process each track
            for track_elem in root.findall('Track'):
                print(f"Processing track with {len(track_elem.findall('Message'))} messages")
                
                # Step 1: Parse all events into absolute time
                events = []
                abs_time = 0
                
                for msg_elem in track_elem.findall('Message'):
                    delta_time = int(msg_elem.get('time', 0))
                    abs_time += delta_time
                    
                    event = {
                        'element': msg_elem,
                        'original_abs_time': abs_time,
                        'new_abs_time': abs_time,  # Will be modified if needed
                        'original_delta': delta_time,
                        'type': msg_elem.get('type'),
                        'channel': int(msg_elem.get('channel', 0)) if msg_elem.get('channel') is not None else None,
                        'note': int(msg_elem.get('note', 0)) if msg_elem.get('note') is not None else None,
                        'velocity': int(msg_elem.get('velocity', 0)) if msg_elem.get('velocity') is not None else None
                    }
                    events.append(event)
                
                # Step 2: Find note pairs (note_on -> note_off for same channel/pitch)
                active_notes = {}  # (channel, note) -> start_event
                note_pairs = []
                
                for event in events:
                    if event['type'] == 'note_on' and event['velocity'] and event['velocity'] > 0:
                        key = (event['channel'], event['note'])
                        active_notes[key] = event
                    elif (event['type'] == 'note_off' or 
                          (event['type'] == 'note_on' and (not event['velocity'] or event['velocity'] == 0))):
                        key = (event['channel'], event['note'])
                        if key in active_notes:
                            start_event = active_notes[key]
                            note_pairs.append((start_event, event))
                            del active_notes[key]
                
                # Step 3: Group note pairs by pitch and apply gap logic
                notes_by_pitch = {}
                for start_event, end_event in note_pairs:
                    key = (start_event['channel'], start_event['note'])
                    notes_by_pitch.setdefault(key, []).append((start_event, end_event))
                
                track_modifications = 0
                
                for key, notes in notes_by_pitch.items():
                    if len(notes) < 2:
                        continue
                    
                    # Sort by original start time
                    notes.sort(key=lambda x: x[0]['original_abs_time'])
                    
                    channel, pitch = key
                    
                    for i in range(1, len(notes)):
                        prev_start_event, prev_end_event = notes[i-1]
                        curr_start_event, curr_end_event = notes[i]
                        
                        # Calculate gap using current absolute times (which may have been modified)
                        prev_end_time = prev_end_event['new_abs_time']
                        curr_start_time = curr_start_event['new_abs_time']
                        gap = curr_start_time - prev_end_time
                        
                        if gap < gap_ticks:
                            # Calculate new end time for previous note
                            new_prev_end_time = curr_start_time - gap_ticks
                            
                            # Check if new note duration would be acceptable
                            prev_start_time = prev_start_event['new_abs_time']
                            new_duration = new_prev_end_time - prev_start_time
                            
                            if new_duration >= min_duration_ticks:
                                # Apply the modification
                                prev_end_event['new_abs_time'] = new_prev_end_time
                                track_modifications += 1
                                
                                if track_modifications <= 5:  # Debug first few
                                    print(f"  Modified Ch{channel} Note{pitch}: gap {gap} -> {gap_ticks} ticks (shortened by {prev_end_time - new_prev_end_time})")
                            else:
                                if track_modifications <= 5:
                                    print(f"  Skipped Ch{channel} Note{pitch}: would make note too short ({new_duration} < {min_duration_ticks})")
                
                print(f"Track modifications: {track_modifications}")
                total_modifications += track_modifications
                
                # Step 4: Rebuild the entire track with new delta times
                if track_modifications > 0:
                    # Sort all events by their new absolute times
                    events.sort(key=lambda x: x['new_abs_time'])
                    
                    # Clear the track and rebuild it
                    for msg_elem in list(track_elem):
                        track_elem.remove(msg_elem)
                    
                    # Recalculate delta times and add events back
                    prev_time = 0
                    for event in events:
                        new_delta = event['new_abs_time'] - prev_time
                        event['element'].set('time', str(new_delta))
                        track_elem.append(event['element'])
                        prev_time = event['new_abs_time']
                    
                    print(f"Rebuilt track with {len(events)} events")
            
            if total_modifications > 0:
                # Convert modified XML back to string and update the text editor
                xml_str = ET.tostring(root, encoding='unicode')
                dom = minidom.parseString(xml_str)
                pretty_xml = dom.toprettyxml(indent='  ')
                lines = [line for line in pretty_xml.split('\n') if line.strip()]
                formatted_xml = '\n'.join(lines[1:])
                new_content = content[:xml_start] + formatted_xml
                self.text.delete('1.0', 'end')
                self.text.insert('1.0', new_content)
                self.modifications_applied = True
                self.text.event_generate('<<Modified>>')
                
                print(f"[ROBUST GAP] Successfully applied {total_modifications} gap modifications")
            
            summary_msg = f"[ROBUST GAP] Created {gap_ms} ms gaps by modifying {total_modifications} note durations."
            messagebox.showinfo("Success", summary_msg)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create gaps: {str(e)}")
            traceback.print_exc()

    def draw_visualization(self, notes, max_time):
        self.canvas.delete('all')
        self.canvas.update_idletasks()
        # Get Y-scale multiplier
        scale = self.y_scale_var.get()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()        # compute total drawing height (scrollable) based on scale
        total_height = height * scale
        # clear and configure scrollregion early so coordinates map correctly
        self.canvas.configure(scrollregion=(0, 0, width, total_height))
        # Dimensions for keys: white and black key widths
        white_key_w = width / 88
        black_key_w = white_key_w * 0.75
        radius = 2  # corner radius        # Draw time lines every 2 seconds
        line_interval = 2.0  # 2 seconds
        num_lines = int(max_time // line_interval) + 1
        for i in range(1, num_lines + 1):
            t = i * line_interval
            # map time to Y in total_height space (0 at top)
            y = total_height - (t / max_time) * total_height
            self.canvas.create_line(0, y, width, y, fill='#444')
            # Label time just above the line
            minutes = int(t // 60)
            seconds = t % 60
            time_str = f"{minutes:02d}:{seconds:05.3f}"
            self.canvas.create_text(6, y - 14, text=time_str, anchor='nw', fill='white', font=self.vis_font)
        # Draw octave lines before each C key
        for note in range(21, 109):
            if note % 12 == 0:
                idx = note - 21
                x = idx * white_key_w
                # draw vertical lines spanning full scrollable region
                self.canvas.create_line(x, 0, x, total_height, fill='#444')
                # Label C and octave number to right of the line in blue with larger font
                octave = (note // 12) - 1
                self.canvas.create_text(x + 2, 2, text=f"C{octave}", anchor='nw', fill='blue', font=self.vis_font)
        # Draw each note scaled by duration with tooltip events
        # Prepare for tooltips
        self.rect_data = {}
        prev_end = {}
        # Sort notes by start time for gap calculation
        for idx, (time, note, channel, dur) in enumerate(sorted(notes, key=lambda x: x[0])):
            # Skip drawing notes for channels that are not visible
            if channel not in self.visible_channels:
                continue
            # Calculate key index (0 to 87)
            key_idx = note - 21
            # Determine if the key is black
            semitone = note % 12
            is_black = semitone in {1, 3, 6, 8, 10}
            note_w = black_key_w if is_black else white_key_w
            x1 = key_idx * white_key_w
            x2 = x1 + note_w
            # Y positions based on start time and duration
            # map note times to Y positions
            y1 = total_height - (time          / max_time) * total_height
            y2 = total_height - ((time + dur)  / max_time) * total_height
            y_top, y_bot = min(y1, y2), max(y1, y2)
            # Draw note rectangle with tag for events
            # Define tag and color for this note
            tag = f"note_{idx}"
            color = self.channel_colors.get(channel, '#cccccc')
            # Emulate rounded corners: draw two overlapping rectangles with corner radius
            self.canvas.create_rectangle(x1+radius, y_top, x2-radius, y_bot, fill=color, outline='', tags=(tag,))
            self.canvas.create_rectangle(x1, y_top+radius, x2, y_bot-radius, fill=color, outline='', tags=(tag,))
            # Calculate gap from previous same note
            prev = prev_end.get(note)
            gap = time - prev if prev is not None else None
            prev_end[note] = time + dur
            # Store data for tooltip
            self.rect_data[tag] = {'note': note, 'start': time, 'dur': dur, 'gap': gap}            # Bind hover events
            self.canvas.tag_bind(tag, '<Enter>', lambda e, t=tag: self.on_note_enter(e, t))
            self.canvas.tag_bind(tag, '<Leave>', lambda e: self.on_note_leave(e))        
        
        # Draw the keyboard underneath the visualization
        self.draw_keyboard()
        
        # Update scroll region to encompass all notes
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))        # Auto-scroll if flagged (e.g., after autoload), then clear flag
        if getattr(self, 'scroll_to_bottom_on_next_draw', False):
            self.canvas.yview_moveto(1.0)
            self.scroll_to_bottom_on_next_draw = False

    def draw_keyboard(self):
        """Draw an 88-key piano keyboard in Synthesia style underneath the visualization."""
        if not hasattr(self, 'keyboard_canvas'):
            return
            
        self.keyboard_canvas.delete('all')
        self.keyboard_canvas.update_idletasks()
        
        # Clear previous key references
        self.keyboard_keys = {}
        
        width = self.keyboard_canvas.winfo_width()
        height = self.keyboard_canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
            
        # Draw 2 pixel high blue horizontal line at the top
        self.keyboard_canvas.create_rectangle(0, 0, width, 2, fill='blue', outline='blue')
        
        # 88 keys total (A0 to C8), starting from MIDI note 21
        # White key pattern: C, D, E, F, G, A, B (7 white keys per octave)
        # Black key pattern: C#, D#, F#, G#, A# (5 black keys per octave)
        
        white_key_width = width / 52  # 52 white keys in 88-key piano
        white_key_height = height - 15  # Leave space for blue line at top and margin at bottom
        black_key_width = white_key_width * 0.6
        black_key_height = white_key_height * 0.6
        
        # Draw white keys first
        white_key_x = 0
        for note in range(21, 109):  # MIDI notes 21-108 (88 keys)
            semitone = note % 12
            # White keys: C(0), D(2), E(4), F(5), G(7), A(9), B(11)
            if semitone in [0, 2, 4, 5, 7, 9, 11]:
                # Create white key
                x1 = white_key_x
                y1 = 8  # Start below the blue line
                x2 = white_key_x + white_key_width - 1
                y2 = y1 + white_key_height
                
                # White key background
                key_id = self.keyboard_canvas.create_rectangle(
                    x1, y1, x2, y2, 
                    fill='white', outline='#666', width=1,
                    tags=f'key_{note}'
                )
                
                # Store key reference for highlighting
                self.keyboard_keys[note] = key_id
                
                # Label C keys with octave number
                if semitone == 0:
                    octave = (note // 12) - 1
                    self.keyboard_canvas.create_text(
                        x1 + white_key_width/2, y2 - 15,
                        text=f'C{octave}', fill='#666', 
                        font=('Arial', 8), anchor='center'
                    )
                
                white_key_x += white_key_width
        
        # Draw black keys on top
        white_key_x = 0
        for note in range(21, 109):  # MIDI notes 21-108
            semitone = note % 12
            
            # Position black keys between appropriate white keys
            if semitone in [0, 2, 4, 5, 7, 9, 11]:  # White key
                if semitone in [0, 2, 5, 7, 9]:  # White keys that have black keys to their right
                    next_note = note + 1
                    if next_note < 109:  # Make sure we don't go beyond the keyboard
                        next_semitone = next_note % 12
                        if next_semitone in [1, 3, 6, 8, 10]:  # Next note is black
                            # Draw black key
                            black_x = white_key_x + white_key_width - (black_key_width / 2)
                            black_y = 8  # Start below the blue line
                            
                            black_key_id = self.keyboard_canvas.create_rectangle(
                                black_x, black_y, 
                                black_x + black_key_width, black_y + black_key_height,
                                fill='#1a1a1a', outline='#333', width=1,
                                tags=f'key_{next_note}'
                            )
                              # Store black key reference for highlighting
                            self.keyboard_keys[next_note] = black_key_id
                
                white_key_x += white_key_width

    def update_keyboard_highlighting(self):
        """Update keyboard key highlighting based on notes visible in current viewport"""
        if not hasattr(self, 'keyboard_canvas') or not hasattr(self, 'keyboard_keys'):
            return
            
        # Reset all keys to their default colors first
        for note, key_id in self.keyboard_keys.items():
            semitone = note % 12
            if semitone in [1, 3, 6, 8, 10]:  # Black keys
                self.keyboard_canvas.itemconfig(key_id, fill='#1a1a1a')
            else:  # White keys
                self.keyboard_canvas.itemconfig(key_id, fill='white')        # IMPROVED: Use visual rectangle positions for accurate highlighting
        # This eliminates all coordinate mapping errors and timing drift issues
        currently_playing_notes = set()
        
        if hasattr(self, 'canvas') and hasattr(self, 'rect_data'):
            try:
                # FIXED: Use direct canvas coordinate methods to eliminate drift
                # Get the actual visible area using canvas methods that don't drift
                canvas_height = self.canvas.winfo_height()
                
                # Get the top-left corner of the visible area in canvas coordinates
                visible_top_y = self.canvas.canvasy(0)  # Top of visible area
                visible_bottom_y = self.canvas.canvasy(canvas_height)  # Bottom of visible area
                
                # The blue line is at the bottom edge of the visible viewport
                # This is where notes should be highlighted (when they touch the keyboard)
                blue_line_y = visible_bottom_y                
                # Use a small tolerance around the blue line for intersection
                highlight_tolerance = 5.0  # Very tight tolerance for precise highlighting
                
                # OPTIMIZED: Use spatial query to only check notes near the blue line
                # This dramatically improves performance for large MIDI files
                search_top = blue_line_y - highlight_tolerance - 50  # Extra margin for safety
                search_bottom = blue_line_y + highlight_tolerance + 50
                
                # Get canvas width for the search area
                try:
                    canvas_width = float(self.canvas.cget('scrollregion').split()[2])
                except:
                    canvas_width = self.canvas.winfo_width()
                
                # Find only rectangles that overlap with the blue line area
                # This is much faster than checking every single note
                overlapping_items = self.canvas.find_overlapping(0, search_top, canvas_width, search_bottom)
                
                # Check only the notes found in the spatial query
                for item in overlapping_items:
                    try:
                        # Get the tags for this canvas item
                        tags = self.canvas.gettags(item)
                        
                        # Find the note data tag (skip system tags like 'current')
                        note_tag = None
                        for tag in tags:
                            if tag in self.rect_data:
                                note_tag = tag
                                break
                        
                        if note_tag:
                            note_data = self.rect_data[note_tag]
                            
                            # Skip notes from deleted channels
                            if note_data.get('channel') in getattr(self, 'deleted_channels', set()):
                                continue
                            
                            # Get precise coordinates for intersection test
                            coords = self.canvas.coords(item)
                            if len(coords) >= 4:
                                rect_top_y = coords[1]  # y1
                                rect_bottom_y = coords[3]  # y2
                                
                                # Check if note rectangle intersects with the blue line
                                if (rect_top_y <= blue_line_y + highlight_tolerance and 
                                    rect_bottom_y >= blue_line_y - highlight_tolerance):
                                    currently_playing_notes.add((note_data['note'], note_data.get('channel', 0)))
                    except:
                        # If coordinate lookup fails, skip this note
                        continue
                            
            except:
                # Fallback: if visual approach fails, use audio position
                audio_position = self.get_actual_audio_position()
                if audio_position >= 0:
                    for note_data in getattr(self, 'notes_for_visualization', []):
                        if note_data.get('channel') in getattr(self, 'deleted_channels', set()):
                            continue
                        note_start = note_data.get('start_time', 0)
                        note_end = note_start + note_data.get('duration', 0)
                        if note_start <= audio_position <= note_end:
                            currently_playing_notes.add((note_data['note'], note_data.get('channel', 0)))
          
        # Update MIDI playback based on highlighted notes
        if self.is_playing and hasattr(self, 'note_player') and self.note_player.midi_out:
            self._update_midi_notes_from_highlighting(currently_playing_notes)
        
        # Highlight currently playing notes (extract just the note numbers for display)
        display_notes = {note for note, channel in currently_playing_notes}
        for note in display_notes:
            if note in self.keyboard_keys:
                key_id = self.keyboard_keys[note]
                semitone = note % 12
                
                if semitone in [1, 3, 6, 8, 10]:  # Black keys
                    # Highlight black keys with bright blue
                    self.keyboard_canvas.itemconfig(key_id, fill='#4080FF')
                else:  # White keys
                    # Highlight white keys with light blue
                    self.keyboard_canvas.itemconfig(key_id, fill='#B0D0FF')

    def _update_midi_notes_from_highlighting(self, currently_playing_notes):
        """Update MIDI note playback based on currently highlighted notes"""
        if not hasattr(self, 'active_midi_notes'):
            self.active_midi_notes = set()
        
        # Get sets of (note, channel) tuples for comparison
        new_notes = currently_playing_notes
        active_notes = self.active_midi_notes
          # Notes to turn OFF (were playing but no longer highlighted)
        notes_to_stop = active_notes - new_notes
        for note, channel in notes_to_stop:
            if channel not in getattr(self, 'visible_channels', set()):
                continue  # Skip invisible channels
            try:
                if hasattr(self, 'note_player') and self.note_player and self.note_player.midi_out:
                    self.note_player._note_off(channel, note)
            except:
                pass
        
        # Notes to turn ON (newly highlighted)
        notes_to_start = new_notes - active_notes
        for note, channel in notes_to_start:
            if channel not in getattr(self, 'visible_channels', set()):
                continue  # Skip invisible channels
            try:
                # Get velocity from note data if available
                velocity = 64  # Default velocity
                for note_data in getattr(self, 'notes_for_visualization', []):
                    if note_data.get('note') == note and note_data.get('channel') == channel:
                        velocity = note_data.get('velocity', 64)
                        break
                
                if hasattr(self, 'note_player') and self.note_player and self.note_player.midi_out:
                    self.note_player._note_on(channel, note, velocity)
            except:
                pass
        
        # Update the active notes set
        self.active_midi_notes = new_notes.copy()

    def get_actual_audio_position(self):
        """Calculate the actual audio playback position with perfect timing synchronization"""
        if not self.is_playing or self.playback_start_time is None:
            # If not playing, use the visual position for manual seeking
            return self.playback_position
          # Calculate elapsed time since audio started
        elapsed_time = time.time() - self.playback_start_time
        
        # The playback_start_time represents the current playback position
        return elapsed_time

    def on_text_modified(self, event):
        # Reset modified flag
        text_widget = event.widget
        if text_widget.edit_modified():
            text_widget.edit_modified(False)
            # Parse XML from text widget
            content = text_widget.get('1.0', 'end')
            # Extract XML portion starting at root tag
            idx = content.find('<MidiFile')
            if idx != -1:
                xml_str = content[idx:]
                try:
                    root = ET.fromstring(xml_str)
                    # Always rebuild visualization from the current XML
                    # This ensures gaps and other modifications are reflected
                    self.rebuild_notes_from_xml(root)
                except Exception as e:
                    print(f"Error parsing XML for visualization: {e}")
                    return

    def on_closing(self):
        # Stop any ongoing playback
        self.stop_midi()
        
        # Clean up MIDI note player
        if hasattr(self, 'note_player') and self.note_player:
            self.note_player.close()
        
        # Save window geometry and state
        self.config_data['geometry'] = self.geometry()
        self.config_data['window_state'] = self.state()  # Save window state (normal/zoomed)
        self.config_data['y_scale'] = self.y_scale_var.get()
        save_config(self.config_data)
        self.destroy()
    
    def update_channel_legend(self):
        # Clear existing legend
        for child in self.channel_content_frame.winfo_children():
            child.destroy()
        # Create legend items per channel with visibility checkbox
        for ch, color in sorted(self.channel_colors.items()):
            program = self.channel_instruments.get(ch, 0)
            instr = GM_INSTRUMENTS[program] if program < len(GM_INSTRUMENTS) else 'Unknown'
            item = tk.Frame(self.channel_content_frame)
            item.pack(side='top', anchor='w', pady=2)
            # Checkbox for visibility
            var = self.channel_vars.get(ch)
            if var is None:
                var = tk.BooleanVar(value=(ch in self.visible_channels))
                self.channel_vars[ch] = var
            cb = tk.Checkbutton(item, variable=var, command=lambda ch=ch: self.toggle_channel(ch))
            # 'S' button for selecting only this channel
            select_btn = tk.Button(item, text='S', width=2, height=1, 
                                 command=lambda ch=ch: self.select_only_channel(ch),
                                 font=('Arial', 8, 'bold'))
            # Color indicator and label will be alongside checkbox
            dot = tk.Canvas(item, width=12, height=12, bg=color, highlightthickness=0)
            lbl = ttk.Label(item, text=f'Ch {ch}: {instr}', foreground=color)
            # Pack widgets
            cb.pack(side='left')
            select_btn.pack(side='left', padx=(2, 2))
            dot.pack(side='left', padx=(4,4))
            lbl.pack(side='left')            # Define click handlers
            def on_left(e, ch=ch, var=var):
                var.set(not var.get())
                self.toggle_channel(ch)
            def on_right(e, ch=ch):
                self.show_channel_delete_menu(e, ch)
            
            # Bind left-click on row frame, dot, and label only (checkbox handles its own toggle)
            for widget in (item, dot, lbl):
                widget.bind('<Button-1>', on_left)
                widget.bind('<Button-3>', on_right)
            
            # Also bind right-click to checkbox and select button
            cb.bind('<Button-3>', on_right)
            select_btn.bind('<Button-3>', on_right)
            
            # Bind hover events to new items as well
            self.bind_hover_events(item)
            self.bind_hover_events(select_btn)

    def toggle_channel(self, ch):
        # Update visibility set based on checkbox and redraw
        if self.channel_vars[ch].get():
            self.visible_channels.add(ch)
        else:
            self.visible_channels.discard(ch)
        self.draw_visualization(self.notes, self.max_time)

    def select_only_channel(self, ch):
        # If this channel is already the only visible one, toggle to show all channels
        all_channels = set(self.channel_vars.keys())
        if self.visible_channels == {ch}:
            for c, var in self.channel_vars.items():
                var.set(True)
            self.visible_channels = set(all_channels)
        else:
            # Otherwise, select only this channel and uncheck others
            for c, var in self.channel_vars.items():
                if c == ch:

                    var.set(True)
                else:
                    var.set(False)
            self.visible_channels = {ch}
        # Redraw visualization with updated visibility
        self.draw_visualization(self.notes, self.max_time)

    # Tooltip window
    def show_tooltip(self, x, y, text):
        # create tooltip window at (x, y)
        self.hide_tooltip()
        self.tooltip_window = tk.Toplevel(self)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x+10}+{y+10}")
        label = tk.Label(self.tooltip_window, text=text, justify='left', background='lightyellow', relief='solid', borderwidth=1)
        label.pack()

    def hide_tooltip(self):
        if hasattr(self, 'tooltip_window') and self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def note_number_to_name(self, note):
        # Convert MIDI note number to name with octave
        name = self.NOTE_NAMES[note % 12]
        octave = note // 12 - 1
        return f"{name}{octave}"

    def on_note_enter(self, event, tag):
        data = self.rect_data.get(tag, {})
        note = data.get('note')
        start = data.get('start')
        dur = data.get('dur')
        gap = data.get('gap')
        # Format times
        mins, secs = divmod(start, 60)
        start_str = f"{int(mins):02d}:{secs:05.3f}"
        dur_str = f"{dur:0.3f}s"
        gap_str = f"{gap:0.3f}s" if gap is not None else "NA"
        note_name = self.note_number_to_name(note)
        text = f"Note: {note_name}\nStart: {start_str}\nDuration: {dur_str}\nGap: {gap_str}"
        # Show tooltip at mouse position
        self.show_tooltip(event.x_root, event.y_root, text)

    def on_note_leave(self, event):
        self.hide_tooltip()

    def get_current_tempo(self, t):
        """
        Return the tempo (in microseconds per quarter note) active at time t (seconds).
        """
        tempo = self.tempo_changes[0][1] if hasattr(self, 'tempo_changes') and self.tempo_changes else self.tempo_us
        for change_time, change_tempo in self.tempo_changes:
            if change_time <= t:
                tempo = change_tempo
            else:
                break
        return tempo

    def rebuild_notes_from_xml(self, root):
        """Rebuild note visualization data from XML by processing note on/off pairs"""
        notes = []
        active_notes = {}  # key: (channel, note) -> start_time
        
        # Get ticks per beat for time conversion
        ticks_per_beat = int(root.get('ticks_per_beat', 480))
        tempo_us = 500000  # Default tempo (120 BPM)
        
        # Calculate absolute time from delta times OR use abs_time if present
        for tr in root.findall('Track'):
            abs_time = 0.0
            
            for msg_elem in tr.findall('Message'):                # Check if abs_time is present (from our gapping modifications)
                if msg_elem.get('abs_time') is not None:
                    # Use the abs_time directly (convert from ticks to seconds)
                    try:
                        abs_time_str = msg_elem.get('abs_time')
                        # Handle both integer and float string representations
                        abs_time_ticks = int(float(abs_time_str))
                        abs_time = (abs_time_ticks / ticks_per_beat) * (tempo_us / 1e6)
                    except (ValueError, TypeError) as e:
                        print(f"Warning: Invalid abs_time value '{abs_time_str}', falling back to delta time calculation")
                        delta_time = int(msg_elem.get('time', 0))
                        abs_time += (delta_time / ticks_per_beat) * (tempo_us / 1e6)
                else:
                    # Calculate from delta time
                    delta_time = int(msg_elem.get('time', 0))
                    abs_time += (delta_time / ticks_per_beat) * (tempo_us / 1e6)
                
                msg_type = msg_elem.get('type')
                
                # Update tempo for time calculations
                if msg_type == 'set_tempo':
                    tempo_us = int(msg_elem.get('tempo', 500000))
                
                # Process note events
                elif msg_type == 'note_on':
                    note = int(msg_elem.get('note', 0))
                    channel = int(msg_elem.get('channel', 0))
                    velocity = int(msg_elem.get('velocity', 0))
                    
                    if velocity > 0:
                        # Note on
                        active_notes[(channel, note)] = abs_time
                    else:
                        # Note off (velocity 0)
                        key = (channel, note)
                        if key in active_notes:
                            start_time = active_notes.pop(key)
                            duration = abs_time - start_time
                            if duration > 0:
                                notes.append((start_time, note, channel, duration))
                
                elif msg_type == 'note_off':
                    note = int(msg_elem.get('note', 0))
                    channel = int(msg_elem.get('channel', 0))
                    key = (channel, note)
                    if key in active_notes:
                        start_time = active_notes.pop(key)
                        duration = abs_time - start_time
                        if duration > 0:
                            notes.append((start_time, note, channel, duration))
        
        # Update visualization data
        self.notes = notes
        self.max_time = max((t + d for t, _, _, d in notes), default=1)
        self.draw_visualization(self.notes, self.max_time)

    def compare_midi_and_xml(self):
        """Diagnostic function to compare original MIDI data with XML representation"""
        if not hasattr(self, 'midi_data') or self.midi_data is None:
            print("No MIDI data loaded")
            return
        
        print("=== MIDI vs XML Comparison ===")
        
        # Get XML from text widget
        content = self.text.get('1.0', 'end')
        xml_start = content.find('<MidiFile')
        if xml_start == -1:
            print("No XML found in text widget")
            return
        
        xml_content = content[xml_start:]
        try:
            xml_root = ET.fromstring(xml_content)
        except Exception as e:
            print(f"Failed to parse XML: {e}")
            return
        
        # Compare track count
        midi_track_count = len(self.midi_data.tracks)
        xml_track_count = len(xml_root.findall('Track'))
        print(f"Tracks: MIDI={midi_track_count}, XML={xml_track_count}")
        
        # Compare each track
        for i, (midi_track, xml_track) in enumerate(zip(self.midi_data.tracks, xml_root.findall('Track'))):
            print(f"\n--- Track {i} ---")
            midi_msg_count = len(midi_track)
            xml_msg_count = len(xml_track.findall('Message'))
            print(f"Messages: MIDI={midi_msg_count}, XML={xml_msg_count}")
            
            # Compare first few messages in detail
            xml_messages = xml_track.findall('Message')
            for j, (midi_msg, xml_msg) in enumerate(zip(midi_track[:5], xml_messages[:5])):
                print(f"  Message {j}:")
                print(f"    MIDI: {midi_msg}")
                print(f"    XML:  type={xml_msg.get('type')}, time={xml_msg.get('time')}")
                
                # Compare attributes
                midi_attrs = midi_msg.dict()
                xml_attrs = dict(xml_msg.attrib)
                
                midi_keys = set(midi_attrs.keys())
                xml_keys = set(xml_attrs.keys())
                
                if midi_keys != xml_keys:
                    print(f"    Attribute mismatch:")
                    print(f"      MIDI only: {midi_keys - xml_keys}")
                    print(f"      XML only: {xml_keys - midi_keys}")
                
                # Check attribute values
                for key in midi_keys & xml_keys:
                    midi_val = str(midi_attrs[key])
                    xml_val = xml_attrs[key]
                    if midi_val != xml_val:
                        print(f"    Value mismatch for '{key}': MIDI='{midi_val}', XML='{xml_val}'")

    def test_roundtrip_conversion(self):
        """Test converting XML back to MIDI and compare with original"""
        if not hasattr(self, 'midi_data') or self.midi_data is None:
            print("No MIDI data loaded")
            return
        
        print("=== Testing Round-trip Conversion ===")
        
        # Get XML from text widget
        content = self.text.get('1.0', 'end')
        xml_start = content.find('<MidiFile')
        if xml_start == -1:
            print("No XML found in text widget")
            return
        
        xml_content = content[xml_start:]
        try:
            root = ET.fromstring(xml_content)
        except Exception as e:
            print(f"Failed to parse XML: {e}")
            return
        
        # Convert XML back to MIDI (same logic as save function)
        ticks_per_beat = int(root.get('ticks_per_beat', 480))
        reconstructed_midi = MidiFile(ticks_per_beat=ticks_per_beat)
        
        print(f"Original ticks_per_beat: {self.midi_data.ticks_per_beat}")
        print(f"Reconstructed ticks_per_beat: {ticks_per_beat}")
        
        for track_elem in root.findall('Track'):
            track = MidiTrack()
            track_name = track_elem.get('name', '')
            track.name = track_name
            
            # Collect all messages
            messages = []
            for msg_elem in track_elem.findall('Message'):
                msg_type = msg_elem.get('type')
                time = int(msg_elem.get('time', 0))
                
                attrs = {'type': msg_type, 'time': time}
                for key, value in msg_elem.attrib.items():
                    if key not in ('type', 'time'):
                        # Convert numeric attributes
                        if key in ('channel', 'note', 'velocity', 'program', 'control', 'value', 'pitch', 
                                  'port', 'numerator', 'denominator', 'clocks_per_click', 
                                  'notated_32nd_notes_per_beat', 'tempo'):
                            try:
                                attrs[key] = int(value)
                            except (ValueError, TypeError):
                                attrs[key] = value
                        else:
                            attrs[key] = value
                
                messages.append(attrs)
            
            messages.sort(key=lambda x: x['time'])
            
            success_count = 0
            fail_count = 0
            
            for msg_attrs in messages:
                try:
                    msg_type = msg_attrs['type']
                    time = msg_attrs['time']
                    
                    # Create the message (using same logic as save function)
                    kwargs = {k: v for k, v in msg_attrs.items() if k not in ('type', 'time')}
                    
                    if msg_type in ['note_on', 'note_off']:
                        msg = mido.Message(msg_type, 
                                         channel=kwargs.get('channel', 0),
                                         note=kwargs.get('note', 60),
                                         velocity=kwargs.get('velocity', 64),
                                         time=time)
                    elif msg_type == 'set_tempo':
                        msg = mido.MetaMessage(msg_type, 
                                             tempo=kwargs.get('tempo', 500000),
                                             time=time)
                    elif msg_type == 'time_signature':
                        msg = mido.MetaMessage(msg_type,
                                             numerator=kwargs.get('numerator', 4),
                                             denominator=kwargs.get('denominator', 4),
                                             clocks_per_click=kwargs.get('clocks_per_click', 24),
                                             notated_32nd_notes_per_beat=kwargs.get('notated_32nd_notes_per_beat', 8),
                                             time=time)
                    elif msg_type == 'program_change':
                        msg = mido.Message(msg_type,
                                         channel=kwargs.get('channel', 0),
                                         program=kwargs.get('program', 0),
                                         time=time)
                    elif msg_type == 'control_change':
                        msg = mido.Message(msg_type,
                                         channel=kwargs.get('channel', 0),
                                         control=kwargs.get('control', 0),
                                         value=kwargs.get('value', 0),
                                         time=time)
                    elif msg_type == 'key_signature':
                        msg = mido.MetaMessage(msg_type,
                                             key=kwargs.get('key', 'C'),
                                             time=time)
                    elif msg_type == 'midi_port':
                        msg = mido.MetaMessage(msg_type,
                                             port=kwargs.get('port', 0),
                                             time=time)
                    elif msg_type == 'end_of_track':
                        msg = mido.MetaMessage(msg_type, time=time)
                    else:
                        print(f"Unsupported message type in test: {msg_type}")
                        fail_count += 1
                        continue
                    
                    track.append(msg)
                    success_count += 1
                    
                except Exception as e:
                    print(f"Failed to create message {msg_attrs}: {e}")
                    fail_count += 1
            
            reconstructed_midi.tracks.append(track)
            print(f"Track '{track.name}': {success_count} success, {fail_count} failed")
        
        # Compare original vs reconstructed
        print(f"\nComparison:")
        print(f"Original tracks: {len(self.midi_data.tracks)}")
        print(f"Reconstructed tracks: {len(reconstructed_midi.tracks)}")
        
        for i, (orig_track, recon_track) in enumerate(zip(self.midi_data.tracks, reconstructed_midi.tracks)):
            print(f"Track {i}: Original={len(orig_track)} messages, Reconstructed={len(recon_track)} messages")

    def test_timing_preservation(self):
        """Test that timing is preserved correctly in the round-trip conversion"""
        if not hasattr(self, 'midi_data') or self.midi_data is None:
            print("No MIDI data loaded")
            return
        
        print("=== Testing Timing Preservation ===")
        
        # Get original timing from first track
        orig_track = self.midi_data.tracks[0]
        orig_times = [msg.time for msg in orig_track]
        print(f"Original track has {len(orig_track)} messages")
        print(f"Original delta times: {orig_times[:10]}...")  # Show first 10
        
        # Calculate cumulative times for original
        orig_cumulative = []
        cum = 0
        for t in orig_times:
            cum += t
            orig_cumulative.append(cum)
        print(f"Original cumulative times: {orig_cumulative[:10]}...")
        
        # Get XML from text widget and convert back to MIDI
        content = self.text.get('1.0', 'end')
        xml_start = content.find('<MidiFile')
        if xml_start == -1:
            print("No XML found")
            return
        
        xml_content = content[xml_start:]
        try:
            root = ET.fromstring(xml_content)
        except Exception as e:
            print(f"Failed to parse XML: {e}")
            return
        
        # Reconstruct first track
        track_elem = root.findall('Track')[0]
        recon_times = []
        
        for msg_elem in track_elem.findall('Message'):
            delta_time = int(msg_elem.get('time', 0))
            recon_times.append(delta_time)
        
        print(f"Reconstructed track has {len(recon_times)} messages")
        print(f"Reconstructed delta times: {recon_times[:10]}...")
        
        # Calculate cumulative times for reconstructed
        recon_cumulative = []
        cum = 0
        for t in recon_times:
            cum += t
            recon_cumulative.append(cum)
        print(f"Reconstructed cumulative times: {recon_cumulative[:10]}...")
        
        # Compare
        if orig_times == recon_times:
            print("✅ Delta times preserved perfectly!")
        else:
            print("❌ Delta times differ!")
            mismatches = 0
            for i, (orig, recon) in enumerate(zip(orig_times, recon_times)):
                if orig != recon:
                    print(f"  Message {i}: {orig} → {recon}")
                    mismatches += 1
                    if mismatches >= 5:  # Limit output
                        print(f"  ... and {len(orig_times) - i - 1} more mismatches")
                        break
        
        if orig_cumulative == recon_cumulative:
            print("✅ Cumulative timing preserved perfectly!")
        else:
            print("❌ Cumulative timing differs!")
        
        print("=== End Timing Test ===")

    def show_channel_delete_menu(self, event, channel):
        """Show context menu for channel deletion"""
        import tkinter.messagebox as msgbox
        
        # Get channel info for confirmation
        program = self.channel_instruments.get(channel, 0)
        instr = GM_INSTRUMENTS[program] if program < len(GM_INSTRUMENTS) else 'Unknown'
        
        # Show confirmation dialog
        result = msgbox.askyesno(
            "Delete Channel", 
            f"Are you sure you want to delete Channel {channel} ({instr})?\n\n"
            f"This will permanently remove all notes from this channel."
        )
        
        if result:
            self.delete_channel(channel)
    
    def delete_channel(self, channel):
        """Delete a channel from the MIDI data, XML, and visualization"""
        try:
            # Remove from channel tracking
            if channel in self.channel_colors:
                del self.channel_colors[channel]
            if channel in self.channel_instruments:
                del self.channel_instruments[channel]
            if channel in self.channel_vars:
                del self.channel_vars[channel]
            if channel in self.visible_channels:
                self.visible_channels.discard(channel)
            
            # Remove from visualization data
            self.notes_for_visualization = [
                note for note in self.notes_for_visualization 
                if note['channel'] != channel
            ]
            
            # Update notes list for visualization
            self.notes = [(d['start_time'], d['note'], d['channel'], d['duration']) 
                         for d in self.notes_for_visualization]
            self.max_time = max((d['start_time'] + d['duration'] for d in self.notes_for_visualization), default=1)
            
            # Remove from XML in text widget
            self.remove_channel_from_xml(channel)
            
            # Update channel legend
            self.update_channel_legend()
            
            # Redraw visualization
            self.draw_visualization(self.notes, self.max_time)
            
            print(f"Channel {channel} deleted successfully")
            
        except Exception as e:
            import tkinter.messagebox as msgbox
            msgbox.showerror("Error", f"Failed to delete channel {channel}: {str(e)}")
    
    def remove_channel_from_xml(self, channel):
        """Remove all messages for a specific channel from the XML text"""
        try:
            content = self.text.get('1.0', 'end')
            xml_start = content.find('<MidiFile')
            
            if xml_start == -1:
                return
                
            xml_content = content[xml_start:]
            
            # Parse XML
            root = ET.fromstring(xml_content)
            
            # Remove messages with the specified channel
            for track in root.findall('Track'):
                messages_to_remove = []
                for msg in track.findall('Message'):
                    if msg.get('channel') == str(channel):
                        messages_to_remove.append(msg)
                
                # Remove the messages
                for msg in messages_to_remove:
                    track.remove(msg)
              # Convert back to pretty XML
            pretty_xml = minidom.parseString(ET.tostring(root, encoding='utf-8')).toprettyxml(indent="  ")            # Remove empty lines
            lines = pretty_xml.split('\n')
            non_empty_lines = [line for line in lines if line.strip()]
            clean_xml = '\n'.join(non_empty_lines)
            
            # Update text widget
            self.text.delete('1.0', 'end')
            self.text.insert('1.0', clean_xml)
        except Exception as e:
            print(f"Error removing channel {channel} from XML: {e}")

    def rewind_to_start(self):
        """Rewind playback to the beginning"""
        try:
            # Stop current playback if playing
            if self.is_playing:
                self.stop_midi()
              # Reset position to start
            self.playback_position = 0.0
            self.playback_start_time = None
            
            # Update displays
            self.update_led_clock()
            self.sync_scrollbar_to_midi_position()
            self.update_keyboard_highlighting()
            
            print("Rewound to start")
            
        except Exception as e:
            print(f"Error rewinding to start: {e}")

    def toggle_play_pause(self):
        """Toggle between play and pause using highlighting-driven playback"""
        print("=== toggle_play_pause() called ===")
        try:
            print(f"Current MIDI file: {getattr(self, 'current_midi_file', 'None')}")
            print(f"Has note_player: {hasattr(self, 'note_player')}")
            if hasattr(self, 'note_player'):
                print(f"note_player.midi_out: {getattr(self.note_player, 'midi_out', 'None')}")
            
            if not self.current_midi_file:
                print("❌ No MIDI file loaded")
                return
                
            if not hasattr(self, 'note_player') or not self.note_player.midi_out:
                print("❌ Note-based MIDI playback not available")
                print("⚠ Continuing anyway for testing (no audio will be heard)")
                # Temporarily bypass MIDI output requirement for testing
                # return
            
            # DEBUG: Print current playback position
            print(f"Current playback_position: {self.playback_position:.2f}s")
            
            if self.is_playing:
                # Currently playing, so pause
                self.pause_midi()
            elif self.is_paused:
                # Currently paused, so resume
                self.play_midi()
            else:
                # Not playing, so start
                print(f"Starting highlighting-driven playback from position: {self.playback_position:.2f}s")
                self.play_midi()
                
        except Exception as e:
            print(f"Error toggling play/pause: {e}")
            import traceback
            traceback.print_exc()

    def play_midi(self):
        """Start highlighting-driven MIDI playback"""
        print("=== play_midi() called ===")
        
        if not self.current_midi_file:
            print("❌ No MIDI file loaded")
            return
            
        print(f"✓ MIDI file loaded: {self.current_midi_file}")
        
        if not hasattr(self, 'note_player'):
            print("❌ note_player not found")
            return
            
        print(f"✓ note_player exists: {type(self.note_player)}")
        
        if not self.note_player.midi_out:
            print("⚠ Note-based MIDI playback not available - no MIDI output device")
            print("✓ Visualization playback will continue without audio")
        else:
            print(f"✓ MIDI output device available")
            
        print(f"✓ Notes loaded: {len(getattr(self, 'notes_for_visualization', []))}")
        print(f"✓ Current position: {self.playback_position:.2f}s")
        
        try:
            # Initialize active notes tracking
            if not hasattr(self, 'active_midi_notes'):
                self.active_midi_notes = set()
            
            # Set timing state for highlighting-driven playback
            self.playback_start_time = time.time() - self.playback_position
            self.is_playing = True
            self.is_paused = False
            
            print(f"✓ Highlighting-driven playback state updated: is_playing={self.is_playing}")
              # Update button states
            self.play_pause_button.config(text='⏸', bg='yellow')
            print("✓ Button updated to pause symbol")
            
            # Start the playback timer - this will drive everything through highlighting
            self.update_playback_timer()
            print("✓ Playback timer started")
            
            print(f"✓ Highlighting-driven MIDI playback started at position {self.playback_position:.2f}s")
            
        except Exception as e:
            print(f"❌ Error in play_midi(): {e}")
            import traceback
            traceback.print_exc()

    def start_midi_playback(self):
        """Start highlighting-driven MIDI playback"""
        self.play_midi()

    def pause_midi(self):
        """Pause highlighting-driven MIDI playback"""
        if self.is_playing:
            try:
                # Stop all currently playing MIDI notes
                if hasattr(self, 'active_midi_notes') and hasattr(self, 'note_player') and self.note_player.midi_out:
                    for note, channel in self.active_midi_notes:
                        try:
                            self.note_player._note_off(channel, note)
                        except:
                            pass
                    self.active_midi_notes.clear()
                
                self.is_playing = False
                self.is_paused = True
                
                if self.playback_timer:
                    self.after_cancel(self.playback_timer)
                    self.playback_timer = None
                
                # Update playback position to current position when paused
                # Update playback position to current position when paused
                if self.playback_start_time:
                    self.playback_position = time.time() - self.playback_start_time
                
                # Update button to show play symbol when paused
                self.play_pause_button.config(text='▶', bg='lightgreen')
                
                print(f"✓ Highlighting-driven MIDI playback paused at {self.playback_position:.2f}s")
            except Exception as e:
                print(f"Error pausing MIDI: {e}")

    def stop_midi(self):
        """Stop highlighting-driven MIDI playback and reset position"""
        try:
            # Stop all currently playing MIDI notes
            if hasattr(self, 'active_midi_notes') and hasattr(self, 'note_player') and self.note_player.midi_out:
                for note, channel in self.active_midi_notes:
                    try:
                        self.note_player._note_off(channel, note)
                    except:
                        pass
                self.active_midi_notes.clear()
                
            self.is_playing = False
            self.is_paused = False
            self.playback_position = 0.0
            self.playback_start_time = None
                
            if self.playback_timer:
                self.after_cancel(self.playback_timer)
                self.playback_timer = None
            
            # Reset button to play symbol when stopped
            self.play_pause_button.config(text='▶', bg='lightgreen')
            
            self.update_led_clock()
            self.sync_scrollbar_to_midi_position()
            self.update_keyboard_highlighting()  # Clear any highlighted keys
            print("✓ Highlighting-driven MIDI playback stopped")
        except Exception as e:
            print(f"Error stopping MIDI: {e}")
            self.playback_position = 0.0
            self.playback_start_time = None
                
            if self.playback_timer:
                self.after_cancel(self.playback_timer)
                self.playback_timer = None
              # Stop playback thread if running
            if self.playback_thread and self.playback_thread.is_alive():
                self.playback_stop_event.set()
                self.playback_thread.join(timeout=1.0)
            
            # Reset button to play symbol when stopped
            self.play_pause_button.config(text='▶', bg='lightgreen')
            
            self.update_led_clock()
            self.sync_scrollbar_to_midi_position()
            self.update_keyboard_highlighting()  # Clear any highlighted keys
            print("MIDI playback stopped")
        except Exception as e:
            print(f"Error stopping MIDI: {e}")

    def update_playback_timer(self):
        """Update playback position and schedule next update"""
        if self.is_playing and not self.is_paused:
            # Calculate accurate playback position using the unified timing approach
            if self.playback_start_time is not None:
                # Use the same logic as get_actual_audio_position()
                self.playback_position = self.get_actual_audio_position()
            
            # Check if we've reached the end
            if hasattr(self, 'max_time') and self.playback_position >= self.max_time:
                self.stop_midi()
                return
            
            # Update LED display
            self.update_led_clock()
            
            # Sync scrollbar position with playback position
            self.sync_scrollbar_to_midi_position()
              # Update keyboard highlighting
            self.update_keyboard_highlighting()
            
            # Schedule next update (faster update for smoother highlighting)
            self.playback_timer = self.after(50, self.update_playback_timer)

    def update_led_clock(self):
        """Update the LED-style position clock display"""
        self.led_clock.delete('all')
        
        # Convert position to minutes:seconds.milliseconds
        minutes = int(self.playback_position // 60)
        seconds = int(self.playback_position % 60)
        milliseconds = int((self.playback_position % 1) * 1000)
          # Format as MM:SS.mmm
        time_str = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
          # LED segment colors
        led_on_color = '#00FF00'  # Bright green for active segments
        led_off_color = '#003300'  # Dark green for inactive segments
          # Draw LED-style digits (scaled up for larger display and centered)
        char_width = 18  # Character width
        char_spacing = 3  # Spacing between characters
        
        # Calculate total width needed for the time string
        total_text_width = len(time_str) * char_width + (len(time_str) - 1) * char_spacing
          # Center the text horizontally in the 200px wide canvas
        canvas_width = 200
        start_x = (canvas_width - total_text_width) // 2
        
        # Vertical offset to center the 24px tall digits in the 40px canvas
        y_offset = (40 - 24) // 2
        
        for i, char in enumerate(time_str):
            x_pos = start_x + i * (char_width + char_spacing)
            
            if char == ':':
                # Draw colon as two dots (centered vertically)
                self.led_clock.create_oval(x_pos + 6, y_offset + 8, x_pos + 12, y_offset + 14, 
                                         fill=led_on_color, outline=led_on_color)
                self.led_clock.create_oval(x_pos + 6, y_offset + 16, x_pos + 12, y_offset + 22, 
                                         fill=led_on_color, outline=led_on_color)
            elif char == '.':
                # Draw decimal point as a small dot (centered vertically)
                self.led_clock.create_oval(x_pos + 8, y_offset + 20, x_pos + 14, y_offset + 26, 
                                         fill=led_on_color, outline=led_on_color)
            else:                # Draw digit using 7-segment display pattern
                self.draw_led_digit(x_pos, y_offset, char, led_on_color, led_off_color)

    def draw_led_digit(self, x, y_offset, digit, on_color, off_color):
        """Draw a single LED digit using 7-segment display pattern"""
        # 7-segment display patterns for digits 0-9
        segments = {
            '0': [1, 1, 1, 1, 1, 1, 0],  # top, top-right, bottom-right, bottom, bottom-left, top-left, middle
            '1': [0, 1, 1, 0, 0, 0, 0],
            '2': [1, 1, 0, 1, 1, 0, 1],
            '3': [1, 1, 1, 1, 0, 0, 1],
            '4': [0, 1, 1, 0, 0, 1, 1],
            '5': [1, 0, 1, 1, 0, 1, 1],
            '6': [1, 0, 1, 1, 1, 1, 1],
            '7': [1, 1, 1, 0, 0, 0, 0],
            '8': [1, 1, 1, 1, 1, 1, 1],
            '9': [1, 1, 1, 1, 0, 1, 1]
        }
        
        pattern = segments.get(digit, [0, 0, 0, 0, 0, 0, 0])
        
        # Segment coordinates (relative to x position)
        seg_coords = [
            # top
            [(2, 3), (10, 3), (9, 4), (3, 4)],
            # top-right  
            [(10, 4), (11, 5), (11, 11), (10, 12)],
            # bottom-right
            [(10, 13), (11, 14), (11, 20), (10, 21)],
            # bottom
            [(2, 21), (10, 21), (9, 20), (3, 20)],
            # bottom-left
            [(2, 13), (3, 14), (3, 20), (2, 21)],
            # top-left
            [(2, 4), (3, 5), (3, 11), (2, 12)],
            # middle
            [(3, 12), (9, 12), (9, 13), (3, 13)]
        ]
          # Draw each segment
        for i, coords in enumerate(seg_coords):
            color = on_color if pattern[i] else off_color
            # Convert relative coordinates to absolute (with vertical centering)
            abs_coords = []
            for px, py in coords:
                abs_coords.extend([x + px, y_offset + py])
            
            self.led_clock.create_polygon(abs_coords, fill=color, outline=color)
    
    def on_scroll_with_midi_sync(self, *args):
        """Handle scrollbar movement and sync MIDI playback position"""
        # Update canvas view first
        self.canvas.yview(*args)
        
        # Calculate MIDI position based on scroll position
        if hasattr(self, 'max_time') and self.max_time > 0:
            # Get current scroll position (0.0 to 1.0)
            scroll_top, scroll_bottom = self.canvas.yview()
            
            # In the visualization, time flows from bottom to top
            # Y coordinate mapping: y = total_height - (t / max_time) * total_height
            # So: t = 0 is at y = total_height (bottom)
            #     t = max_time is at y = 0 (top)
            
            # Calculate the time position based on the bottom of the visible area
            # When scroll_bottom = 1.0 (at bottom), we want time = 0
            # When scroll_top = 0.0 (at top), we want time = max_time
            time_position = (1.0 - scroll_bottom) * self.max_time
              # Update MIDI playback position
            self.playback_position = max(0.0, min(time_position, self.max_time))
            print(f"DEBUG: Scroll position updated to {self.playback_position:.2f}s (from scroll_bottom: {scroll_bottom:.3f})")
              # Update LED clock immediately (lightweight)
            self.update_led_clock()
            
            # Smart highlighting updates: immediate for small files, throttled for large files
            if hasattr(self, 'rect_data') and len(self.rect_data) > 3000:
                # Large file: Use throttling but allow periodic updates during continuous scrolling
                if hasattr(self, 'scroll_update_timer') and self.scroll_update_timer:
                    # Check if enough time has passed for a periodic update during scroll
                    current_time = time.time()
                    if not hasattr(self, 'last_highlight_time'):
                        self.last_highlight_time = 0
                    
                    # Allow highlighting every 200ms during continuous scrolling
                    if current_time - self.last_highlight_time > 0.2:
                        self.update_keyboard_highlighting()
                        self.last_highlight_time = current_time
                        # Cancel the pending timer since we just updated
                        self.after_cancel(self.scroll_update_timer)
                        self.scroll_update_timer = None
                    else:
                        # Still within the 200ms window, keep the existing timer
                        pass
                else:
                    # No pending timer, schedule immediate update for large files
                    self.update_keyboard_highlighting()
                    self.last_highlight_time = time.time()
                
                # Always schedule a final update when scrolling stops
                if hasattr(self, 'scroll_update_timer') and self.scroll_update_timer:
                    self.after_cancel(self.scroll_update_timer)
                self.scroll_update_timer = self.after(self.scroll_throttle_delay, self.delayed_highlight_update)
            else:
                # Small file: Update immediately for responsive feel
                self.update_keyboard_highlighting()
            
            # If we're at the end, stop playback
            if self.playback_position >= self.max_time and self.is_playing:
                self.stop_midi()
    
    def delayed_highlight_update(self):
        """Update keyboard highlighting after scroll throttle delay"""
        self.update_keyboard_highlighting()
        self.scroll_update_timer = None

    def sync_scrollbar_to_midi_position(self):
        """Update scrollbar position to match current MIDI playback position"""
        if hasattr(self, 'max_time') and self.max_time > 0:
            # Calculate scroll position from MIDI position
            # We want: playback_position 0.0 → scroll_bottom = 1.0 (at bottom)
            #          playback_position max_time → scroll_bottom = visible_height (at top)
            
            # For simplicity, position the playback time at the bottom of the visible area
            # scroll_bottom = 1.0 - (playback_position / max_time)
            target_scroll_bottom = 1.0 - (self.playback_position / self.max_time)
            
            # Get current view height
            current_top, current_bottom = self.canvas.yview()
            view_height = current_bottom - current_top
            
            # Calculate where the top should be to put playback_position at bottom
            target_scroll_top = target_scroll_bottom - view_height
            
            # Clamp to valid range
            target_scroll_top = max(0.0, min(1.0 - view_height, target_scroll_top))
            
            # Move canvas to the calculated position
            self.canvas.yview_moveto(target_scroll_top)

    def seek_relative(self, delta_seconds):
        """Seek relative to current position by the specified number of seconds"""
        if not hasattr(self, 'max_time') or self.max_time <= 0:
            return
            
        # Calculate new position
        new_position = max(0.0, min(self.playback_position + delta_seconds, self.max_time))
        
        # Update playback position
        self.playback_position = new_position
          # If currently playing, restart playback from new position
        # This ensures consistent timing regardless of seek distance
        if self.is_playing:
            # Stop current playback and restart from new position
            self.stop_midi()
            self.start_midi_playback()
            
        # Update scrollbar to match new position
        self.sync_scrollbar_to_midi_position()
        
        # Update LED clock
        self.update_led_clock()
          # Update keyboard highlighting        self.update_keyboard_highlighting()    def destroy(self):
        """Clean up resources when closing the application"""
        try:
            # Stop any playing MIDI
            if self.is_playing:
                self.stop_midi()
            
            # Save window geometry
            geometry = self.geometry()
            config = self.config_data
            config['geometry'] = geometry
            config['y_scale'] = self.y_scale_var.get()
            save_config(config)
            
        except Exception as e:
            print(f"Warning: Error during cleanup: {e}")
            
        # Call parent destroy
        super().destroy()
        
    def refresh_midi_devices(self):
        """Refresh FluidSynth availability and setup"""
        try:
            # Try to import fluidsynth to check if it's available
            try:
                import fluidsynth
                fluidsynth_available = True
            except ImportError:
                fluidsynth_available = False
            
            if not fluidsynth_available:
                print("⚠ pyfluidsynth not installed. MIDI output will not be available.")
                print("ℹ To install: pip install pyfluidsynth")
                print("ℹ FluidSynth provides software MIDI synthesis - no external devices needed!")
                self.midi_output_dropdown['values'] = ['FluidSynth not installed - see console for help']
                self.midi_output_var.set('FluidSynth not installed - see console for help')
                self.update_midi_status_indicator()
                return
              # FluidSynth is available - it's always a single "device"
            output_names = ['FluidSynth Software Synthesizer']
            
            print("✓ FluidSynth available - software MIDI synthesis ready")
            print("ℹ FluidSynth provides built-in piano sounds with no external setup required")
            
            # Update dropdown values
            self.midi_output_dropdown['values'] = output_names
            self.midi_output_var.set(output_names[0])
            print(f"✓ MIDI output: {output_names[0]}")
                    
            # Automatically connect to FluidSynth
            self.on_midi_output_changed()
            
            # Update connection status
            self.update_midi_status_indicator()
            
        except Exception as e:
            print(f"Error checking FluidSynth availability: {e}")
            self.midi_output_dropdown['values'] = ['Error checking FluidSynth - see console']
            self.midi_output_var.set('Error checking FluidSynth - see console')
            self.update_midi_status_indicator()
    
    def on_midi_output_changed(self, event=None):
        """Handle FluidSynth connection"""
        selected_device = self.midi_output_var.get()
        
        if 'not installed' in selected_device or 'Error' in selected_device:
            return
            
        print(f"Initializing FluidSynth: {selected_device}")
        
        # Save selected device to config
        self.config_data['last_midi_output'] = selected_device
        save_config(self.config_data)
        
        # Initialize FluidSynth player
        try:
            if hasattr(self, 'note_player') and self.note_player:
                self.note_player.close()
            
            # Create new FluidSynth player (no device parameter needed)
            self.note_player = FluidSynthPlayer()
            
            if self.note_player.midi_out:  # This means FluidSynth initialized successfully
                self.midi_playback_available = True
                print(f"✓ FluidSynth ready for MIDI playback")
            else:
                self.midi_playback_available = False
                print(f"⚠ Failed to initialize FluidSynth")
                
        except Exception as e:
            print(f"Error initializing FluidSynth: {e}")
            self.midi_playback_available = False
            
        # Update status indicator
        self.update_midi_status_indicator()
    
    def update_midi_status_indicator(self):
        """Update the connection status indicator (green/red circle)"""
        self.status_canvas.delete('all')
        
        # Determine connection status
        is_connected = (hasattr(self, 'note_player') and 
                       self.note_player and 
                       self.note_player.midi_out is not None)
        
        # Draw status circle
        color = '#00aa00' if is_connected else '#aa0000'  # Green if connected, red if not
        self.status_canvas.create_oval(2, 2, 14, 14, fill=color, outline='#333333')
        
        # Create tooltip information
        if is_connected:
            device_name = getattr(self.note_player.midi_out, 'name', 'Unknown Device')
            tooltip_text = f"Connected to: {device_name}"
        else:
            tooltip_text = "Not connected - select a MIDI device"
            
        # Simple status display on click
        def show_status():
            print(f"MIDI Status: {tooltip_text}")
            
        self.status_canvas.bind('<Button-1>', lambda e: show_status())


if __name__ == "__main__":
    print("Starting Python Midi Gapper 2...")
    try:
        print("Creating MidiGapperGUI instance...")
        app = MidiGapperGUI()
        print("Starting main loop...")
        app.mainloop()
        print("Main loop exited.")
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
