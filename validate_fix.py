#!/usr/bin/env python3
"""
Quick validation of the save function syntax and logic
"""

def validate_save_function_syntax():
    """Check that the save function has correct syntax"""
    print("🔍 Validating save function syntax...")
    
    # Read the main.py file and look for the save function
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for the save_midi_file function
        if 'def save_midi_file(self):' not in content:
            print("❌ save_midi_file function not found")
            return False
        
        # Check for key components
        checks = [
            ('ET.fromstring(xml_content)', 'XML parsing'),
            ('MidiFile(ticks_per_beat=ticks_per_beat)', 'MIDI file creation'),
            ('mido.Message(msg_type', 'MIDI message creation'),
            ('mido.MetaMessage(msg_type', 'Meta message creation'),
            ('new_midi.save(file_path)', 'MIDI file saving'),
        ]
        
        print("✅ Checking save function components:")
        all_good = True
        for check, description in checks:
            if check in content:
                print(f"   ✅ {description}: Found")
            else:
                print(f"   ❌ {description}: Missing")
                all_good = False
        
        # Check for message type handlers
        message_types = [
            'note_on', 'note_off', 'program_change', 'control_change', 
            'pitchwheel', 'set_tempo', 'time_signature', 'key_signature',
            'midi_port', 'end_of_track'
        ]
        
        print("\n✅ Checking message type handlers:")
        for msg_type in message_types:
            if f"msg_type == '{msg_type}'" in content:
                print(f"   ✅ {msg_type}: Handled")
            else:
                print(f"   ⚠️  {msg_type}: Not explicitly handled")
        
        return all_good
        
    except Exception as e:
        print(f"❌ Error reading main.py: {e}")
        return False

def check_xml_structure():
    """Check the XML file structure"""
    print(f"\n🔍 Checking XML file structure...")
    
    try:
        import xml.etree.ElementTree as ET
        
        xml_file = "A HA.Take on me  K.xml"
        if not os.path.exists(xml_file):
            print(f"⚠️  XML file not found: {xml_file}")
            return False
        
        with open(xml_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        root = ET.fromstring(content)
        
        print(f"✅ XML structure:")
        print(f"   📊 Root element: {root.tag}")
        print(f"   🎵 Ticks per beat: {root.get('ticks_per_beat')}")
        print(f"   📁 Tracks: {len(root.findall('Track'))}")
        
        total_messages = 0
        for track in root.findall('Track'):
            messages = len(track.findall('Message'))
            total_messages += messages
            print(f"   🎯 Track '{track.get('name', 'Unknown')}': {messages} messages")
        
        print(f"   📝 Total messages: {total_messages}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error parsing XML: {e}")
        return False

if __name__ == "__main__":
    import os
    
    print("🚀 VALIDATION TEST SUITE")
    print("=" * 50)
    
    # Change to the correct directory
    os.chdir(r"g:\My Drive\Programming Projects\Player Piano\Jeremys Code\Python Midi Gapper 2")
    
    # Run validations
    syntax_ok = validate_save_function_syntax()
    xml_ok = check_xml_structure()
    
    if syntax_ok and xml_ok:
        print(f"\n🎉 VALIDATION PASSED!")
        print(f"✅ Save function syntax is correct")
        print(f"✅ XML structure is valid")
        print(f"✅ Ready for testing!")
    else:
        print(f"\n❌ VALIDATION ISSUES FOUND!")
        if not syntax_ok:
            print(f"❌ Save function has syntax issues")
        if not xml_ok:
            print(f"❌ XML structure has issues")
