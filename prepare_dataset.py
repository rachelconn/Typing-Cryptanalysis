"""
Splits all training data from the raw audio and labels folders into small ~8-20 second clips
so that they're more fit for training.
"""
from pathlib import Path
from pydub import AudioSegment

# Constants determining output clip length (in ms)
MIN_CLIP_LENGTH = 8_000
MAX_CLIP_LENGTH = 20_000

# Determine paths for I/O
base_directory = Path(__file__).resolve().parent
input_audio_directory = base_directory / 'audio'
input_label_directory = base_directory / 'labels'
output_base_directory = base_directory / 'dataset'
output_audio_directory = output_base_directory / 'audio'
output_label_directory = output_base_directory / 'labels'

# Create output directories
output_audio_directory.mkdir(parents=True, exist_ok=True)
output_label_directory.mkdir(exist_ok=True)

def save_clip(source_file, clip_number, clip, clip_keys):
    output_audio_file = output_audio_directory / f'{source_file.name}_{clip_number:04}.wav'
    output_label_file = output_label_directory / f'{source_file.name}_{clip_number:04}.txt'
    # Export audio
    clip.export(output_audio_file, format="wav")
    # Export key codes
    label_text = bytes(clip_keys).decode('utf8')
    with output_label_file.open('w') as label_file:
        label_file.write(label_text)

for child in input_label_directory.iterdir():
    if not child.is_file():
        continue

    # Parse timestamps and keys from file
    timestamps = []
    keys = []
    with child.open() as input_label_file:
        for line in input_label_file:
            timestamp, key = line.rstrip().split(' ')
            timestamp = int(float(timestamp) * 1000) # Convert to milliseconds
            key = int(key)
            timestamps.append(timestamp)
            keys.append(key)

    # Create utility function for clipping audio
    audio_file = input_audio_directory / f'{child.name}.wav'
    audio = AudioSegment.from_wav(audio_file)
    def create_clip(start_idx, end_idx):
        # Add slight space before the first key press and after the last one to keep residual key press sound
        start_timestamp = timestamps[start_idx] - 50
        end_timestamp = timestamps[end_idx] + 50
        return audio[start_timestamp:end_timestamp]

    # Split into clips based on timestamps
    start_idx = 0
    start_timestamp = timestamps[0]
    clip_number = 1
    for i, timestamp in enumerate(timestamps):
        # Check if clipping including the current timestamp is too long
        if timestamp > start_timestamp + MAX_CLIP_LENGTH:
            # Save clip with previous keys
            clip = create_clip(start_idx, i - 1)
            clip_keys = keys[start_idx:i]
            save_clip(child, clip_number, clip, clip_keys)
            # Update helper variables
            clip_number += 1
            start_idx = i
            start_timestamp = timestamp
    # Create clip of the end
    if start_idx < len(timestamps) - 1:
        clip = create_clip(start_idx, len(timestamps) - 1)
        clip_keys = keys[start_idx:len(timestamps) - 1]
        save_clip(child, clip_number, clip, clip_keys)
