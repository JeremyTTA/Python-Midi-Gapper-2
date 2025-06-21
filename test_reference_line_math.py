#!/usr/bin/env python3
"""
Simple test for 90% reference line position logic.
Tests the mathematical positioning without requiring the full GUI.
"""

def test_reference_line_positions():
    """Test reference line positioning at various scroll positions"""
    print("=== Testing 90% Reference Line Position ===")
    
    # Simulate typical viewport dimensions
    visible_height = 600  # pixels
    canvas_height = 3000  # total canvas height
    max_scroll = canvas_height - visible_height  # 2400
    
    print(f"Canvas height: {canvas_height}")
    print(f"Visible height: {visible_height}")
    print(f"Max scroll: {max_scroll}")
    
    # Test different scroll positions
    test_positions = [
        ("Top (0%)", 0.0),
        ("25% down", 0.25),
        ("Middle (50%)", 0.50),
        ("75% down", 0.75),
        ("Bottom (100%)", 1.0)
    ]
    
    print("\n=== Reference Line Positions at Different Scroll Points ===")
    
    for position_name, scroll_ratio in test_positions:
        scroll_y = scroll_ratio * max_scroll
        visible_top_y = scroll_y
        visible_bottom_y = scroll_y + visible_height
        
        # Calculate reference line positions for different ratios
        reference_67 = visible_top_y + (visible_height * 0.67)  # Original
        reference_85 = visible_top_y + (visible_height * 0.85)  # Previous
        reference_90 = visible_top_y + (visible_height * 0.90)  # Current
        reference_95 = visible_top_y + (visible_height * 0.95)  # Alternative
        
        print(f"\n--- {position_name} (scroll: {scroll_y:.0f}) ---")
        print(f"  Visible area: {visible_top_y:.0f} - {visible_bottom_y:.0f}")
        print(f"  67% reference: {reference_67:.0f} ({reference_67 - visible_top_y:.0f} from top, {visible_bottom_y - reference_67:.0f} from bottom)")
        print(f"  85% reference: {reference_85:.0f} ({reference_85 - visible_top_y:.0f} from top, {visible_bottom_y - reference_85:.0f} from bottom)")
        print(f"  90% reference: {reference_90:.0f} ({reference_90 - visible_top_y:.0f} from top, {visible_bottom_y - reference_90:.0f} from bottom)")
        print(f"  95% reference: {reference_95:.0f} ({reference_95 - visible_top_y:.0f} from top, {visible_bottom_y - reference_95:.0f} from bottom)")

def test_highlighting_timing():
    """Test when notes would be highlighted with different reference positions"""
    print("\n=== Highlighting Timing Analysis ===")
    
    # Simulate some notes
    pixels_per_second = 100  # 100 pixels per second
    visible_height = 600
    scroll_y = 1000  # middle scroll position
    highlight_tolerance = 20
    
    # Sample notes at different times
    notes = [
        {"name": "Note A", "start_time": 8.0, "end_time": 8.5},
        {"name": "Note B", "start_time": 9.0, "end_time": 9.3},
        {"name": "Note C", "start_time": 10.0, "end_time": 10.8},
        {"name": "Note D", "start_time": 11.0, "end_time": 11.2},
        {"name": "Note E", "start_time": 12.0, "end_time": 12.4},
    ]
    
    visible_top_y = scroll_y
    visible_bottom_y = scroll_y + visible_height
    
    # Test with 90% reference line
    reference_line_y = visible_top_y + (visible_height * 0.90)
    reference_time = reference_line_y / pixels_per_second
    
    print(f"Scroll position: {scroll_y}")
    print(f"Visible area: {visible_top_y} - {visible_bottom_y}")
    print(f"90% reference line at Y: {reference_line_y}")
    print(f"Reference line time: {reference_time:.2f}s")
    print(f"Highlight tolerance: ±{highlight_tolerance} pixels")
    
    print("\nNote highlighting analysis:")
    for note in notes:
        rect_top_y = note['start_time'] * pixels_per_second
        rect_bottom_y = note['end_time'] * pixels_per_second
        
        # Check if note would be highlighted
        is_highlighted = (rect_top_y <= reference_line_y + highlight_tolerance and 
                         rect_bottom_y >= reference_line_y - highlight_tolerance)
        
        # Calculate distances
        distance_to_ref = abs((rect_top_y + rect_bottom_y) / 2 - reference_line_y)
        
        status = "HIGHLIGHTED" if is_highlighted else "not highlighted"
        print(f"  {note['name']}: {note['start_time']:.1f}-{note['end_time']:.1f}s "
              f"(Y: {rect_top_y:.0f}-{rect_bottom_y:.0f}) - {status}")
        print(f"    Distance to ref line: {distance_to_ref:.1f} pixels")

def compare_timing_feel():
    """Compare the 'feel' of different reference line positions"""
    print("\n=== Timing Feel Comparison ===")
    
    visible_height = 600
    
    positions = [
        ("67% (Original)", 0.67, "Notes highlighted when they're 1/3 down from top"),
        ("85% (Previous)", 0.85, "Notes highlighted when they're near bottom"),
        ("90% (Current)", 0.90, "Notes highlighted when they're very close to bottom"),
        ("95% (Alternative)", 0.95, "Notes highlighted right before they disappear")
    ]
    
    for name, ratio, description in positions:
        pixels_from_top = visible_height * ratio
        pixels_from_bottom = visible_height * (1 - ratio)
        
        print(f"\n{name}:")
        print(f"  Position: {pixels_from_top:.0f} pixels from top, {pixels_from_bottom:.0f} pixels from bottom")
        print(f"  Feel: {description}")
        
        # Calculate 'lead time' - how much advance notice before note reaches bottom
        lead_time_pixels = pixels_from_bottom
        lead_time_seconds = lead_time_pixels / 100  # assuming 100 pixels per second
        print(f"  Lead time: {lead_time_seconds:.1f}s before note reaches bottom")

if __name__ == "__main__":
    print("Reference Line Position Analysis")
    print("=" * 50)
    
    test_reference_line_positions()
    test_highlighting_timing()
    compare_timing_feel()
    
    print("\n=== Summary ===")
    print("The 90% reference line position provides:")
    print("- 60 pixels (0.6s at 100px/s) lead time before notes reach bottom")
    print("- More natural highlighting that occurs closer to when notes are about to disappear")
    print("- Consistent behavior across all scroll positions")
    print("\nIf highlighting still feels too early, try 95% (30 pixels/0.3s lead time)")
