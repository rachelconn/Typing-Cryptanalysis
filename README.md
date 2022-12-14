# Installation
1. Download python 3.8 or higher (tested with 3.8.5)
2. If not running on Windows, follow the instructions for setting up PyAudio [here](https://pypi.org/project/PyAudio/)
3. If you plan on recording training data, run `pip install -r data_collection_requirements.txt`

# Collecting labeled data
After installation, run `python record.py` and start typing to create labeled typing data.
Your default microphone will be used to record, so make sure it's set up correctly before starting a long recording session.

## Data format
Labeled training data will be collected into the `labels` folder with a filename corresponding to the datetime when the data was collected.
Each line of the label file consists of a timestamp for the keypress detected relative to the start of the audio and the [scancode](https://deskthority.net/wiki/Scancode) of the key pressed with microsecond precision, separated by a space.

These raw data files can be converted into smaller clips to make training feasible by running `python utils/prepare_dataset.py`.
This will create a `dataset` folder in the project root, with an `audio` folder containing audio clips
and a `labels` folder containing one character corresponding to each scancode for a key pressed in the corresponding clip.

# Collecting unlabeled data
Run utils/download_unlabeled_data.py to create the `dataset/unlabeled` folder. This can be used to pretrain the network.

# Creating files needed for fine-tuning
1. Once labeled data has been collected to the `audio` and `labels` folders, run `get_dataset_composition.py` to create `dict.ltr.txt`, a file used to determine the weights for each class during training.
2. Follow the instructions in [my wav2vec repo](https://github.com/rachelconn/wav2vec2-typing) for generations a tsv file.
2. Run `python utils/create_labels $tsv_path` to create `.wrd` and `.ltr` files in the `dataset` folder. These files are used by fairseq as labels.
3. Place `dict.ltr.txt`, `train.ltr`, `train.wrd`, `valid.ltr`, and `valid.wrd` into the manifest folder described in [my wav2vec repo](https://github.com/rachelconn/wav2vec2-typing).

# Pretraining and training
For model training, follow the steps in [my wav2vec repo](https://github.com/rachelconn/wav2vec2-typing).

# Results visualization
Run `utils.visualize_train_log.py $.log_file_1, $.log_file_2, ...` with any number of log paths >=1.

# Evaluation
Convert the model to hugging face format using the steps in [my wav2vec repo](https://github.com/rachelconn/wav2vec2-typing).
