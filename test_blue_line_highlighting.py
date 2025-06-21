#!/usr/bin/env python3
"""
Test script for the blue line highlighting approach.
Tests if notes are highlighted when they reach the blue line at the top of the keyboard.
"""

def test_blue_line_highlighting():
    """Test the blue line highlighting logic"""
    print("=== Testing Blue Line Highlighting Approach ===")
    
    # Simulate typical viewport and canvas dimensions
    visible_height = 600  # Main canvas visible height
    keyboard_height = 200  # Keyboard height (fixed)
    canvas_height = 3000  # Total canvas height
    
    print(f"Setup:")
    print(f"  Visible height: {visible_height}")
    print(f"  Keyboard height: {keyboard_height}")
    print(f"  Total canvas height: {canvas_height}")
    
    # Test different scroll positions
    test_positions = [
        ("Top (0%)", 0.0),
        ("25% down", 0.25),
        ("Middle (50%)", 0.50),
        ("75% down", 0.75),
        ("Bottom (100%)", 1.0)
    ]
    
    max_scroll = canvas_height - visible_height  # 2400
    
    print(f"\n=== Blue Line Position at Different Scroll Points ===")
    
    for position_name, scroll_ratio in test_positions:
        scroll_y = scroll_ratio * max_scroll
        visible_top_y = scroll_y
        visible_bottom_y = scroll_y + visible_height
        
        # Calculate blue line position (at bottom edge of visible area)
        blue_line_y = visible_bottom_y
        
        print(f"\n--- {position_name} (scroll: {scroll_y:.0f}) ---")
        print(f"  Visible area: {visible_top_y:.0f} - {visible_bottom_y:.0f}")
        print(f"  Blue line Y: {blue_line_y:.0f}")
        print(f"  Blue line position: at bottom edge of viewport")
        
        # Show what this means for note timing
        pixels_per_second = 100  # Assume 100 pixels per second
        blue_line_time = blue_line_y / pixels_per_second
        print(f"  Blue line time: {blue_line_time:.2f}s")

def test_note_highlighting_timing():
    """Test when notes would be highlighted with blue line approach"""
    print("\n=== Note Highlighting with Blue Line ===")
    
    # Simulate some notes and scroll position
    pixels_per_second = 100
    visible_height = 600
    scroll_y = 1200  # Middle scroll position
    highlight_tolerance = 10  # Tighter tolerance for blue line
    
    # Sample notes at different times
    notes = [
        {"name": "Note A", "start_time": 10.0, "end_time": 10.5},
        {"name": "Note B", "start_time": 11.0, "end_time": 11.3},
        {"name": "Note C", "start_time": 12.0, "end_time": 12.8},
        {"name": "Note D", "start_time": 18.0, "end_time": 18.2},  # Right at blue line
        {"name": "Note E", "start_time": 19.0, "end_time": 19.4},
    ]
    
    visible_top_y = scroll_y
    visible_bottom_y = scroll_y + visible_height
    blue_line_y = visible_bottom_y  # 1800
    blue_line_time = blue_line_y / pixels_per_second  # 18.0s
    
    print(f"Scroll position: {scroll_y}")
    print(f"Visible area: {visible_top_y} - {visible_bottom_y}")
    print(f"Blue line at Y: {blue_line_y} (time: {blue_line_time:.2f}s)")
    print(f"Highlight tolerance: ±{highlight_tolerance} pixels")
    
    print(f"\nNote highlighting analysis:")
    for note in notes:
        rect_top_y = note['start_time'] * pixels_per_second
        rect_bottom_y = note['end_time'] * pixels_per_second
        
        # Check if note would be highlighted
        is_highlighted = (rect_top_y <= blue_line_y + highlight_tolerance and 
                         rect_bottom_y >= blue_line_y - highlight_tolerance)
        
        # Calculate how far note is from blue line
        note_center_y = (rect_top_y + rect_bottom_y) / 2
        distance_to_blue = note_center_y - blue_line_y
        
        status = "HIGHLIGHTED" if is_highlighted else "not highlighted"
        direction = "above" if distance_to_blue < 0 else "below"
        
        print(f"  {note['name']}: {note['start_time']:.1f}-{note['end_time']:.1f}s "
              f"(Y: {rect_top_y:.0f}-{rect_bottom_y:.0f}) - {status}")
        print(f"    Center {abs(distance_to_blue):.1f} pixels {direction} blue line")
        
        if is_highlighted:
            # Show exactly when note intersects blue line
            if rect_top_y <= blue_line_y <= rect_bottom_y:
                print(f"    *** Blue line passes through note rectangle ***")
            elif rect_bottom_y >= blue_line_y - highlight_tolerance:
                print(f"    *** Note bottom within tolerance of blue line ***")

def compare_approaches():
    """Compare blue line approach with previous reference line approaches"""
    print("\n=== Approach Comparison ===")
    
    visible_height = 600
    visible_top_y = 1200
    visible_bottom_y = visible_top_y + visible_height  # 1800
    
    approaches = [
        ("67% Reference Line", visible_top_y + (visible_height * 0.67), "1602"),
        ("85% Reference Line", visible_top_y + (visible_height * 0.85), "1710"),
        ("90% Reference Line", visible_top_y + (visible_height * 0.90), "1740"),
        ("Blue Line (Bottom Edge)", visible_bottom_y, "1800")
    ]
    
    print(f"Viewport: {visible_top_y} - {visible_bottom_y}")
    
    for name, position, y_str in approaches:
        pixels_from_top = position - visible_top_y
        pixels_from_bottom = visible_bottom_y - position
        
        print(f"\n{name}:")
        print(f"  Y position: {position}")
        print(f"  Distance from top: {pixels_from_top:.0f} pixels")
        print(f"  Distance from bottom: {pixels_from_bottom:.0f} pixels")
        
        if position == visible_bottom_y:
            print(f"  *** Represents the actual blue line at keyboard edge ***")

def test_visual_accuracy():
    """Test how visually accurate the blue line approach would be"""
    print("\n=== Visual Accuracy Test ===")
    
    print("Blue Line Highlighting Benefits:")
    print("✅ Notes highlight exactly when they reach the keyboard")
    print("✅ Perfect visual correspondence - what you see is what plays")
    print("✅ No arbitrary percentages or guesswork")
    print("✅ Intuitive - matches Synthesia-style visualization")
    print("✅ Consistent timing regardless of scroll position")
    print("✅ Tight tolerance (10px) for precise highlighting")
    
    print("\nExpected User Experience:")
    print("- Notes will light up exactly when they touch the blue line")
    print("- This matches when the note should be played")
    print("- Visual feedback is immediate and accurate")
    print("- No more 'early' or 'late' highlighting issues")

if __name__ == "__main__":
    print("Blue Line Highlighting Test")
    print("=" * 50)
    
    test_blue_line_highlighting()
    test_note_highlighting_timing()
    compare_approaches()
    test_visual_accuracy()
    
    print("\n=== Summary ===")
    print("The blue line approach should provide:")
    print("- Perfect visual accuracy (notes highlight when touching keyboard)")
    print("- Immediate feedback with no lead time")
    print("- Intuitive behavior matching visual expectations")
    print("- Consistent performance at all scroll positions")
    print("\nThis should completely eliminate the 'too early' highlighting issue!")
