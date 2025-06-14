#!/usr/bin/env python3
"""
Simple test to verify MIDI -> XML -> MIDI round-trip conversion
"""

import sys
import os
import mido
import xml.etree.ElementTree as ET
import tempfile
from mido import MidiFile, MidiTrack

def test_conversion():
    print("=== MIDI Round-trip Conversion Test ===")
    
    # Look for a MIDI file to test with
    midi_files = [f for f in os.listdir('.') if f.endswith('.mid') or f.endswith('.midi')]
    
    if not midi_files:
        print("No MIDI files found in current directory for testing")
        # Create a simple test MIDI file
        test_midi = mido.MidiFile()
        track = mido.MidiTrack()
        track.append(mido.Message('program_change', channel=0, program=1, time=0))
        track.append(mido.Message('note_on', channel=0, note=60, velocity=64, time=0))
        track.append(mido.Message('note_off', channel=0, note=60, velocity=64, time=480))
        track.append(mido.MetaMessage('end_of_track', time=0))
        test_midi.tracks.append(track)
        
        test_midi.save('test_input.mid')
        test_file = 'test_input.mid'
        print(f"Created test MIDI file: {test_file}")
    else:
        test_file = midi_files[0]
        print(f"Using existing MIDI file: {test_file}")
    
    try:
        # Load original MIDI
        original_midi = mido.MidiFile(test_file)
        print(f"Original MIDI: {len(original_midi.tracks)} tracks, {original_midi.ticks_per_beat} ticks_per_beat")
        
        # Count original messages
        orig_msg_count = sum(len(track) for track in original_midi.tracks)
        print(f"Original message count: {orig_msg_count}")
        
        # Generate XML using the same logic as the main application
        xml_content = generate_xml_from_midi(original_midi)
        print(f"Generated XML length: {len(xml_content)} characters")
        
        # Parse the XML to check structure
        root = ET.fromstring(xml_content)
        xml_tracks = root.findall('Track')
        print(f"XML contains {len(xml_tracks)} tracks")
        
        xml_msg_count = sum(len(track.findall('Message')) for track in xml_tracks)
        print(f"XML message count: {xml_msg_count}")
        
        # Now test the save function - reconstruct MIDI from XML
        output_file = 'test_output.mid'
        reconstructed_midi = reconstruct_midi_from_xml(xml_content)
        
        # Save the reconstructed MIDI
        reconstructed_midi.save(output_file)
        print(f"Saved reconstructed MIDI: {output_file}")
        
        # Compare the results
        print(f"Reconstructed MIDI: {len(reconstructed_midi.tracks)} tracks, {reconstructed_midi.ticks_per_beat} ticks_per_beat")
        
        recon_msg_count = sum(len(track) for track in reconstructed_midi.tracks)
        print(f"Reconstructed message count: {recon_msg_count}")
        
        # Check if they match
        tracks_match = len(original_midi.tracks) == len(reconstructed_midi.tracks)
        ticks_match = original_midi.ticks_per_beat == reconstructed_midi.ticks_per_beat
        messages_match = orig_msg_count == recon_msg_count
        
        print(f"\nComparison Results:")
        print(f"Tracks match: {tracks_match} ({len(original_midi.tracks)} vs {len(reconstructed_midi.tracks)})")
        print(f"Ticks per beat match: {ticks_match} ({original_midi.ticks_per_beat} vs {reconstructed_midi.ticks_per_beat})")
        print(f"Message count match: {messages_match} ({orig_msg_count} vs {recon_msg_count})")
        
        if tracks_match and ticks_match and messages_match:
            print("\n✅ Round-trip conversion appears to be working correctly!")
        else:
            print("\n❌ Round-trip conversion has discrepancies.")
            
        # Clean up temp files
        try:
            if test_file == 'test_input.mid':
                os.unlink(test_file)
            os.unlink(output_file)
        except:
            pass
            
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()

def generate_xml_from_midi(mf):
    """Generate XML from MIDI file using the same logic as the main application"""
    # Build XML root
    root = ET.Element('MidiFile', ticks_per_beat=str(mf.ticks_per_beat))
    
    for i, track in enumerate(mf.tracks):
        tr_elem = ET.SubElement(root, 'Track', name=track.name or f'Track_{i}')
        abs_time = 0.0
        tempo = 500000
        
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
    
    return ET.tostring(root, encoding='unicode')

def reconstruct_midi_from_xml(xml_content):
    """Reconstruct MIDI file from XML using the same logic as save_midi_file"""
    root = ET.fromstring(xml_content)
    
    # Create new MIDI file from XML
    ticks_per_beat = int(root.get('ticks_per_beat', 480))
    new_midi = MidiFile(ticks_per_beat=ticks_per_beat)
    
    for track_elem in root.findall('Track'):
        track = MidiTrack()
        track.name = track_elem.get('name', '')
        
        # Sort messages by time for proper MIDI ordering
        messages = []
        for msg_elem in track_elem.findall('Message'):
            msg_type = msg_elem.get('type')
            time = int(msg_elem.get('time', 0))
            # Build message attributes
            attrs = {'type': msg_type, 'time': time}
            for key, value in msg_elem.attrib.items():
                if key not in ('type', 'time', 'abs_time', 'duration'):
                    # Convert numeric attributes
                    if key in ('channel', 'note', 'velocity', 'program', 'control', 'value', 'pitch', 
                              'port', 'numerator', 'denominator', 'clocks_per_click', 
                              'notated_32nd_notes_per_beat'):
                        attrs[key] = int(value)
                    elif key == 'tempo':
                        attrs[key] = int(value)
                    else:
                        attrs[key] = value
            
            messages.append(attrs)
        
        # Sort by time and add to track
        messages.sort(key=lambda x: x['time'])
        for msg_attrs in messages:
            try:
                msg_type = msg_attrs['type']
                time = msg_attrs['time']
                # Build kwargs for message creation, excluding XML-specific attributes
                kwargs = {}
                for key, value in msg_attrs.items():
                    if key not in ('type', 'time', 'abs_time', 'duration'):
                        kwargs[key] = value
                
                # Create message based on type
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
                elif msg_type == 'pitchwheel':
                    msg = mido.Message(msg_type,
                                     channel=kwargs.get('channel', 0),
                                     pitch=kwargs.get('pitch', 0),
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
                elif msg_type in ['track_name', 'text', 'copyright', 'marker', 'cue_marker', 'lyrics']:
                    msg = mido.MetaMessage(msg_type, 
                                         text=kwargs.get('text', ''),
                                         time=time)
                elif msg_type == 'midi_port':
                    msg = mido.MetaMessage(msg_type,
                                         port=kwargs.get('port', 0),
                                         time=time)
                elif msg_type == 'end_of_track':
                    msg = mido.MetaMessage(msg_type, time=time)
                elif msg_type == 'sysex':
                    data = kwargs.get('data', [])
                    if isinstance(data, str):
                        try:
                            data = eval(data) if data.startswith('[') else []
                        except:
                            data = []
                    msg = mido.Message(msg_type, data=data, time=time)
                else:
                    print(f"Skipping unsupported message type: {msg_type}")
                    continue
                
                # Successfully created message
                track.append(msg)
                
            except Exception as e:
                print(f"Error processing message {msg_attrs}: {e}")
                continue
        
        # Add the completed track to the MIDI file
        new_midi.tracks.append(track)
    
    return new_midi

if __name__ == '__main__':
    test_conversion()
