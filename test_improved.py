#!/usr/bin/env python3
"""
Test the improved MIDI save function
"""

import mido
import xml.etree.ElementTree as ET
from mido import MidiFile, MidiTrack
import os

def create_test_midi():
    """Create a comprehensive test MIDI file with various message types"""
    midi = MidiFile()
    track = MidiTrack()
    
    # Add various message types
    track.append(mido.MetaMessage('set_tempo', tempo=355030, time=0))
    track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, 
                                clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    track.append(mido.MetaMessage('key_signature', key='A', time=0))
    track.append(mido.Message('program_change', channel=0, program=37, time=0))
    track.append(mido.Message('control_change', channel=0, control=7, value=100, time=0))
    track.append(mido.Message('note_on', channel=0, note=60, velocity=64, time=0))
    track.append(mido.Message('note_off', channel=0, note=60, velocity=64, time=480))
    track.append(mido.Message('pitchwheel', channel=0, pitch=1000, time=0))
    track.append(mido.MetaMessage('end_of_track', time=0))
    
    midi.tracks.append(track)
    return midi

def midi_to_xml(midi_file):
    """Convert MIDI to XML using the same logic as the main application"""
    root = ET.Element('MidiFile', ticks_per_beat=str(midi_file.ticks_per_beat))
    
    for i, track in enumerate(midi_file.tracks):
        tr_elem = ET.SubElement(root, 'Track', name=track.name or f'Track_{i}')
        
        for msg in track:
            attrs = msg.dict()
            msg_elem = ET.SubElement(tr_elem, 'Message', type=msg.type, time=str(msg.time))
            
            # set standard attributes
            for attr, value in attrs.items():
                if attr not in ('type', 'time'):
                    msg_elem.set(attr, str(value))
    
    return ET.tostring(root, encoding='unicode')

def xml_to_midi(xml_content):
    """Convert XML back to MIDI using the improved logic"""
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
                    attrs[key] = value  # Keep as string initially
            
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
                        msg = mido.MetaMessage(msg_type, time=time, **kwargs)
                    else:
                        # Create regular Message with all available kwargs
                        msg = mido.Message(msg_type, time=time, **kwargs)
                        
                except Exception as e:
                    print(f"Failed to create message {msg_type} with kwargs {kwargs}: {e}")
                    continue
                    
                # Successfully created message
                track.append(msg)
                
            except Exception as e:
                print(f"Error processing message {msg_attrs}: {e}")
                continue
        
        # Add the completed track to the MIDI file
        new_midi.tracks.append(track)
    
    return new_midi

def test_roundtrip():
    """Test the complete round-trip conversion"""
    print("=== Testing Improved MIDI Conversion ===")
    
    # Create test MIDI
    original_midi = create_test_midi()
    print(f"Original MIDI: {len(original_midi.tracks)} tracks, {original_midi.ticks_per_beat} ticks_per_beat")
    
    # Save original
    original_midi.save('test_original.mid')
    
    # Convert to XML
    xml_content = midi_to_xml(original_midi)
    print(f"Generated XML length: {len(xml_content)} characters")
    
    # Convert back to MIDI
    reconstructed_midi = xml_to_midi(xml_content)
    print(f"Reconstructed MIDI: {len(reconstructed_midi.tracks)} tracks, {reconstructed_midi.ticks_per_beat} ticks_per_beat")
    
    # Save reconstructed
    reconstructed_midi.save('test_reconstructed.mid')
    
    # Compare message by message
    print("\nDetailed comparison:")
    orig_track = original_midi.tracks[0]
    recon_track = reconstructed_midi.tracks[0]
    
    print(f"Original track: {len(orig_track)} messages")
    print(f"Reconstructed track: {len(recon_track)} messages")
    
    matches = 0
    for i, (orig_msg, recon_msg) in enumerate(zip(orig_track, recon_track)):
        print(f"\nMessage {i}:")
        print(f"  Original:     {orig_msg}")
        print(f"  Reconstructed: {recon_msg}")
        
        if orig_msg.dict() == recon_msg.dict():
            print(f"  ✅ Perfect match")
            matches += 1
        else:
            print(f"  ❌ Mismatch")
            orig_dict = orig_msg.dict()
            recon_dict = recon_msg.dict()
            
            for key in set(orig_dict.keys()) | set(recon_dict.keys()):
                orig_val = orig_dict.get(key, '<missing>')
                recon_val = recon_dict.get(key, '<missing>')
                if orig_val != recon_val:
                    print(f"    {key}: {orig_val} → {recon_val}")
    
    print(f"\nSummary: {matches}/{len(orig_track)} messages matched perfectly")
    
    if matches == len(orig_track):
        print("✅ Round-trip conversion is PERFECT!")
    else:
        print("❌ Round-trip conversion has issues")
    
    # Clean up
    try:
        os.unlink('test_original.mid')
        os.unlink('test_reconstructed.mid')
    except:
        pass

if __name__ == '__main__':
    test_roundtrip()
