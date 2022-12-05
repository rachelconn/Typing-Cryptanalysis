# Installation
1. Download python 3.8 or higher (tested with 3.8.5)
2. If not running on Windows, follow the instructions for setting up PyAudio [here](https://pypi.org/project/PyAudio/)
3. If you plan on recording training data, run `pip install -r data_collection_requirements.txt`
4. If you plan on using ML models, run `pip install -r ml_requirements.txt`

# Collecting labeled data
After installation, run `python record.py` and start typing to create labeled typing data.
Your default microphone will be used to record, so make sure it's set up correctly before starting a long recording session.

# Data format
Labeled training data will be collected into the `labels` folder with a filename corresponding to the datetime when the data was collected.
Each line of the label file consists of a timestamp for the keypress detected relative to the start of the audio and the [scancode](https://deskthority.net/wiki/Scancode) of the key pressed with microsecond precision, separated by a space.

These raw data files can be converted into smaller clips to make training feasible by running `python utils/prepare_dataset.py`.
This will create a `dataset` folder in the project root, with an `audio` folder containing audio clips
and a `labels` folder containing one character corresponding to each scancode for a key pressed in the corresponding clip.
