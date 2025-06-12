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
    def __init__(self):
        super().__init__()
        self.title('Python Midi Gapper 2')
        # Load window geometry
        self.config_data = load_config()
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
        # Create UI
        self.create_widgets()
        # Initialize channel-color and instrument mapping
        self.channel_colors = {}
        self.channel_instruments = {}
        # Autoload last MIDI file if available
        last = self.config_data.get('last_midi')
        if last and os.path.exists(last):
            # Delay autoload until GUI is idle so layout is complete
            self.after_idle(lambda: self.process_midi(last))
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Load MIDI button at top
        load_btn = ttk.Button(self, text='Load MIDI File', command=self.load_midi_file)
        load_btn.pack(side='top', anchor='w', padx=5, pady=5)

        # Channel legend at top-right
        self.channel_frame = ttk.LabelFrame(self, text='Channels')
        self.channel_frame.pack(side='top', anchor='ne', padx=5, pady=5)

        # Notebook for tabs at bottom
        notebook = ttk.Notebook(self)
        notebook.pack(side='bottom', fill='both', expand=True)

        # Visualization tab
        vis_frame = ttk.Frame(notebook)
        notebook.add(vis_frame, text='Visualization')
        # Container for canvas and scrollbar
        canvas_container = ttk.Frame(vis_frame)
        canvas_container.pack(fill='both', expand=True)
        # Visualization canvas with vertical scroll enabled
        self.canvas = tk.Canvas(canvas_container, bg='black', yscrollincrement=1)
        self.canvas.pack(fill='both', expand=True, side='left')
        # Vertical scrollbar for visualization
        v_scroll = ttk.Scrollbar(canvas_container, orient='vertical', command=self.canvas.yview)
        v_scroll.pack(fill='y', side='right')
        self.canvas.configure(yscrollcommand=v_scroll.set)
        # Redraw visualization on canvas resize (fix autoload sizing issues)
        self.canvas.bind('<Configure>', lambda e: self.draw_visualization(self.notes, self.max_time))

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
        self.update_channel_legend()
        # XML conversion
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
        # Build detailed visualization data (start, duration, velocity)
        self.notes_for_visualization.clear()
        active_notes = {}
        for track in mf.tracks:
            abs_time = 0.0
            tempo = 500000
            for msg in track:
                abs_time += mido.tick2second(msg.time, mf.ticks_per_beat, tempo)
                if msg.is_meta and msg.type == 'set_tempo':
                    tempo = msg.tempo
                if hasattr(msg, 'channel') and msg.type == 'note_on' and msg.velocity > 0:
                    active_notes[(msg.channel, msg.note)] = {'start': abs_time, 'velocity': msg.velocity}
                elif hasattr(msg, 'channel') and (msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)):
                    key = (msg.channel, msg.note)
                    if key in active_notes:
                        info = active_notes.pop(key)
                        duration = abs_time - info['start']
                        self.notes_for_visualization.append({
                            'channel': key[0], 'note': key[1],
                            'start_time': info['start'], 'duration': duration,
                            'velocity': info['velocity']
                        })
        # Prepare notes for drawing
        self.notes = [(d['start_time'], d['note'], d['channel']) for d in self.notes_for_visualization]
        # Compute max_time including durations
        self.max_time = max((d['start_time'] + d['duration'] for d in self.notes_for_visualization), default=1)
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

    def save_gapped_midi(self):
        """Save the current MIDI file, applying gap modifications and excluding deleted channels."""
        if not self.midi_data or not self.current_midi_file:
            messagebox.showerror("Error", "No MIDI file loaded to save.")
            return
        save_path = filedialog.asksaveasfilename(
            initialfile=os.path.splitext(os.path.basename(self.current_midi_file))[0] + '_gapped.mid',
            defaultextension='.mid', filetypes=[('MIDI files', '*.mid')], title='Save MIDI File'
        )
        if not save_path:
            return
        try:
            if not self.modifications_applied and not self.deleted_channels:
                shutil.copyfile(self.current_midi_file, save_path)
                messagebox.showinfo("Save Complete", f"MIDI saved to {save_path}")
                return
            new_midi = MidiFile(type=self.midi_data.type, ticks_per_beat=self.midi_data.ticks_per_beat)
            active_channels = set(range(16)) - self.deleted_channels
            # Build modification map
            mod_map = {}
            for note in self.notes_for_visualization:
                if note['channel'] in active_channels:
                    key = (note['channel'], note['note'], round(note['start_time'],8), note['velocity'])
                    mod_map[key] = note['duration']
            max_end = 0.0
            for track in self.midi_data.tracks:
                new_track = MidiTrack()
                new_midi.tracks.append(new_track)
                abs_time = 0.0; tempo=500000; active={}; pending=[]
                for msg in track:
                    delta = mido.tick2second(msg.time, self.midi_data.ticks_per_beat, tempo)
                    abs_time += delta
                    if msg.is_meta and msg.type=='set_tempo': tempo=msg.tempo
                    if hasattr(msg,'channel') and msg.channel not in active_channels: continue
                    entry={'msg':msg,'abs':abs_time,'mod':None}
                    pending.append(entry)
                    if msg.type=='note_on' and msg.velocity>0:
                        active[(msg.channel,msg.note)]={'start':abs_time,'velocity':msg.velocity}
                    elif msg.type in ('note_off','note_on') and msg.velocity==0:
                        key=(msg.channel,msg.note)
                        if key in active:
                            start=active.pop(key)['start']
                            mod_key=(key[0],key[1],round(start,8),entry['msg'].velocity)
                            if mod_key in mod_map:
                                entry['mod']=start+mod_map[mod_key]
                                max_end=max(max_end, entry['mod'])
                # write new track
                abs_new=0.0; tempo=500000
                for e in pending:
                    msg=e['msg']; tgt=e['mod'] or e['abs']
                    if msg.is_meta and msg.type=='set_tempo': tempo=msg.tempo
                    delta_s=max(0,tgt-abs_new)
                    dt=int(round(mido.second2tick(delta_s,self.midi_data.ticks_per_beat,tempo)))
                    new_track.append(msg.copy(time=dt)); abs_new+=delta_s
                # end of track
                if new_track and new_track[-1].is_meta and new_track[-1].type=='end_of_track': new_track.pop()
                pad = max(0, max_end-abs_new+0.01)
                new_track.append(mido.MetaMessage('end_of_track',time=int(round(mido.second2tick(pad,self.midi_data.ticks_per_beat,tempo)))))
            new_midi.tracks=[t for t in new_midi.tracks if len(t)>1 or (len(t)==1 and not t[0].is_meta)]
            new_midi.save(save_path)
            messagebox.showinfo("Save Complete", f"MIDI saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save MIDI:\n{e}\n{traceback.format_exc()}")

    def draw_visualization(self, notes, max_time):
        self.canvas.delete('all')
        self.canvas.update_idletasks()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        # Dimensions for keys: white and black key widths, note height, and corner radius
        white_key_w = width / 88
        black_key_w = white_key_w * 0.75
        note_h = 10
        radius = 4
        # Draw each note
        for time, note, channel in notes:
            # Calculate key index (0 to 87)
            idx = note - 21
            # Determine if the key is black (C#=1, D#=3, F#=6, G#=8, A#=10)
            semitone = note % 12
            is_black = semitone in {1, 3, 6, 8, 10}
            # Set note width accordingly
            note_w = black_key_w if is_black else white_key_w
            # X center: place each key evenly across the canvas
            x_center = (idx + 0.5) * white_key_w
            # Y position by time
            y_center = height - (time / max_time) * height
            x1 = x_center - note_w / 2
            y1 = y_center - note_h / 2
            x2 = x_center + note_w / 2
            y2 = y_center + note_h / 2
            # Draw rounded rectangle (corners and center) with channel color
            color = self.channel_colors.get(channel, '#cccccc')
            self.canvas.create_rectangle(x1+radius, y1, x2-radius, y2, fill=color, outline='')
            self.canvas.create_rectangle(x1, y1+radius, x2, y2-radius, fill=color, outline='')
            self.canvas.create_oval(x1, y1, x1+2*radius, y1+2*radius, fill=color, outline='')
            self.canvas.create_oval(x2-2*radius, y1, x2, y1+2*radius, fill=color, outline='')
            self.canvas.create_oval(x1, y2-2*radius, x1+2*radius, y2, fill=color, outline='')
            self.canvas.create_oval(x2-2*radius, y2-2*radius, x2, y2, fill=color, outline='')
        # Update scroll region to encompass all notes
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # Auto-scroll to bottom (latest notes at top of canvas)
        self.canvas.yview_moveto(1.0)

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
                # Build notes from XML with cumulative times per track
                notes = []
                for tr in root.findall('Track'):
                    cumulative = 0
                    for msg_elem in tr.findall('Message'):
                        dt = int(msg_elem.get('time', '0'))
                        cumulative += dt
                        if msg_elem.get('type') == 'note_on' and int(msg_elem.get('velocity', '0')) > 0:
                            note = int(msg_elem.get('note', '0'))
                            ch = int(msg_elem.get('channel', '0'))
                            notes.append((cumulative, note, ch))
                # Store notes and max_time then redraw
                self.notes = notes
                self.max_time = max((t for t, *_ in notes), default=1)
                self.draw_visualization(self.notes, self.max_time)

    def on_closing(self):
        # Save window geometry
        self.config_data['geometry'] = self.geometry()
        save_config(self.config_data)
        self.destroy()

    def update_channel_legend(self):
        # Clear existing legend
        for child in self.channel_frame.winfo_children():
            child.destroy()
        # Create legend items per channel
        for ch, color in sorted(self.channel_colors.items()):
            program = self.channel_instruments.get(ch, 0)
            instr = GM_INSTRUMENTS[program] if program < len(GM_INSTRUMENTS) else 'Unknown'
            item = tk.Frame(self.channel_frame)
            # Pack items vertically
            item.pack(side='top', anchor='w', pady=2)
            dot = tk.Canvas(item, width=12, height=12, bg=color, highlightthickness=0)
            dot.pack(side='left', padx=(0,4))
            lbl = ttk.Label(item, text=f'Ch {ch}: {instr}', foreground=color)
            lbl.pack(side='left')

if __name__ == '__main__':
    app = MidiGapperGUI()
    app.mainloop()
