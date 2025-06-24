@echo off
echo Starting Python MIDI Gapper 2...
cd /d "g:\My Drive\Programming Projects\Player Piano\Jeremys Code\Python Midi Gapper 2"
python main.py
if errorlevel 1 (
    echo.
    echo Program encountered an error. Press any key to close.
    pause >nul
) else (
    echo.
    echo Program closed normally.
    timeout /t 2 >nul
)
