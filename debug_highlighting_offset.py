#!/usr/bin/env python3
"""
Diagnose the highlighting offset issue.
The problem: "highlighted notes are off at the bottom position and closer at the top"
"""

def analyze_highlighting_offset_pattern():
    """Analyze why highlighting accuracy varies by position"""
    print("Analyzing Highlighting Offset Pattern")
    print("=" * 45)
    
    print("REPORTED ISSUE:")
    print("- Bottom position: Highlighted notes are OFF")
    print("- Top position: Highlighted notes are CLOSER")
    print()
    
    print("This suggests a systematic error that varies with scroll position.")
    print("Let's investigate potential causes...")
    print()

def test_coordinate_system_understanding():
    """Test our understanding of the coordinate system"""
    print("Coordinate System Analysis")
    print("=" * 30)
    
    print("CANVAS COORDINATE SYSTEM:")
    print("- Y=0 at TOP of canvas (latest time in MIDI)")
    print("- Y=max at BOTTOM of canvas (earliest time in MIDI)")
    print()
    
    print("SCROLL COORDINATE SYSTEM:")
    print("- scroll_top=0.0 means TOP of content visible")
    print("- scroll_bottom=1.0 means BOTTOM of content visible")
    print()
    
    print("NOTE RECTANGLE POSITIONING:")
    print("- Earlier times (t=0) → Y coordinates near bottom (high Y values)")
    print("- Later times (t=max) → Y coordinates near top (low Y values)")
    print()
    
    print("POTENTIAL ISSUE:")
    print("If highlighting zone calculation doesn't account for this properly,")
    print("we could get systematic offset that varies by position!")

def diagnose_highlighting_zone_issues():
    """Diagnose potential issues with highlighting zone calculation"""
    print("\nHighlighting Zone Diagnosis")
    print("=" * 35)
    
    print("CURRENT APPROACH:")
    print("1. Get visible area: canvas_top, canvas_bottom from yview()")
    print("2. Convert to absolute coords: multiply by total_canvas_height")
    print("3. Calculate center zone: 30% of visible height around center")
    print("4. Test intersection with note rectangles")
    print()
    
    print("POTENTIAL PROBLEMS:")
    print()
    
    print("1. ZONE SIZE ISSUE:")
    print("   - 30% zone might be too large or too small")
    print("   - Should we use a fixed pixel height instead?")
    print("   - Should we highlight at a specific line/position?")
    print()
    
    print("2. ZONE POSITION ISSUE:")
    print("   - Using center of visible area")
    print("   - Maybe should use bottom 1/3 or top 1/3?")
    print("   - Maybe should match playback position indicator?")
    print()
    
    print("3. COORDINATE CONVERSION ISSUE:")
    print("   - canvas.yview() returns 0.0-1.0 scroll positions")
    print("   - Multiplying by total_canvas_height")
    print("   - Could have rounding or precision errors")
    print()
    
    print("4. RECTANGLE COORDINATE ISSUE:")
    print("   - canvas.coords() returns actual pixel coordinates")
    print("   - These should match our calculated zone coordinates")
    print("   - Mismatch could cause offset")

def propose_debugging_approach():
    """Propose a debugging approach to identify the issue"""
    print("\nDebugging Strategy")
    print("=" * 25)
    
    print("STEP 1: ADD DEBUG LOGGING")
    print("- Log visible area coordinates")
    print("- Log highlighting zone coordinates") 
    print("- Log sample note rectangle coordinates")
    print("- Compare expected vs actual positions")
    print()
    
    print("STEP 2: TEST DIFFERENT ZONE STRATEGIES")
    print("- Try fixed pixel height zone (e.g., 50 pixels)")
    print("- Try different zone positions (top/center/bottom)")
    print("- Try single-line highlighting instead of zone")
    print()
    
    print("STEP 3: VALIDATE COORDINATE MAPPING")
    print("- Verify canvas.yview() values make sense")
    print("- Verify total_canvas_height is correct")
    print("- Verify rectangle coordinates match visualization")
    print()
    
    print("STEP 4: TEST POSITION-SPECIFIC FIXES")
    print("- If bottom is off, check bottom-specific coordinate handling")
    print("- If top is closer, understand why top works better")
    print("- Look for scroll position dependent errors")

def suggest_improved_approaches():
    """Suggest alternative approaches to fix the highlighting"""
    print("\nImproved Highlighting Approaches")
    print("=" * 40)
    
    print("OPTION 1: FIXED REFERENCE LINE")
    print("- Instead of 30% zone, use single reference line")
    print("- Position line at specific fraction of view (e.g., 2/3 from top)")
    print("- Highlight notes that cross this line")
    print("- More predictable and easier to debug")
    print()
    
    print("OPTION 2: PLAYBACK POSITION SYNC")
    print("- Use the position timer as reference point")
    print("- Calculate where that time should appear visually")
    print("- Highlight notes at that exact Y coordinate")
    print("- Ensures highlighting matches timer display")
    print()
    
    print("OPTION 3: USER-CONFIGURABLE ZONE")
    print("- Let user adjust highlighting zone size and position")
    print("- Provide visual feedback showing the highlighting zone")
    print("- Allow fine-tuning for different preferences")
    print()
    
    print("OPTION 4: MOUSE CURSOR REFERENCE")
    print("- Highlight notes near the mouse cursor position")
    print("- Most intuitive - highlights what user is looking at")
    print("- Works naturally with user's visual attention")
    print()
    
    print("RECOMMENDED: Option 1 (Fixed Reference Line)")
    print("- Simple and predictable")
    print("- Easy to debug and adjust")
    print("- Consistent behavior across all positions")

if __name__ == "__main__":
    analyze_highlighting_offset_pattern()
    test_coordinate_system_understanding()
    diagnose_highlighting_zone_issues()
    propose_debugging_approach()
    suggest_improved_approaches()
    
    print("\nNext Steps:")
    print("1. Add debug logging to understand current coordinate values")
    print("2. Try fixed reference line approach for simplicity")
    print("3. Test positioning that matches user expectations")
    print("4. Validate that highlighting feels natural at all scroll positions")
