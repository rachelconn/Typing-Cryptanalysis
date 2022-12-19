import argparse
import json
from pathlib import Path
import matplotlib
from matplotlib import pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('log_paths', type=Path, nargs='+')

def parse_stats(line):
    return json.loads(line.split(' - ')[1].rstrip())

def parse_log(path):
    # Parse loss values for each epoch
    train_epochs = []
    train_losses = []
    valid_epochs = []
    valid_losses = []
    with open(path, 'r') as log_file:
        for line in log_file:
            if '[train][INFO]' in line:
                stats = parse_stats(line)
                if 'train_loss' not in stats:
                    continue
                train_epochs.append(int(stats['epoch']))
                train_losses.append(float(stats['train_loss']))
            elif '[valid][INFO]' in line:
                stats = parse_stats(line)
                valid_epochs.append(int(stats['epoch']))
                valid_losses.append(float(stats['valid_loss']))
    return train_epochs, train_losses, valid_epochs, valid_losses

def main():
    """ Stitches together fairseq log files to show training results """
    args = parser.parse_args()
    matplotlib.use('QtCairo')
    train_epochs = []
    train_losses = []
    valid_epochs = []
    valid_losses = []
    for path in args.log_paths:
        parsed = parse_log(path)
        train_epochs.extend(parsed[0])
        train_losses.extend(parsed[1])
        valid_epochs.extend(parsed[2])
        valid_losses.extend(parsed[3])

    # # Graph loss over time
    plt.title('Pre-training training and validation loss')
    plt.xlabel('Epoch')
    plt.ylabel('Total Loss (Contrastive + Diversity)')
    plt.plot(train_epochs, train_losses, label='Training loss')
    plt.plot(valid_epochs, valid_losses, label='Validation loss')
    plt.legend()
    plt.savefig('pretraining.pdf')


if __name__ == '__main__':
    main()
