import mido

print("Checking MIDI backend...")
print(f"Mido version: {mido.__version__}")

try:
    print("Backend:", mido.backend)
    print("Available MIDI output devices:", mido.get_output_names())
    print("Available MIDI input devices:", mido.get_input_names())
except Exception as e:
    print(f"Error accessing MIDI: {e}")
    
print("Test complete.")
