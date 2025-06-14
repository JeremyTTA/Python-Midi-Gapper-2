#!/usr/bin/env python3
"""
Test script to verify MIDI save functionality
"""
import mido
import xml.etree.ElementTree as ET
from xml.dom import minidom

def test_midi_roundtrip():
    """Test loading a MIDI file, converting to XML, and saving back to MIDI"""
    
    # Create a simple test MIDI file
    print("Creating test MIDI file...")
    test_midi = mido.MidiFile()
    track = mido.MidiTrack()
    
    # Add some test messages
    track.append(mido.MetaMessage('set_tempo', tempo=500000, time=0))
    track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))
    track.append(mido.MetaMessage('key_signature', key='C', time=0))
    track.append(mido.MetaMessage('track_name', text='Test Track', time=0))
    track.append(mido.Message('program_change', channel=0, program=1, time=0))
    track.append(mido.Message('note_on', channel=0, note=60, velocity=64, time=0))
    track.append(mido.Message('note_off', channel=0, note=60, velocity=64, time=480))
    track.append(mido.MetaMessage('end_of_track', time=0))
    
    test_midi.tracks.append(track)
    test_midi.save('test_original.mid')
    print(f"Original MIDI: {len(test_midi.tracks)} tracks, {len(track)} messages")
    
    # Convert to XML format (simulate what the app does)
    print("\nConverting to XML...")
    root = ET.Element('MidiFile')
    root.set('ticks_per_beat', str(test_midi.ticks_per_beat))
    
    for i, track in enumerate(test_midi.tracks):
        track_elem = ET.SubElement(root, 'Track')
        track_elem.set('index', str(i))
        track_elem.set('name', getattr(track, 'name', f'Track {i}'))
        
        for msg in track:
            msg_elem = ET.SubElement(track_elem, 'Message')
            msg_elem.set('type', msg.type)
            msg_elem.set('time', str(msg.time))
            
            # Add all message attributes
            for attr, value in msg.dict().items():
                if attr not in ('type', 'time'):
                    msg_elem.set(attr, str(value))
    
    # Convert back to MIDI (simulate save functionality)
    print("Converting back to MIDI...")
    new_midi = mido.MidiFile(ticks_per_beat=int(root.get('ticks_per_beat', 480)))
    
    for track_elem in root.findall('Track'):
        new_track = mido.MidiTrack()
        new_track.name = track_elem.get('name', '')
        
        # Sort messages by time
        messages = []
        for msg_elem in track_elem.findall('Message'):
            msg_type = msg_elem.get('type')
            time = int(msg_elem.get('time', 0))
            
            # Build message attributes
            attrs = {'type': msg_type, 'time': time}
            for key, value in msg_elem.attrib.items():
                if key not in ('type', 'time'):
                    # Convert numeric attributes
                    if key in ('channel', 'note', 'velocity', 'program', 'control', 'value', 'pitch', 
                              'port', 'numerator', 'denominator', 'clocks_per_click', 
                              'notated_32nd_notes_per_beat', 'tempo'):
                        attrs[key] = int(value)
                    else:
                        attrs[key] = value
            
            messages.append(attrs)
        
        messages.sort(key=lambda x: x['time'])
        
        for msg_attrs in messages:
            try:
                msg_type = msg_attrs['type']
                time = msg_attrs['time']
                
                # Create message based on type
                if msg_type in ['note_on', 'note_off']:
                    msg = mido.Message(msg_type, 
                                     channel=msg_attrs.get('channel', 0),
                                     note=msg_attrs.get('note', 60),
                                     velocity=msg_attrs.get('velocity', 64),
                                     time=time)
                elif msg_type == 'program_change':
                    msg = mido.Message(msg_type,
                                     channel=msg_attrs.get('channel', 0),
                                     program=msg_attrs.get('program', 0),
                                     time=time)
                elif msg_type == 'set_tempo':
                    msg = mido.MetaMessage(msg_type, 
                                         tempo=msg_attrs.get('tempo', 500000),
                                         time=time)
                elif msg_type == 'time_signature':
                    msg = mido.MetaMessage(msg_type,
                                         numerator=msg_attrs.get('numerator', 4),
                                         denominator=msg_attrs.get('denominator', 4),
                                         clocks_per_click=msg_attrs.get('clocks_per_click', 24),
                                         notated_32nd_notes_per_beat=msg_attrs.get('notated_32nd_notes_per_beat', 8),
                                         time=time)
                elif msg_type == 'key_signature':
                    msg = mido.MetaMessage(msg_type,
                                         key=msg_attrs.get('key', 'C'),
                                         time=time)
                elif msg_type in ['track_name', 'text', 'copyright', 'marker', 'cue_marker', 'lyrics']:
                    msg = mido.MetaMessage(msg_type, 
                                         text=msg_attrs.get('text', ''),
                                         time=time)
                elif msg_type == 'end_of_track':
                    msg = mido.MetaMessage(msg_type, time=time)
                else:
                    print(f"Skipping unsupported message type: {msg_type}")
                    continue
                
                new_track.append(msg)
                print(f"Successfully created {msg_type} message")
                
            except Exception as e:
                print(f"Failed to create message {msg_attrs}: {e}")
                continue
        
        new_midi.tracks.append(new_track)
    
    # Save the reconstructed MIDI
    new_midi.save('test_reconstructed.mid')
    print(f"\nReconstructed MIDI: {len(new_midi.tracks)} tracks")
    
    # Compare original and reconstructed
    print(f"\nComparison:")
    print(f"Original tracks: {len(test_midi.tracks)}, Reconstructed tracks: {len(new_midi.tracks)}")
    print(f"Original messages: {len(test_midi.tracks[0])}, Reconstructed messages: {len(new_midi.tracks[0])}")
    
    print("\nOriginal messages:")
    for i, msg in enumerate(test_midi.tracks[0]):
        print(f"  {i}: {msg}")
    
    print("\nReconstructed messages:")
    for i, msg in enumerate(new_midi.tracks[0]):
        print(f"  {i}: {msg}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_midi_roundtrip()
