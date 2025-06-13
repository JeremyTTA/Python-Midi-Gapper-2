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

# Predefined distinct colors for channels
DEFAULT_CHANNEL_COLORS = [
    '#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4',
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

class MidiGapperGUI(tk.Tk):
    # Map MIDI note number to note name
    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def __init__(self):
        super().__init__()
        self.title('Python Midi Gapper 2')
        # Create a menu bar with File -> Load MIDI File
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Load MIDI File', command=self.load_midi_file)
        menu_bar.add_cascade(label='File', menu=file_menu)
        self.config(menu=menu_bar)
        # Load window geometry
        self.config_data = load_config()
        # Default tempo in microseconds per quarter note
        self.tempo_us = 500000
        # Y-scale multiplier for visualization
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
        self.vis_font = tkfont.Font(family=default_font.cget("family"), size=new_size)
        # Initialize channel-color and instrument mapping
        self.channel_colors = {}
        self.channel_instruments = {}        # Autoload last MIDI file if available
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
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Header frame containing midi info
        header_frame = ttk.Frame(self)
        header_frame.pack(side='top', fill='x')
        # MIDI info display
        self.midi_info_var = tk.StringVar(value='')
        info_label = ttk.Label(header_frame, textvariable=self.midi_info_var, anchor='center')
        info_label.pack(side='left', expand=True)

        # Channel legend at top
        self.channel_frame = ttk.LabelFrame(header_frame, text='Channels')
        self.channel_frame.pack(side='right', anchor='ne', padx=5, pady=5)

        # Notebook for tabs at bottom
        notebook = ttk.Notebook(self)
        notebook.pack(side='bottom', fill='both', expand=True)

        # Visualization tab
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
        # Visualization canvas with vertical scroll enabled
        self.canvas = tk.Canvas(canvas_container, bg='black', yscrollincrement=1)
        self.canvas.pack(fill='both', expand=True, side='left')
        # Vertical scrollbar for visualization
        v_scroll = ttk.Scrollbar(canvas_container, orient='vertical', command=self.canvas.yview)
        v_scroll.pack(fill='y', side='right')
        self.canvas.configure(yscrollcommand=v_scroll.set)        # Redraw visualization on canvas resize (fix autoload sizing issues)
        def on_canvas_configure(event):
            # Don't scroll to bottom on resize events, only on initial load
            if hasattr(self, 'notes') and self.notes:
                self.draw_visualization(self.notes, self.max_time)
        self.canvas.bind('<Configure>', on_canvas_configure)
        # Enable scrolling of visualization with mouse wheel and arrow keys
        self.canvas.bind('<Enter>', lambda e: self.canvas.focus_set())
        # Increase scroll speed by using a multiplier for faster scrolling
        scroll_factor = 20
        self.bind_all('<MouseWheel>', lambda e: self.canvas.yview_scroll(-scroll_factor * int(e.delta/120), 'units'))
        self.bind_all('<Up>', lambda e: self.canvas.yview_scroll(-scroll_factor, 'units'))
        self.bind_all('<Down>', lambda e: self.canvas.yview_scroll(scroll_factor, 'units'))

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
        # XML conversion with absolute time and duration for notes
        def format_abs(sec):
            m = int(sec // 60)
            s = sec - m*60
            return f"{m:02d}:{s:05.3f}"
        def format_dur(sec):
            return f"{sec:05.3f}"
        # Prepare visualization data
        self.notes_for_visualization = []
        # Build XML root
        root = ET.Element('MidiFile', ticks_per_beat=str(mf.ticks_per_beat))
        for i, track in enumerate(mf.tracks):
            tr_elem = ET.SubElement(root, 'Track', name=track.name or f'Track_{i}')
            abs_time = 0.0
            tempo = 500000
            active_on = {}
            for msg in track:
                # accumulate real time
                delta = mido.tick2second(msg.time, mf.ticks_per_beat, tempo)
                abs_time += delta
                if msg.is_meta and msg.type == 'set_tempo':
                    tempo = msg.tempo
                attrs = msg.dict()
                msg_elem = ET.SubElement(tr_elem, 'Message', type=msg.type, time=str(msg.time))
                # set standard attributes
                for attr, value in attrs.items():
                    if attr not in ('type', 'time'):
                        msg_elem.set(attr, str(value))
                # note_on: record absolute time
                if msg.type == 'note_on' and getattr(msg, 'velocity', 0) > 0:
                    active_on[(msg.channel, msg.note)] = (msg_elem, abs_time)
                    msg_elem.set('abs_time', format_abs(abs_time))
                # note_off: calculate duration
                elif msg.type == 'note_off' or (msg.type == 'note_on' and getattr(msg, 'velocity', 0) == 0):
                    key = (getattr(msg, 'channel', None), getattr(msg, 'note', None))
                    if key in active_on:
                        start_elem, start_time = active_on.pop(key)
                        duration = abs_time - start_time
                        start_elem.set('duration', format_dur(duration))
                        # Record raw note data for visualization
                        self.notes_for_visualization.append({'start_time': start_time, 'note': key[1], 'channel': key[0], 'duration': duration})
        pretty_xml = minidom.parseString(ET.tostring(root, encoding='utf-8')).toprettyxml(indent="  ")
        self.text.insert('end', pretty_xml)
        # Populate visualization notes from processed MIDI data (mido-based for accurate durations)
        self.notes = [(d['start_time'], d['note'], d['channel'], d['duration']) for d in self.notes_for_visualization]
        self.max_time = max((d['start_time'] + d['duration'] for d in self.notes_for_visualization), default=1)
        # Update the MIDI info label with all tempo changes
        # Convert tempo_changes (microseconds per quarter note) to BPM list
        tempos_us = [msg.tempo for track in mf.tracks for msg in track if msg.is_meta and msg.type == 'set_tempo']
        if not tempos_us:
            tempos_us = [self.tempo_us]
        tempos_bpm = [str(int(round(60e6/t))) for t in tempos_us]
        tempo_str = ','.join(tempos_bpm)
        fname = os.path.basename(file_path)
        # Show only filename and track count in header
        self.midi_info_var.set(f"{fname} | Tracks: {len(mf.tracks)}")
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
        radius = 2  # corner radius
        # Draw measure lines (assume 4/4 time)
        # seconds per quarter note from initial tempo
        spqn = self.tempo_us / 1e6
        meas_dur = 4 * spqn
        num_measures = int(max_time // meas_dur) + 1
        for m in range(1, num_measures + 1):
            t = m * meas_dur
            # map time to Y in total_height space (0 at top)
            y = total_height - (t / max_time) * total_height
            self.canvas.create_line(0, y, width, y, fill='#444')
            # Label time, measure number, and tempo just above the line in blue with larger font
            minutes = int(t // 60)
            seconds = t % 60
            time_str = f"{minutes:02d}:{seconds:05.3f}"
            bpm = int(round(60e6 / self.tempo_us))
            self.canvas.create_text(6, y - 14, text=f"{time_str} M{m} BPM{bpm}", anchor='nw', fill='white', font=self.vis_font)
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
            self.rect_data[tag] = {'note': note, 'start': time, 'dur': dur, 'gap': gap}
            # Bind hover events
            self.canvas.tag_bind(tag, '<Enter>', lambda e, t=tag: self.on_note_enter(e, t))
            self.canvas.tag_bind(tag, '<Leave>', lambda e: self.on_note_leave(e))        # Update scroll region to encompass all notes
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # Auto-scroll if flagged (e.g., after autoload), then clear flag
        if getattr(self, 'scroll_to_bottom_on_next_draw', False):
            self.canvas.yview_moveto(1.0)
            self.scroll_to_bottom_on_next_draw = False

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
                except Exception:
                    return
                # Build notes from XML: include start time and duration
                notes = []
                for tr in root.findall('Track'):
                    for msg_elem in tr.findall('Message'):
                        if msg_elem.get('type') == 'note_on' and int(msg_elem.get('velocity','0'))>0:
                            abs_str = msg_elem.get('abs_time'); dur_str = msg_elem.get('duration')
                            if abs_str:
                                m,s = abs_str.split(':'); start = int(m)*60 + float(s)
                                dur = float(dur_str) if dur_str is not None else 0.0
                                # skip zero or negative durations
                                if dur <= 0:
                                    continue
                                note = int(msg_elem.get('note','0')); ch = int(msg_elem.get('channel','0'))
                                notes.append((start, note, ch, dur))
                # Update notes and rescale
                self.notes = notes
                self.max_time = max((t+d for t,_,_,d in notes), default=1)
                self.draw_visualization(self.notes, self.max_time)

    def on_closing(self):
        # Save window geometry and Y-scale
        self.config_data['geometry'] = self.geometry()
        self.config_data['y_scale'] = self.y_scale_var.get()
        save_config(self.config_data)
        self.destroy()

    def update_channel_legend(self):
        # Clear existing legend
        for child in self.channel_frame.winfo_children():
            child.destroy()
        # Create legend items per channel with visibility checkbox
        for ch, color in sorted(self.channel_colors.items()):
            program = self.channel_instruments.get(ch, 0)
            instr = GM_INSTRUMENTS[program] if program < len(GM_INSTRUMENTS) else 'Unknown'
            item = tk.Frame(self.channel_frame)
            item.pack(side='top', anchor='w', pady=2)
            # Checkbox for visibility
            var = self.channel_vars.get(ch)
            if var is None:
                var = tk.BooleanVar(value=(ch in self.visible_channels))
                self.channel_vars[ch] = var
            cb = tk.Checkbutton(item, variable=var, command=lambda ch=ch: self.toggle_channel(ch))
            # Color indicator and label will be alongside checkbox
            dot = tk.Canvas(item, width=12, height=12, bg=color, highlightthickness=0)
            lbl = ttk.Label(item, text=f'Ch {ch}: {instr}', foreground=color)
            # Pack widgets
            cb.pack(side='left')
            dot.pack(side='left', padx=(4,4))
            lbl.pack(side='left')
            # Define click handlers
            def on_left(e, ch=ch, var=var):
                var.set(not var.get())
                self.toggle_channel(ch)
            def on_right(e, ch=ch, var=var):
                self.select_only_channel(ch)
            # Bind left-click and right-click on row frame, dot, and label only (checkbox handles its own toggle)
            for widget in (item, dot, lbl):
                widget.bind('<Button-1>', on_left)
                widget.bind('<Button-3>', on_right)
            # Checkbox right-click selects only this channel
            cb.bind('<Button-3>', on_right)

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

if __name__ == '__main__':
    app = MidiGapperGUI()
    app.mainloop()
