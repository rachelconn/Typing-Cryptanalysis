from datetime import datetime
import keyboard
import os
from pathlib import Path
import pyaudio
import time
import wave

# Create label folder
base_directory = Path(__file__).resolve().parent
audio_folder = base_directory / 'audio'
label_folder = base_directory / 'labels'
audio_folder.mkdir(exist_ok=True)
label_folder.mkdir(exist_ok=True)
filename = datetime.now().strftime('%Y%m%d%H%M%S')

# Record audio
p = pyaudio.PyAudio()
nchannels = 1
sampwidth = p.get_sample_size(pyaudio.paInt16)
framerate = 16000
frames_per_buffer = 1024
start_time = datetime.now().timestamp()
wf = wave.open(os.path.join(audio_folder, f'{filename}.wav'), 'wb')
wf.setnchannels(nchannels)
wf.setsampwidth(sampwidth)
wf.setframerate(framerate)
def record_audio(recorded_data, *_):
    wf.writeframes(recorded_data)
    return (recorded_data, pyaudio.paContinue)
audio_stream = p.open(
    format=pyaudio.paInt16,
    channels=nchannels,
    rate=framerate,
    frames_per_buffer=frames_per_buffer,
    input=True,
    stream_callback=record_audio,
)
audio_stream.start_stream()

# Record all keyboard presses with a timestamp
keys_pressed = set()
with open(os.path.join(label_folder, filename), 'w') as label_file:
    def handle_event(e: keyboard.KeyboardEvent):
        if e.event_type == keyboard.KEY_UP:
            keys_pressed.discard(e.scan_code)
        # Don't write to file unless this is a new keypress
        elif e.event_type == keyboard.KEY_DOWN and e.scan_code not in keys_pressed:
            keys_pressed.add(e.scan_code)
            normalized_time = e.time - start_time
            label_file.write(f'{normalized_time} {e.scan_code} {e.name.replace(" ", "")}\n')

    keyboard.hook(handle_event)

    # Idle until manually stopped, recording audio and key events
    while True:
        time.sleep(1)
