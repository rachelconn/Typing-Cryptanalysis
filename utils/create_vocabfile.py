"""
Creates vocab.json, a json object mapping vocab tokens to their class indices.
Wav2Vec2CTCTokenizer takes in this vocab file as an argument to determine what tokens are in the model's vocabulary.
"""
# TODO: rewrite to use key names instead of scancodes
import json
import os
from pathlib import Path

base_directory = Path(__file__).resolve().parent.parent

output_filename = base_directory / 'vocab.json'
label_file_directory = base_directory / 'labels'

# Collect keystrokes from all label files
keystrokes = set()
for filename in os.listdir(label_file_directory):
    path = os.path.join(label_file_directory, filename)
    with open(path, 'r') as label_file:
        for line in label_file.readlines():
            _timestamp, keystroke = line.rstrip().split(' ', maxsplit=1)
            keystrokes.add(keystroke)

# Write out the collected keystrokes to vocab.json
vocab_data = {token: i for i, token in enumerate(sorted(keystrokes))}
with open(output_filename, 'w') as output_file:
    output_file.write(json.dumps(vocab_data, indent=4))
