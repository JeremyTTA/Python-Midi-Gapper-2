#!/usr/bin/env python3
"""
Focused diagnostic to identify XML/MIDI conversion issues
"""
import xml.etree.ElementTree as ET
import os

def analyze_xml_message_types():
    """Analyze the XML file to see what message types exist"""
    xml_file = "A HA.Take on me  K.xml"
    if not os.path.exists(xml_file):
        print(f"XML file not found: {xml_file}")
        return
    
    try:
        with open(xml_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        root = ET.fromstring(content)
        print(f"XML Analysis:")
        print(f"Tracks: {len(root.findall('Track'))}")
        print(f"Ticks per beat: {root.get('ticks_per_beat')}")
        
        # Count message types
        message_types = {}
        total_messages = 0
        
        for track_elem in root.findall('Track'):
            track_name = track_elem.get('name', 'Unknown')
            messages = track_elem.findall('Message')
            print(f"\nTrack '{track_name}': {len(messages)} messages")
            
            for msg_elem in messages:
                msg_type = msg_elem.get('type')
                message_types[msg_type] = message_types.get(msg_type, 0) + 1
                total_messages += 1
        
        print(f"\nTotal messages: {total_messages}")
        print(f"\nMessage type breakdown:")
        for msg_type, count in sorted(message_types.items()):
            print(f"  {msg_type}: {count}")
        
        # Check which message types are NOT handled by the save function
        handled_types = {
            'note_on', 'note_off', 'program_change', 'control_change', 'pitchwheel',
            'aftertouch', 'polytouch', 'set_tempo', 'time_signature', 'key_signature',
            'track_name', 'text', 'copyright', 'marker', 'cue_marker', 'lyrics',
            'midi_port', 'end_of_track', 'sysex', 'songpos', 'song_select',
            'start', 'stop', 'continue', 'clock', 'active_sensing', 'reset',
            'quarter_frame', 'tune_request', 'sequence_number', 'channel_prefix',
            'device_name', 'instrument_name', 'program_name', 'smpte_offset',
            'sequencer_specific'
        }
        
        unhandled_types = set(message_types.keys()) - handled_types
        if unhandled_types:
            print(f"\n*** UNHANDLED MESSAGE TYPES ***")
            for msg_type in sorted(unhandled_types):
                print(f"  {msg_type}: {message_types[msg_type]} messages")
        else:
            print(f"\nAll message types are handled by the save function!")
        
        # Check for potential attribute issues
        print(f"\nSample message attributes:")
        for track_elem in root.findall('Track')[:1]:  # Just first track
            for msg_elem in track_elem.findall('Message')[:10]:  # First 10 messages
                msg_type = msg_elem.get('type')
                attrs = dict(msg_elem.attrib)
                print(f"  {msg_type}: {attrs}")
        
    except Exception as e:
        print(f"Error analyzing XML: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_xml_message_types()
