# FluidSynth Installation Guide for MIDI Seeking

## Why FluidSynth?
FluidSynth enables **real MIDI seeking** in the Player Piano app, allowing you to scroll to any position and have audio start immediately from that exact location. Without FluidSynth, the app falls back to pygame which cannot seek in MIDI files.

## Windows Installation

### Option 1: Winget (Recommended)
```bash
winget install FluidSynth.FluidSynth
```

### Option 2: Manual Download
1. Go to https://www.fluidsynth.org/download/
2. Download the Windows binary
3. Extract to `C:\tools\fluidsynth\` (or another location)
4. Add the `bin` directory to your system PATH

### Option 3: Conda
```bash
conda install -c conda-forge fluidsynth
```

## Current Error
```
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\tools\\fluidsynth\\bin'
```

This means the `pyfluidsynth` Python package is installed, but the actual FluidSynth binary is not found at the expected location.

## Solution
1. **Install FluidSynth binary** using one of the options above
2. **Restart the application** - it will automatically detect FluidSynth
3. **Verify installation** - you should see:
   ```
   ✓ FluidSynth available - will use for MIDI playback with seeking support
   ```

## Fallback Behavior
If FluidSynth is not available, the app will automatically fall back to pygame with these messages:
```
⚠ FluidSynth not available - falling back to pygame (no seeking)
⚠ Using pygame fallback (no seeking)
```

The app will still work, but without real seeking capability (it will use the temporary file approach).

## Soundfonts
FluidSynth requires a soundfont to generate audio. The app automatically searches for:
- Windows: `C:\Windows\System32\drivers\gm.dls`
- Common SF2 locations

If no soundfont is found, you may need to download one (like FluidR3_GM.sf2) for audio output.

## Testing
After installation, run the app and look for:
```
✓ FluidSynth available - will use for MIDI playback with seeking support
Initializing FluidSynth...
✓ FluidSynth initialized successfully
```

Then test seeking by:
1. Loading a MIDI file
2. Scrolling to a different position
3. Pressing play - audio should start immediately from that position

## Troubleshooting

### "Failed to create FluidSynth synthesizer"
- FluidSynth binary not properly installed
- Try reinstalling with a different method

### "Failed to create FluidSynth audio driver"
- Audio system is busy
- Try closing other audio applications
- Restart the app

### "No soundfont found"
- FluidSynth will work but may be silent
- Download a soundfont like FluidR3_GM.sf2
- Place it in a common location

### Still using pygame fallback
- Restart the application after installing FluidSynth
- Check that FluidSynth is in your system PATH
- Verify the installation worked by running `fluidsynth --version` in a terminal
