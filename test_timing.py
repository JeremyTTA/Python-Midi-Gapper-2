#!/usr/bin/env python3
"""
Test to verify timing is preserved correctly
"""

import mido
import xml.etree.ElementTree as ET
from mido import MidiFile, MidiTrack

def test_timing_preservation():
    """Test that delta times are preserved correctly"""
    print("=== Testing Timing Preservation ===")
    
    # Create a test MIDI with specific timing
    midi = MidiFile()
    track = MidiTrack()
    
    # Add messages with specific delta times
    track.append(mido.MetaMessage('set_tempo', tempo=500000, time=0))      # time=0
    track.append(mido.Message('note_on', channel=0, note=60, velocity=64, time=384))   # time=384
    track.append(mido.Message('note_on', channel=0, note=64, velocity=64, time=0))     # time=0 (simultaneous)
    track.append(mido.Message('note_off', channel=0, note=60, velocity=64, time=96))   # time=96
    track.append(mido.Message('note_off', channel=0, note=64, velocity=64, time=0))    # time=0 (simultaneous)
    track.append(mido.MetaMessage('end_of_track', time=0))                # time=0
    
    midi.tracks.append(track)
    
    print("Original MIDI timing:")
    for i, msg in enumerate(track):
        print(f"  {i}: {msg.type} time={msg.time}")
    
    # Convert to XML (simulate the app's XML generation)
    root = ET.Element('MidiFile', ticks_per_beat=str(midi.ticks_per_beat))
    tr_elem = ET.SubElement(root, 'Track', name='Track_0')
    
    for msg in track:
        attrs = msg.dict()
        msg_elem = ET.SubElement(tr_elem, 'Message', type=msg.type, time=str(msg.time))
        for attr, value in attrs.items():
            if attr not in ('type', 'time'):
                msg_elem.set(attr, str(value))
    
    xml_content = ET.tostring(root, encoding='unicode')
    print(f"\nGenerated XML snippet:")
    # Show just the time attributes
    for line in xml_content.split('\n'):
        if 'time=' in line:
            print(f"  {line.strip()}")
    
    # Parse XML back to MIDI (simulate the fixed save function)
    root = ET.fromstring(xml_content)
    reconstructed_midi = MidiFile(ticks_per_beat=int(root.get('ticks_per_beat', 480)))
    
    for track_elem in root.findall('Track'):
        new_track = MidiTrack()
        new_track.name = track_elem.get('name', '')
        
        # Process messages in XML order (no sorting!)
        for msg_elem in track_elem.findall('Message'):
            msg_type = msg_elem.get('type')
            delta_time = int(msg_elem.get('time', 0))
            
            # Build kwargs
            kwargs = {}
            for key, value in msg_elem.attrib.items():
                if key not in ('type', 'time'):
                    if isinstance(value, str) and value.lstrip('-').isdigit():
                        kwargs[key] = int(value)
                    else:
                        kwargs[key] = value
            
            # Create message
            is_meta = msg_type in ['set_tempo', 'end_of_track']
            if is_meta:
                msg = mido.MetaMessage(msg_type, time=delta_time, **kwargs)
            else:
                msg = mido.Message(msg_type, time=delta_time, **kwargs)
            
            new_track.append(msg)
        
        reconstructed_midi.tracks.append(new_track)
    
    print("\nReconstructed MIDI timing:")
    recon_track = reconstructed_midi.tracks[0]
    for i, msg in enumerate(recon_track):
        print(f"  {i}: {msg.type} time={msg.time}")
    
    # Compare timing
    print("\nTiming comparison:")
    orig_times = [msg.time for msg in track]
    recon_times = [msg.time for msg in recon_track]
    
    print(f"Original times:     {orig_times}")
    print(f"Reconstructed times: {recon_times}")
    
    if orig_times == recon_times:
        print("✅ Timing preserved perfectly!")
    else:
        print("❌ Timing mismatch!")
        for i, (orig, recon) in enumerate(zip(orig_times, recon_times)):
            if orig != recon:
                print(f"  Message {i}: {orig} → {recon}")
    
    # Test playback timing
    print("\nPlayback timing test:")
    print("Original cumulative times:", end=" ")
    cum_time = 0
    for msg in track:
        cum_time += msg.time
        print(cum_time, end=" ")
    print()
    
    print("Reconstructed cumulative times:", end=" ")
    cum_time = 0
    for msg in recon_track:
        cum_time += msg.time
        print(cum_time, end=" ")
    print()

if __name__ == '__main__':
    test_timing_preservation()
