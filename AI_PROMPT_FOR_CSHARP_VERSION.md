# AI Prompt for Creating MIDI Gapper in C#

## Overview
This document outlines how to prompt an AI to recreate the Python MIDI Gapper application in C# with full feature parity. The application is a professional MIDI editing and visualization tool with real-time playback, gap creation, and Synthesia-style visualization.

## Primary Prompt Structure

### Initial System Prompt
```
You are an expert C# desktop application developer specializing in MIDI processing, audio playback, and rich GUI applications using WPF (Windows Presentation Foundation). You have deep knowledge of:
- C# .NET Framework/Core
- WPF for rich desktop UIs
- MIDI file processing and manipulation
- Audio playback systems (DirectSound, WASAPI)
- Real-time graphics and canvas drawing
- Multi-threading for audio and UI
- Professional software architecture patterns (MVVM)

Create a complete, professional-grade MIDI editing application in C# WPF that matches the functionality described below.
```

### Core Application Description
```
Create a C# WPF application called "MIDI Gapper" with the following specifications:

## Application Purpose
A professional MIDI file editor designed for player piano applications that:
1. Loads and visualizes MIDI files with piano roll display
2. Creates configurable gaps between notes for mechanical piano striking
3. Provides real-time audio playback with seeking capabilities
4. Offers Synthesia-style visualization with keyboard highlighting
5. Supports comprehensive MIDI editing and channel management

## Architecture Requirements
- Use WPF with MVVM pattern for clean separation of concerns
- Implement responsive UI that handles large MIDI files (20,000+ notes)
- Use async/await for file operations and audio processing
- Implement proper resource management and cleanup
- Support themes and configurable UI scaling
```

### Technical Implementation Details

#### MIDI Processing Requirements
```
## MIDI File Processing
Use a C# MIDI library (recommend NAudio or DryWetMIDI) to:

1. **File Loading & Parsing**
   - Load MIDI files (types 0, 1, 2)
   - Parse all tracks, channels, and message types
   - Extract tempo changes, time signatures, and meta data
   - Convert delta times to absolute times for processing
   - Support drag-and-drop file loading

2. **MIDI Data Structures**
   - Create classes for: MidiNote, MidiTrack, MidiChannel
   - Track note on/off pairs with precise timing
   - Handle overlapping notes and hanging note resolution
   - Store instrument assignments per channel (General MIDI)
   - Maintain tempo map for accurate time calculations

3. **Gap Creation Algorithm**
   - Implement configurable gap insertion between consecutive notes
   - Process notes by pitch/channel to avoid cross-interference
   - Use absolute time reconstruction for precise timing
   - Maintain musical integrity while creating mechanical gaps
   - Support undo/redo for gap modifications
```

#### Audio Playback System
```
## Audio Playback Implementation
Implement dual audio backend support:

1. **Primary: NAudio with MIDI Synthesis**
   - Use NAudio.Midi for MIDI file playback
   - Implement soundfont-based synthesis if available
   - Support real-time seeking within MIDI files
   - Handle tempo changes during playback

2. **Fallback: Windows MIDI Services**
   - Use Windows built-in MIDI synthesizer
   - Implement seek-by-recreation (temporary MIDI files)
   - Ensure robust error handling and fallback logic

3. **Playback Controls**
   - Play/Pause/Stop with proper state management
   - Seek to any position via scrollbar or keyboard
   - Real-time position tracking with millisecond precision
   - Automatic cleanup of temporary resources
```

#### Visualization System
```
## Piano Roll Visualization (WPF Canvas)

1. **Main Visualization Canvas**
   - Implement infinite scrolling piano roll view
   - Time flows vertically (bottom = start, top = end)
   - Horizontal layout: 88 piano keys (A0 to C8)
   - Color-coded channels with customizable colors
   - Draw rounded rectangles for notes with duration-based height

2. **Time Grid & Labels**
   - Draw time markers every 2 seconds
   - Label major time points (minutes:seconds.milliseconds)
   - Octave markers at C notes with octave numbers
   - Tempo change indicators where applicable

3. **Real-time Highlighting**
   - Blue reference line showing current playback position
   - Spatial optimization for large files (viewport culling)
   - Smooth scrolling with momentum and easing
   - Keyboard highlighting synchronized with audio

4. **Performance Optimization**
   - Use virtualization for large MIDI files
   - Implement spatial indexing for note lookup
   - Throttle updates during continuous scrolling
   - Use hardware acceleration where possible
```

#### User Interface Layout
```
## WPF Window Layout Structure

1. **Top Control Panel**
   - File operations: Open, Save, Recent files menu
   - Gap controls: Gap size input (ms), Create Gaps button
   - MIDI info display: File name, tracks, format, duration, tempo
   - Channel legend with expand/collapse on hover

2. **Playback Controls (Media Player Style)**
   - Large, accessible buttons: Rewind (⏮), Play/Pause (▶/⏸), Stop (⏹)
   - LED-style position display showing MM:SS.mmm
   - Professional color coding: Green=ready, Orange=playing, Red=stop
   - Keyboard shortcuts: Space=play/pause, Home=rewind, Arrow keys=seek

3. **Main Content Area (TabControl)**
   - **Visualization Tab**: Piano roll with scrollable canvas
   - **MIDI Data Tab**: Raw MIDI data in tree view format
   - **Analysis Tab**: Statistics and channel information

4. **88-Key Piano Keyboard (Bottom)**
   - Synthesia-style keyboard below visualization
   - Real-time key highlighting during playback
   - Visual feedback for currently playing notes
   - Proper black/white key proportions and spacing
```

