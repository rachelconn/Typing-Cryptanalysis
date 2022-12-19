from collections import Counter
from pathlib import Path
import os

label_file_directory = Path(__file__).resolve().parent.parent / 'dataset' / 'labels'
character_freqs = Counter()
for filename in os.listdir(label_file_directory):
    path = os.path.join(label_file_directory, filename)
    with open(path, 'r') as label_file:
        for line in label_file.readlines():
            line = line.rstrip()
            character_freqs.update(line)

with open('dict.ltr.txt', 'w') as vocab_file:
    print('Frequencies:')
    for character, occs in character_freqs.most_common():
        print(f'    {character}: {occs}')
        vocab_file.write(f'{character} {occs}\n')


print('Characters in alphabetical order:')
for character in sorted(character_freqs.keys()):
    print(f'    {character}')
