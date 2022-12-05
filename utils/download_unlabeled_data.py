from pathlib import Path
import tempfile

from pydub import AudioSegment
from pytube import Playlist

# Clip length (in ms)
clip_length = 20_000

# Output directory
base_directory = Path(__file__).resolve().parent.parent
output_directory = base_directory / 'dataset' / 'unlabeled'
output_directory.mkdir(parents=True, exist_ok=True)

# Download each video in dataset playlist
playlist = Playlist('https://www.youtube.com/playlist?list=PLjrqtTEew07mfoATnX4DZ1kMU9ZS8JaNZ')
with tempfile.TemporaryDirectory() as download_directory:
    print(f'Downloading videos to temporary folder {download_directory}.')
    for video_idx, video in enumerate(playlist.videos, 1):
        print(f'({video_idx: 3}/{playlist.length:03}) - Downloading {video.title}...')
        # Find highest quality audio stream
        audio_streams = video.streams.filter(only_audio=True)
        best_stream = None
        best_abr = 0
        for stream in audio_streams:
            abr = int(stream.abr[:-4])
            if abr > best_abr:
                best_stream = stream
                best_abr = abr

        # Download to temp folder
        downloaded_video_path = best_stream.download(download_directory)

        # Create clips from video
        print('    Creating clips...')
        audio = AudioSegment.from_file(downloaded_video_path).set_frame_rate(16_000)
        for clip_idx, clip_start in enumerate(range(0, len(audio), clip_length), 1):
            clip_end = min(clip_start + clip_length, len(audio))
            clip = audio[clip_start:clip_end]
            clip.export(
                output_directory / f'{video_idx:03}_{clip_idx:04}.wav',
                format='wav',
            )
        print('    Finished processing video.')
