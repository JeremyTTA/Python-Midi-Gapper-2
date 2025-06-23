# Python MIDI Gapper 2

A comprehensive MIDI file editor and visualizer built with Python and Tkinter, featuring real-time playback with Synthesia-style piano roll visualization and keyboard highlighting.

## 🎵 Features

### MIDI File Editing
- **Load and save MIDI files** in standard `.mid`/`.midi` format
- **Insert time gaps** between notes with customizable gap duration (milliseconds)
- **Channel management** with visual channel legend and selective deletion
- **XML-based editing** with direct text manipulation of MIDI data
- **Automatic backup** with modified filename suggestions

### Advanced Visualization
- **Piano roll display** with 88-key piano keyboard (A0 to C8)
- **Color-coded channels** with 16 distinct predefined colors
- **Time-based scrolling** with precise time markers (seconds and milliseconds)
- **Note duration visualization** with proportional rectangle heights
- **Real-time highlighting** of active notes during playback
- **Scalable Y-axis** for better visibility of dense MIDI sections

### Professional Playback Engine
- **pygame-powered audio** with high-quality MIDI synthesis
- **Precise seeking** with temporary file generation for accurate positioning
- **Perfect timing synchronization** between audio and visual elements
- **Real-time keyboard highlighting** showing exactly which notes are playing
- **Professional media controls** with rewind, play/pause toggle, and stop

### User Interface
- **Tabbed interface** with visualization and text editing views
- **Responsive layout** with resizable panes and auto-save window geometry
- **Enhanced LED clock** showing precise playback position (MM:SS.mmm)
- **Intuitive controls** with traditional media player symbols
- **Comprehensive keyboard shortcuts** for efficient navigation

## 🚀 Quick Start

### Prerequisites
```bash
pip install pygame mido tkinter xml
```

### Installation
1. Clone or download this repository
2. Ensure all dependencies are installed
3. Run the application:
```bash
python main.py
```

### Basic Usage
1. **Load a MIDI file**: Click "Open MIDI File" or use the last opened file
2. **View the visualization**: See your MIDI data as a piano roll with colored channels
3. **Play the music**: Use the media controls (⏮ ▶/⏸ ⏹) to control playback
4. **Navigate**: Scroll through the timeline or use arrow keys for precise seeking
5. **Edit**: Add gaps between notes or modify channels as needed
6. **Save**: Export your modified MIDI file

## 🎹 Controls

### Media Player Controls
- **⏮ Rewind**: Return to start (position 0:00.000)
- **▶/⏸ Play/Pause**: Toggle playback (also **Space Bar**)
- **⏹ Stop**: Stop playback and reset position

### Navigation
- **Arrow Keys**: 
  - `Left/Right`: Seek ±1 second
  - `Shift+Left/Right`: Seek ±5 seconds  
  - `Up/Down`: Scroll visualization vertically
- **Mouse Wheel**: Scroll through timeline
- **Scrollbar**: Manual position control with visual sync

### Editing
- **Gap Controls**: Set gap duration (ms) and apply to loaded MIDI
- **Channel Legend**: Toggle channel visibility or select single channels
- **Text View**: Direct XML editing of MIDI structure

## 🏗️ Technical Architecture

### Core Components
- **MidiGapperGUI**: Main application class with Tkinter UI
- **MIDI Processing**: Uses `mido` library for file I/O and manipulation
- **Audio Engine**: pygame mixer for real-time MIDI playback
- **Visualization**: Canvas-based piano roll with spatial optimization
- **Timing System**: Unified timing logic for perfect audio/visual sync

### Key Technical Features
- **Temporal MIDI File Creation**: Generates temporary files for accurate seeking
- **Spatial Note Indexing**: Optimized rendering for large MIDI files (>3000 notes)
- **Real-time Audio Position Calculation**: Handles pygame seeking limitations
- **Channel-aware Highlighting**: Respects deleted channels in visualization
- **Configuration Persistence**: Auto-saves window state and last opened file

### File Format Support
- **Input**: `.mid`, `.midi` files (MIDI Format 0, 1, 2)
- **Output**: Standard MIDI files with preserved timing and channel data
- **Internal**: XML representation for advanced editing capabilities

## 🎯 Advanced Features

### Gap Creation Algorithm
Intelligently inserts time gaps between notes while preserving:
- Note timing relationships
- Channel assignments  
- Tempo changes
- Control change events
- Program change events

### Visualization Optimization
- **Performance Scaling**: Adapts highlighting frequency based on file size
- **Viewport Culling**: Only processes notes visible in current view
- **Color Management**: 16 distinct channel colors with automatic assignment
- **Memory Efficiency**: Optimized canvas object management

### Timing Synchronization
- **Unified Clock**: Single source of truth for all timing calculations
- **Audio-Visual Sync**: Compensates for pygame MIDI seeking limitations  
- **Position Accuracy**: Millisecond-precise position tracking
- **State Persistence**: Maintains timing through pause/resume cycles

## 🛠️ Configuration

The application automatically creates a `config.json` file to store:
- Last opened MIDI file path
- Window geometry and state (maximized/normal)
- Y-scale factor for visualization
- User preferences

## 📊 Supported MIDI Data

### MIDI Events
- **Note On/Off**: Full velocity and channel support
- **Program Changes**: Instrument assignments per channel
- **Control Changes**: Pedal, volume, pan, etc.
- **Tempo Changes**: Variable tempo throughout the file
- **Time Signatures**: Multiple time signatures supported

### Channel Features
- **16-channel support** with distinct color coding
- **General MIDI instrument names** for program changes
- **Channel muting/soloing** through visibility controls
- **Per-channel statistics** in the interface

## 🔧 Development

### Project Structure
```
├── main.py                    # Main application entry point
├── config.json               # Auto-generated configuration
├── README.md                 # This documentation
├── test_*.py                 # Timing and functionality tests
└── documentation/            # Technical documentation
    ├── timing_fixes/         # Timing synchronization docs
    ├── keyboard_highlighting/ # Real-time highlighting docs
    └── playback_features/     # Audio engine documentation
```

### Key Classes and Methods
- **`MidiGapperGUI`**: Main application window and UI management
- **`process_midi()`**: MIDI file loading and analysis
- **`create_gaps()`**: Gap insertion algorithm
- **`draw_visualization()`**: Piano roll rendering
- **`update_keyboard_highlighting()`**: Real-time key highlighting
- **`start_midi_playback()`**: Audio playback management

## 🐛 Known Limitations

- **pygame MIDI Seeking**: Cannot seek to arbitrary positions in original files (solved with temporary file generation)
- **Large File Performance**: Files with >10,000 notes may experience slower initial loading
- **Windows-Specific**: Developed and tested primarily on Windows (cross-platform compatible)

## 🚀 Future Enhancements

- **MIDI Recording**: Direct MIDI input recording capabilities  
- **Plugin Architecture**: Support for VST instruments and effects
- **Advanced Editing**: Note-level editing with piano roll tools
- **Export Options**: Audio export (WAV, MP3) in addition to MIDI
- **Collaborative Features**: Multi-user editing and version control

## 📝 License

This project is open source. Feel free to modify and distribute according to your needs.

## 🙏 Acknowledgments

- **mido**: Excellent Python MIDI library
- **pygame**: Reliable cross-platform audio playback
- **Tkinter**: Robust GUI framework for desktop applications
- **Python Community**: For extensive documentation and support

---

**Created by**: Jeremy Standlee  
**Version**: 2.0  
**Last Updated**: 2025

For technical questions, bug reports, or feature requests, please refer to the included documentation files or create an issue in the project repository.