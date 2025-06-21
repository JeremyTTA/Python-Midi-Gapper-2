# REFERENCE LINE POSITION QUICK ADJUSTMENT GUIDE

## Current Setting: 85% from top (15% from bottom)

## If highlighting is still TOO EARLY:
Change the line in `update_keyboard_highlighting()`:

```python
# Make highlighting happen even later:
reference_line_y = visible_top_y + (visible_height * 0.90)  # 90% from top (10% from bottom)

# Or even later:
reference_line_y = visible_top_y + (visible_height * 0.95)  # 95% from top (5% from bottom)
```

## If highlighting is now TOO LATE:
Change the line back to an earlier position:

```python
# Make highlighting happen earlier:
reference_line_y = visible_top_y + (visible_height * 0.80)  # 80% from top (20% from bottom)
```

## Explanation:
- **Higher percentage** = reference line lower on screen = highlighting happens later
- **Lower percentage** = reference line higher on screen = highlighting happens earlier

## Traditional Piano Roll Reference:
Most piano roll software positions the "current time" line at about 85-95% from the top, giving users visual "lead time" to see upcoming notes.

## Test the Current Change:
The reference line is now at 85% instead of 67%, which should make highlighting feel more natural and less premature.
