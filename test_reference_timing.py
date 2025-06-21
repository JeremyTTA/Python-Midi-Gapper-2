#!/usr/bin/env python3
"""
Test different reference line positions to find the optimal highlighting timing.
This helps fine-tune when notes should be highlighted.
"""

def analyze_highlighting_timing():
    """Analyze the timing of highlighting vs user expectation"""
    print("Highlighting Timing Analysis")
    print("=" * 35)
    
    print("PROBLEM: 'The highlights are still happening too early'")
    print()
    print("This means the reference line is positioned too high (early) in the visible area.")
    print("We need to move it lower (later in time) to match when notes should actually light up.")
    print()

def test_different_reference_positions():
    """Test different reference line positions"""
    print("Testing Different Reference Line Positions")
    print("=" * 50)
    
    # Test various positions from top of visible area
    positions = [
        {"percent": 0.50, "desc": "50% from top (center)", "timing": "Very early"},
        {"percent": 0.67, "desc": "67% from top (previous)", "timing": "Early"},
        {"percent": 0.75, "desc": "75% from top", "timing": "Slightly early"},
        {"percent": 0.80, "desc": "80% from top", "timing": "Getting closer"},
        {"percent": 0.85, "desc": "85% from top (new)", "timing": "Should be better"},
        {"percent": 0.90, "desc": "90% from top", "timing": "Might be right"},
        {"percent": 0.95, "desc": "95% from top", "timing": "Very close to bottom"},
    ]
    
    visible_height = 400.0  # Example visible height
    visible_top_y = 600.0   # Example top position
    
    print("Simulating different reference line positions:")
    print(f"Visible area: {visible_top_y:.0f} to {visible_top_y + visible_height:.0f}")
    print()
    
    for pos in positions:
        percent = pos["percent"]
        desc = pos["desc"]
        timing = pos["timing"]
        
        reference_y = visible_top_y + (visible_height * percent)
        distance_from_bottom = visible_height * (1.0 - percent)
        
        print(f"{desc}:")
        print(f"  Reference line Y: {reference_y:.0f}")
        print(f"  Distance from bottom: {distance_from_bottom:.0f} pixels")
        print(f"  Expected timing: {timing}")
        print()

def explain_coordinate_system_timing():
    """Explain how coordinate system affects timing"""
    print("Coordinate System and Timing")
    print("=" * 35)
    
    print("MIDI TIME FLOW:")
    print("- Time 0 (start) → Bottom of canvas (high Y values)")
    print("- Time max (end) → Top of canvas (low Y values)")
    print()
    
    print("VISUAL FLOW:")
    print("- Notes flow from top to bottom during playback")
    print("- Earlier times appear lower on screen")
    print("- Later times appear higher on screen")
    print()
    
    print("HIGHLIGHTING EXPECTATION:")
    print("- Notes should light up when they 'reach' the reference line")
    print("- Reference line represents 'current playback position'")
    print("- Too high = highlights too early (notes not yet playing)")
    print("- Too low = highlights too late (notes already finished)")
    print()
    
    print("OPTIMAL POSITION:")
    print("- Should match where user expects 'now' to be")
    print("- Traditional piano rolls use bottom ~10-20% of screen")
    print("- This gives visual 'lead time' to see upcoming notes")

def suggest_fine_tuning_approach():
    """Suggest approach for fine-tuning the position"""
    print("Fine-Tuning Approach")
    print("=" * 25)
    
    print("TESTING STRATEGY:")
    print("1. Try 85% from top (current change)")
    print("2. If still too early → try 90% or 95%")
    print("3. If now too late → try 80% or 75%")
    print("4. Find the sweet spot that feels natural")
    print()
    
    print("EVALUATION CRITERIA:")
    print("- Notes light up when they sound natural")
    print("- Provides useful 'preview' of upcoming notes")
    print("- Feels responsive and immediate")
    print("- Works well at different zoom levels")
    print()
    
    print("QUICK ADJUSTMENT METHOD:")
    print("To make highlighting later (if still too early):")
    print("  reference_line_y = visible_top_y + (visible_height * 0.90)  # 90%")
    print()
    print("To make highlighting earlier (if now too late):")
    print("  reference_line_y = visible_top_y + (visible_height * 0.80)  # 80%")

def calculate_optimal_position():
    """Calculate what might be the optimal position"""
    print("\nOptimal Position Calculation")
    print("=" * 35)
    
    print("REASONING FOR 85% FROM TOP:")
    print("- Provides 15% of screen as 'lead time'")
    print("- Matches traditional piano roll conventions")
    print("- Balances preview with immediate feedback")
    print("- Should feel natural for most users")
    print()
    
    print("IF 85% IS STILL TOO EARLY:")
    print("- Try 90% (10% lead time)")
    print("- Try 95% (5% lead time)")
    print("- Consider user-configurable setting")
    print()
    
    print("FALLBACK OPTIONS:")
    print("- Make position configurable (slider in UI)")
    print("- Add keyboard shortcuts to adjust on-the-fly")
    print("- Different defaults for different zoom levels")

def test_position_consistency():
    """Test that the position works consistently across zoom levels"""
    print("Position Consistency Test")
    print("=" * 30)
    
    test_scenarios = [
        {"view_height": 100, "zoom": "Very zoomed in"},
        {"view_height": 400, "zoom": "Normal view"},
        {"view_height": 800, "zoom": "Zoomed out"},
        {"view_height": 2000, "zoom": "Full file view"},
    ]
    
    print("Testing 85% position at different zoom levels:")
    print()
    
    for scenario in test_scenarios:
        height = scenario["view_height"]
        zoom = scenario["zoom"]
        
        lead_distance = height * 0.15  # 15% from bottom
        
        print(f"{zoom} (height: {height}):")
        print(f"  Lead time distance: {lead_distance:.0f} pixels")
        print(f"  Reference at: {height * 0.85:.0f} from top")
        print()

if __name__ == "__main__":
    analyze_highlighting_timing()
    test_different_reference_positions()
    explain_coordinate_system_timing()
    suggest_fine_tuning_approach()
    calculate_optimal_position()
    test_position_consistency()
    
    print("Next Steps:")
    print("1. Test 85% position - should be better than 67%")
    print("2. If still too early, try 90% or 95%")
    print("3. Find the position that feels most natural")
    print("4. Consider making it user-configurable for final polish")
