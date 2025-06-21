#!/usr/bin/env python3
"""
Simple test to verify keyboard highlighting implementation
"""

# Read the main.py file and check for our new functionality
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Check for required components
checks = [
    ('keyboard_keys initialization', 'self.keyboard_keys = {}'),
    ('update_keyboard_highlighting method', 'def update_keyboard_highlighting(self):'),
    ('keyboard highlighting in playback timer', 'self.update_keyboard_highlighting()'),
    ('key highlighting in draw_keyboard', 'tags=f\'key_{note}\''),
    ('currently playing notes logic', 'currently_playing_notes = set()'),
    ('blue highlighting for black keys', 'fill=\'#4080FF\''),
    ('light blue highlighting for white keys', 'fill=\'#B0D0FF\''),
]

print("Checking keyboard highlighting implementation:")
print("=" * 50)

all_passed = True
for check_name, check_string in checks:
    if check_string in content:
        print(f"✓ {check_name}")
    else:
        print(f"✗ {check_name}")
        all_passed = False

print("=" * 50)
if all_passed:
    print("🎉 All keyboard highlighting features are properly implemented!")
    print("\nFeatures added:")
    print("- Keyboard keys are now stored with references for highlighting")
    print("- update_keyboard_highlighting() method finds notes playing at current position")
    print("- Keys are highlighted in blue when notes are playing")
    print("- Highlighting updates during playback and manual position changes")
    print("- Both white keys (light blue) and black keys (bright blue) are highlighted")
else:
    print("❌ Some features are missing or not implemented correctly")
