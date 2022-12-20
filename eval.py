import argparse
from pathlib import Path
import soundfile as sf
import torch
from datasets import load_dataset
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from utils.character_classes import decode

parser = argparse.ArgumentParser()
parser.add_argument('--dataset_path')
parser.add_argument('--model_path')
args = parser.parse_args()

# load pretrained model
processor = Wav2Vec2Processor.from_pretrained(args.model_path)
model = Wav2Vec2ForCTC.from_pretrained(args.model_path)

dataset = load_dataset(args.dataset_path)

# load audio
for sample in dataset['train']:
    sample = sample['audio']
    path = Path(sample['path']).resolve()
    print(f'Information for {path.name}:')
    audio_input = sample['array']
    sample_rate = sample['sampling_rate']

    # Get contents of label file
    label_path = path.parent.parent / 'labels' / f'{path.stem}.txt'
    with open(label_path, 'r') as label_file:
        print(f'    Label: {decode(label_file.readline().rstrip())}')

    # pad input values and return pt tensor
    input_values = processor(audio_input, sampling_rate=sample_rate, return_tensors="pt").input_values

    # retrieve logits & take argmax
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)

    # transcribe
    transcription = processor.decode(predicted_ids[0])
    print(f'    Prediction: {decode(transcription)}')