#### Channel Management System
```
## Channel Control Features

1. **Channel Legend Panel**
   - Checkbox per channel for visibility toggle
   - Color indicators matching visualization
   - Instrument names from General MIDI standard
   - "Solo" buttons to isolate single channels
   - Right-click context menu for channel deletion

2. **Channel Operations**
   - Toggle visibility with immediate visualization update
   - Delete channels with confirmation dialog
   - Recolor channels with color picker
   - Mute/solo during playback
   - Export individual channels to separate files
```

### Advanced Features Implementation
```
## Professional Features

1. **Configuration & Settings**
   - Save/restore window size, position, and state
   - Remember last opened file and recent files list
   - Configurable Y-axis scaling for visualization density
   - Theme support (light/dark modes)
   - Keyboard shortcut customization

2. **Performance & Scalability**
   - Handle MIDI files with 20,000+ notes smoothly
   - Implement progress bars for long operations
   - Use background workers for file processing
   - Memory-efficient note storage and rendering
   - Responsive UI during heavy operations

3. **Error Handling & Robustness**
   - Comprehensive exception handling with user-friendly messages
   - Graceful handling of corrupted MIDI files
   - Audio system fallback mechanisms
   - Automatic recovery from playback errors
   - Detailed logging for troubleshooting

4. **Accessibility & Usability**
   - High DPI awareness and scaling
   - Keyboard navigation support
   - Screen reader compatibility
   - Tooltips and status bar information
   - Intuitive mouse interactions (scroll, zoom, select)
```

### Code Quality Requirements
```
## Development Standards

1. **Architecture Patterns**
   - Implement MVVM with proper data binding
   - Use dependency injection for services
   - Separate concerns: UI, Business Logic, Data Access
   - Create testable, modular components

2. **Code Quality**
   - Follow C# coding conventions and naming standards
   - Include comprehensive XML documentation
   - Implement proper async/await patterns
   - Use LINQ for data processing where appropriate
   - Handle all edge cases and error conditions

3. **Resource Management**
   - Implement IDisposable for audio resources
   - Use 'using' statements for file operations
   - Proper cleanup in window closing events
   - Memory leak prevention and monitoring

4. **Testing Considerations**
   - Design for unit testing with mock interfaces
   - Separate UI logic from business logic
   - Create testable MIDI processing functions
   - Include sample MIDI files for testing
```

### Specific Library Recommendations
```
## Required NuGet Packages

1. **MIDI Processing**
   - Melanchall.DryWetMidi (recommended) OR NAudio
   - For robust MIDI file reading, writing, and manipulation

2. **Audio Playback**
   - NAudio for Windows audio integration
   - Windows.Media for fallback MIDI synthesis

3. **UI Enhancement**
   - ModernWpf or MaterialDesignInXamlToolkit for modern UI
   - Extended.Wpf.Toolkit for additional controls

4. **Utilities**
   - Newtonsoft.Json for configuration persistence
   - Serilog for structured logging
   - Microsoft.Extensions.DependencyInjection for IoC
```

### Testing & Validation Prompts
```
## Validation Requirements

Create test scenarios that verify:
1. Loading various MIDI file formats (Type 0, 1, 2)
2. Gap creation with different time intervals
3. Audio playback from different seek positions
4. Handling large files (10,000+ notes) without performance issues
5. Channel visibility toggling and deletion
6. Window state persistence across application restarts
7. Error recovery from audio system failures
8. Memory usage stability during extended use

Include sample MIDI files for testing:
- Simple melody (small file)
- Complex orchestral piece (large file)
- File with multiple tempo changes
- Files with various channel configurations
```

## Implementation Instructions for AI

### Phase 1: Core Framework
"Start by creating the basic WPF application structure with MVVM pattern, main window layout, and MIDI file loading capability using DryWetMIDI library."

### Phase 2: Visualization
"Implement the piano roll visualization with Canvas drawing, note rectangles, time grid, and basic scrolling functionality."

### Phase 3: Audio System
"Add NAudio-based MIDI playback with play/pause/stop controls and position tracking."

### Phase 4: Advanced Features
"Implement gap creation algorithm, channel management, seeking functionality, and performance optimizations."

### Phase 5: Polish & Testing
"Add error handling, configuration persistence, accessibility features, and comprehensive testing scenarios."

## Expected Deliverables

The AI should produce:
1. Complete Visual Studio solution with proper project structure
2. All C# source files with comprehensive documentation
3. XAML files for WPF UI with proper styling
4. Configuration files and resources
5. NuGet package references list
6. README with build and usage instructions
7. Sample MIDI files for testing
8. User manual with feature documentation

This prompt structure ensures the AI creates a professional, feature-complete C# WPF application that matches the functionality of the original Python MIDI Gapper while leveraging C#'s strengths in desktop application development and audio processing.
