import soundfile as sf
from datasets import load_dataset
from transformers import (
    Wav2Vec2CTCTokenizer,
    Wav2Vec2FeatureExtractor,
    Wav2Vec2ForCTC,
    Wav2Vec2Processor,
)

"""
Pipeline:
Wav2VecProcessor(feature_extractor, tokenizer)
  - Wav2Vec2FeatureExtractor() (default settings work)
  - Wav2Vec2CTCTokenizer(vocab_file)
Wav2Vec2ForCTC() (use pretrained)
"""

# Load dataset
librispeech = load_dataset("patrickvonplaten/librispeech_asr_dummy", "clean", split="validation")

feature_extractor = Wav2Vec2FeatureExtractor()

# Create tokenizer
# Reference for training (probably unnecessary since this should be pretrained):
# https://huggingface.co/course/chapter6/2?fw=pt#training-a-new-tokenizer
tokenizer = Wav2Vec2CTCTokenizer(
    vocab_file='vocab.json',
    word_delimiter_token='<ew>',
    replace_word_delimiter_char='space',
    # TODO: need to determine whether this setting treats lower case letters the same, or makes them distinct tokens
    do_lower_case=False,
)

# Create processor (performs preprocessing from raw data to transformer input)
processor = Wav2Vec2Processor(feature_extractor, tokenizer)
print(processor)
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
print(model)
