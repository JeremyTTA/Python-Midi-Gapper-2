#!/usr/bin/env python3
"""
Simple test to identify MIDI/XML conversion issues
"""
import mido
from mido import MidiFile
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

def test_conversion():
    # Use the MIDI file from config
    midi_file = "C:/Users/JeremyStandlee/Desktop/Midi Files/A HA.Take on me  K-modified.mid"
    
    if not os.path.exists(midi_file):
        # Try alternative location
        midi_file = "C:/Users/JeremyStandlee/Desktop/Midi Files/A HA.Take on me  K.mid"
        if not os.path.exists(midi_file):
            print(f"MIDI file not found: {midi_file}")
            return
    
    print(f"Testing with MIDI file: {midi_file}")
    
    try:
        # Load MIDI file
        mf = MidiFile(midi_file)
        print(f"Original MIDI: {len(mf.tracks)} tracks, ticks_per_beat={mf.ticks_per_beat}")
        
        # Convert to XML (simplified version of what the app does)
        root = ET.Element('MidiFile', ticks_per_beat=str(mf.ticks_per_beat))
        
        for i, track in enumerate(mf.tracks):
            print(f"Processing track {i}: {len(track)} messages")
            tr_elem = ET.SubElement(root, 'Track', name=track.name or f'Track_{i}')
            
            for msg in track:
                attrs = msg.dict()
                msg_elem = ET.SubElement(tr_elem, 'Message', type=msg.type, time=str(msg.time))
                
                # Set all attributes
                for attr, value in attrs.items():
                    if attr not in ('type', 'time'):
                        msg_elem.set(attr, str(value))
        
        print(f"XML created with {len(root)} tracks")
        
        # Convert XML back to MIDI
        new_midi = MidiFile(ticks_per_beat=int(root.get('ticks_per_beat', 480)))
        
        for track_elem in root.findall('Track'):
            track = mido.MidiTrack()
            track.name = track_elem.get('name', '')
            
            messages = []
            for msg_elem in track_elem.findall('Message'):
                msg_type = msg_elem.get('type')
                time = int(msg_elem.get('time', 0))
                
                attrs = {'type': msg_type, 'time': time}
                for key, value in msg_elem.attrib.items():
                    if key not in ('type', 'time'):
                        # Try to convert to int for numeric attributes
                        if key in ('channel', 'note', 'velocity', 'program', 'control', 'value', 'pitch', 
                                  'port', 'numerator', 'denominator', 'clocks_per_click', 
                                  'notated_32nd_notes_per_beat', 'tempo'):
                            try:
                                attrs[key] = int(value)
                            except:
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
                    kwargs = {k: v for k, v in msg_attrs.items() if k not in ('type', 'time')}
                    
                    # Try to create the message
                    if msg_type in ['note_on', 'note_off']:
                        msg = mido.Message(msg_type, 
                                         channel=kwargs.get('channel', 0),
                                         note=kwargs.get('note', 60),
                                         velocity=kwargs.get('velocity', 64),
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
                    elif msg_type in ['track_name', 'text', 'copyright', 'marker', 'cue_marker', 'lyrics']:
                        msg = mido.MetaMessage(msg_type, 
                                             text=kwargs.get('text', ''),
                                             time=time)
                    else:
                        print(f"Unsupported message type: {msg_type}")
                        fail_count += 1
                        continue
                    
                    track.append(msg)
                    success_count += 1
                    
                except Exception as e:
                    print(f"Failed to create {msg_type}: {e}")
                    print(f"  Attributes: {msg_attrs}")
                    fail_count += 1
            
            new_midi.tracks.append(track)
            print(f"Track '{track.name}': {success_count} success, {fail_count} failures")
        
        print(f"\nResult:")
        print(f"Original: {len(mf.tracks)} tracks")
        print(f"Reconstructed: {len(new_midi.tracks)} tracks")
        
        for i, (orig, recon) in enumerate(zip(mf.tracks, new_midi.tracks)):
            print(f"Track {i}: {len(orig)} -> {len(recon)} messages")
            if len(orig) != len(recon):
                print(f"  *** MESSAGE COUNT MISMATCH ***")
        
        # Save test files
        new_midi.save('test_reconstructed.mid')
        print(f"Saved reconstructed MIDI as: test_reconstructed.mid")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_conversion()
