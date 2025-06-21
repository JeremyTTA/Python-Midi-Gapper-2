#!/usr/bin/env python3
"""
Test script for the 90% reference line adjustment.
Tests highlighting accuracy at various scroll positions with the new reference line position.
"""

import sys
import json
import time
from main import MidiPlayer

def test_reference_line_position():
    """Test highlighting timing with 90% reference line position"""
    print("=== Testing 90% Reference Line Position ===")
    
    # Load configuration
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except:
        print("Error: Could not load config.json")
        return
    
    # Initialize player
    try:
        player = MidiPlayer()
        
        # Simulate loading a MIDI file
        midi_file = config.get('midi_file', 'A HA.Take on me  K.xml')
        if not player.load_midi_file(midi_file):
            print(f"Error: Could not load MIDI file: {midi_file}")
            return
            
        print(f"Loaded MIDI file: {midi_file}")
        print(f"Total duration: {player.total_duration:.2f} seconds")
        
        # Test highlighting at different scroll positions
        test_positions = [
            ("Top (0%)", 0.0),
            ("25% down", 0.25),
            ("Middle (50%)", 0.50),
            ("75% down", 0.75),
            ("Bottom (100%)", 1.0)
        ]
        
        print("\n=== Testing Reference Line at Different Scroll Positions ===")
        
        for position_name, scroll_ratio in test_positions:
            print(f"\n--- {position_name} ---")
            
            # Calculate scroll position
            max_scroll = max(0, player.canvas_height - player.visible_height)
            scroll_y = scroll_ratio * max_scroll
            player.scroll_y = scroll_y
            
            # Calculate visible area
            visible_top_y = scroll_y
            visible_bottom_y = scroll_y + player.visible_height
            visible_height = player.visible_height
            
            # Calculate reference line position (90% from top)
            reference_line_y = visible_top_y + (visible_height * 0.90)
            
            print(f"  Scroll Y: {scroll_y:.1f}")
            print(f"  Visible area: {visible_top_y:.1f} - {visible_bottom_y:.1f}")
            print(f"  Reference line Y: {reference_line_y:.1f}")
            print(f"  Reference line position: {reference_line_y - visible_top_y:.1f} pixels from top")
            print(f"  Reference line position: {visible_bottom_y - reference_line_y:.1f} pixels from bottom")
            
            # Test what notes would be highlighted at this position
            highlight_tolerance = 20
            highlighted_notes = []
            
            for track_idx, track in enumerate(player.tracks):
                for note in track['notes']:
                    # Calculate note rectangle position
                    rect_top_y = note['start_time'] * player.pixels_per_second
                    rect_bottom_y = note['end_time'] * player.pixels_per_second
                    
                    # Check if note intersects with reference line
                    if (rect_top_y <= reference_line_y + highlight_tolerance and 
                        rect_bottom_y >= reference_line_y - highlight_tolerance):
                        highlighted_notes.append({
                            'track': track_idx,
                            'note': note['note'],
                            'start_time': note['start_time'],
                            'end_time': note['end_time'],
                            'rect_top': rect_top_y,
                            'rect_bottom': rect_bottom_y
                        })
            
            print(f"  Notes highlighted: {len(highlighted_notes)}")
            if highlighted_notes:
                # Show timing of first few highlighted notes
                for i, note in enumerate(highlighted_notes[:3]):
                    print(f"    Note {i+1}: {note['note']} at {note['start_time']:.2f}s "
                          f"(rect: {note['rect_top']:.1f}-{note['rect_bottom']:.1f})")
            
            # Calculate what time the reference line corresponds to
            reference_time = reference_line_y / player.pixels_per_second
            print(f"  Reference line time: {reference_time:.2f}s")
            
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()

def compare_reference_positions():
    """Compare highlighting behavior at different reference line positions"""
    print("\n=== Comparing Reference Line Positions ===")
    
    positions = [
        ("67% from top (original)", 0.67),
        ("85% from top (previous)", 0.85),
        ("90% from top (current)", 0.90),
        ("95% from top (alternative)", 0.95)
    ]
    
    # Simulate a visible viewport
    visible_height = 600  # pixels
    visible_top_y = 1000  # example scroll position
    
    print(f"Viewport: {visible_top_y} - {visible_top_y + visible_height} (height: {visible_height})")
    
    for name, ratio in positions:
        reference_line_y = visible_top_y + (visible_height * ratio)
        pixels_from_top = reference_line_y - visible_top_y
        pixels_from_bottom = (visible_top_y + visible_height) - reference_line_y
        
        print(f"\n{name}:")
        print(f"  Reference line Y: {reference_line_y:.1f}")
        print(f"  Distance from top: {pixels_from_top:.1f} pixels ({pixels_from_top/visible_height*100:.1f}%)")
        print(f"  Distance from bottom: {pixels_from_bottom:.1f} pixels ({pixels_from_bottom/visible_height*100:.1f}%)")

if __name__ == "__main__":
    print("Testing 90% Reference Line Position")
    print("=" * 50)
    
    test_reference_line_position()
    compare_reference_positions()
    
    print("\n=== Test Complete ===")
    print("The reference line has been moved to 90% from the top (10% from bottom).")
    print("This should make highlighting occur later, feeling more natural.")
    print("If highlighting is still too early, consider adjusting to 95% from top.")
