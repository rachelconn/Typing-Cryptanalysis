import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('tsv_path', type=Path, nargs='+')

def parse_stats(line):
    return json.loads(line.split(' - ')[1].rstrip())


def main():
    splits = ['train', 'valid']
    args = parseargs()

    for split in splits:
        dataset_folder = Path(__file__).resolve().parent.parent / 'dataset'
        ltr_file_path = dataset_folder / f'{split}.ltr'
        wrd_file_path = dataset_folder / f'{split}.wrd'
        with open(args.tsv_path, 'r') as tsv:
            audio_folder = Path(next(tsv).strip())
            label_folder = audio_folder.parent / 'labels'
            with open(ltr_file_path, 'w') as ltr_file, open(wrd_file_path, 'w') as wrd_file:
                for line in tsv:
                    filename = f"{line.split()[0].rsplit('.')[0]}.txt"
                    label_file_path = label_folder / filename
                    with open(label_file_path, 'r') as label_file:
                        labels = label_file.readline()[:-1]
                        letters = ' '.join(list(labels.replace(' ', '|'))) + ' |'
                        ltr_file.write(f'{letters}\n')
                        words = labels.replace('|', ' ')
                        wrd_file.write(f'{words}\n')

if __name__ == '__main__':
    main()
