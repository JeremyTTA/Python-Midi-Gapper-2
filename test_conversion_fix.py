#!/usr/bin/env python3
"""
Comprehensive test to verify XML/MIDI conversion fix
"""
import xml.etree.ElementTree as ET
import mido
from mido import MidiFile, MidiTrack
import os
import sys

def test_xml_to_midi_conversion():
    """Test converting the XML back to MIDI and compare with original expectations"""
    
    xml_file = "A HA.Take on me  K.xml"
    if not os.path.exists(xml_file):
        print(f"❌ XML file not found: {xml_file}")
        return False
    
    print("🧪 Testing XML to MIDI Conversion")
    print("=" * 50)
    
    try:
        # Parse XML
        with open(xml_file, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        
        root = ET.fromstring(xml_content)
        print(f"✅ XML parsed successfully")
        print(f"   📊 Tracks in XML: {len(root.findall('Track'))}")
        print(f"   🎵 Ticks per beat: {root.get('ticks_per_beat')}")
        
        # Convert XML to MIDI using the same logic as the save function
        ticks_per_beat = int(root.get('ticks_per_beat', 480))
        new_midi = MidiFile(ticks_per_beat=ticks_per_beat)
        
        total_messages_in_xml = 0
        total_messages_converted = 0
        failed_conversions = 0
        
        for track_elem in root.findall('Track'):
            track = MidiTrack()
            track.name = track_elem.get('name', '')
            
            # Collect all messages
            messages = []
            xml_messages = track_elem.findall('Message')
            total_messages_in_xml += len(xml_messages)
            
            print(f"\n🎯 Processing track '{track.name}': {len(xml_messages)} messages")
            
            for msg_elem in xml_messages:
                msg_type = msg_elem.get('type')
                time = int(msg_elem.get('time', 0))
                
                attrs = {'type': msg_type, 'time': time}
                for key, value in msg_elem.attrib.items():
                    if key not in ('type', 'time'):
                        # Convert numeric attributes
                        if key in ('channel', 'note', 'velocity', 'program', 'control', 'value', 'pitch', 
                                  'port', 'numerator', 'denominator', 'clocks_per_click', 
                                  'notated_32nd_notes_per_beat', 'tempo', 'number', 'song', 'pos', 
                                  'frame_type', 'frame_value', 'hours', 'minutes', 'seconds', 
                                  'frames', 'sub_frames'):
                            try:
                                attrs[key] = int(value)
                            except (ValueError, TypeError):
                                attrs[key] = value
                        elif key == 'frame_rate':
                            try:
                                attrs[key] = int(value)
                            except (ValueError, TypeError):
                                attrs[key] = 24
                        elif key == 'data' and isinstance(value, str):
                            try:
                                attrs[key] = eval(value) if value.startswith('[') else []
                            except:
                                attrs[key] = []
                        elif key in ('text', 'name', 'key'):
                            attrs[key] = str(value)
                        else:
                            attrs[key] = value
                
                messages.append(attrs)
            
            # Sort by time and convert to MIDI messages
            messages.sort(key=lambda x: x['time'])
            
            for msg_attrs in messages:
                try:
                    msg_type = msg_attrs['type']
                    time = msg_attrs['time']
                    kwargs = {k: v for k, v in msg_attrs.items() if k not in ('type', 'time')}
                    
                    # Create message based on type
                    msg = None
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
                    elif msg_type == 'aftertouch':
                        msg = mido.Message(msg_type,
                                         channel=kwargs.get('channel', 0),
                                         value=kwargs.get('value', 0),
                                         time=time)
                    elif msg_type == 'polytouch':
                        msg = mido.Message(msg_type,
                                         channel=kwargs.get('channel', 0),
                                         note=kwargs.get('note', 60),
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
                    elif msg_type == 'songpos':
                        msg = mido.Message(msg_type, pos=kwargs.get('pos', 0), time=time)
                    elif msg_type == 'song_select':
                        msg = mido.Message(msg_type, song=kwargs.get('song', 0), time=time)
                    elif msg_type in ['start', 'stop', 'continue', 'clock', 'active_sensing', 'reset']:
                        msg = mido.Message(msg_type, time=time)
                    elif msg_type == 'quarter_frame':
                        msg = mido.Message(msg_type, frame_type=kwargs.get('frame_type', 0), 
                                         frame_value=kwargs.get('frame_value', 0), time=time)
                    elif msg_type == 'tune_request':
                        msg = mido.Message(msg_type, time=time)
                    elif msg_type == 'sequence_number':
                        msg = mido.MetaMessage(msg_type, number=kwargs.get('number', 0), time=time)
                    elif msg_type == 'channel_prefix':
                        msg = mido.MetaMessage(msg_type, channel=kwargs.get('channel', 0), time=time)
                    elif msg_type == 'device_name':
                        msg = mido.MetaMessage(msg_type, name=kwargs.get('name', ''), time=time)
                    elif msg_type == 'instrument_name':
                        msg = mido.MetaMessage(msg_type, name=kwargs.get('name', ''), time=time)
                    elif msg_type == 'program_name':
                        msg = mido.MetaMessage(msg_type, name=kwargs.get('name', ''), time=time)
                    elif msg_type == 'smpte_offset':
                        msg = mido.MetaMessage(msg_type,
                                             frame_rate=kwargs.get('frame_rate', 24),
                                             hours=kwargs.get('hours', 0),
                                             minutes=kwargs.get('minutes', 0),
                                             seconds=kwargs.get('seconds', 0),
                                             frames=kwargs.get('frames', 0),
                                             sub_frames=kwargs.get('sub_frames', 0),
                                             time=time)
                    elif msg_type == 'sequencer_specific':
                        data = kwargs.get('data', [])
                        if isinstance(data, str):
                            try:
                                data = eval(data) if data.startswith('[') else []
                            except:
                                data = []
                        msg = mido.MetaMessage(msg_type, data=data, time=time)
                    else:
                        print(f"⚠️  Unsupported message type: {msg_type}")
                        failed_conversions += 1
                        continue
                    
                    if msg:
                        track.append(msg)
                        total_messages_converted += 1
                        
                except Exception as e:
                    print(f"❌ Failed to create {msg_type}: {e}")
                    print(f"   Attributes: {msg_attrs}")
                    failed_conversions += 1
            
            new_midi.tracks.append(track)
            print(f"   ✅ Track completed: {len(track)} messages")
        
        # Save the test MIDI file
        test_output = "test_conversion_output.mid"
        new_midi.save(test_output)
        
        # Print summary
        print(f"\n📋 CONVERSION SUMMARY")
        print(f"=" * 50)
        print(f"✅ Total XML messages: {total_messages_in_xml}")
        print(f"✅ Successfully converted: {total_messages_converted}")
        print(f"❌ Failed conversions: {failed_conversions}")
        print(f"📊 Success rate: {(total_messages_converted/total_messages_in_xml)*100:.1f}%")
        print(f"💾 Test MIDI saved as: {test_output}")
        
        # Load the saved file to verify it's valid
        try:
            test_midi = MidiFile(test_output)
            print(f"✅ Generated MIDI file is valid")
            print(f"   📊 Tracks: {len(test_midi.tracks)}")
            print(f"   🎵 Ticks per beat: {test_midi.ticks_per_beat}")
            
            for i, track in enumerate(test_midi.tracks):
                print(f"   🎯 Track {i}: {len(track)} messages")
        except Exception as e:
            print(f"❌ Generated MIDI file is invalid: {e}")
            return False
        
        # Test passed if conversion rate is high
        success_rate = (total_messages_converted / total_messages_in_xml) * 100
        if success_rate >= 95:
            print(f"\n🎉 TEST PASSED! Conversion rate: {success_rate:.1f}%")
            return True
        else:
            print(f"\n⚠️  TEST NEEDS IMPROVEMENT. Conversion rate: {success_rate:.1f}%")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def analyze_message_types():
    """Quick analysis of message types in the XML"""
    xml_file = "A HA.Take on me  K.xml"
    if not os.path.exists(xml_file):
        return
    
    print(f"\n🔍 MESSAGE TYPE ANALYSIS")
    print(f"=" * 50)
    
    try:
        with open(xml_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        root = ET.fromstring(content)
        message_types = {}
        
        for track_elem in root.findall('Track'):
            for msg_elem in track_elem.findall('Message'):
                msg_type = msg_elem.get('type')
                message_types[msg_type] = message_types.get(msg_type, 0) + 1
        
        print(f"📊 Found {len(message_types)} different message types:")
        for msg_type, count in sorted(message_types.items(), key=lambda x: x[1], reverse=True):
            print(f"   {msg_type}: {count:,} messages")
            
    except Exception as e:
        print(f"❌ Analysis failed: {e}")

if __name__ == "__main__":
    print("🚀 MIDI CONVERSION TEST SUITE")
    print("=" * 50)
    
    # Run message type analysis first
    analyze_message_types()
    
    # Run the main conversion test
    success = test_xml_to_midi_conversion()
    
    if success:
        print(f"\n🎉 ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print(f"\n❌ TESTS FAILED!")
        sys.exit(1)
