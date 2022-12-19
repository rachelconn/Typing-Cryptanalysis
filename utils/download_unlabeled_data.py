from pathlib import Path
import tempfile
import os
import subprocess

from pydub import AudioSegment
from pytube import Playlist

# Clip length (in ms)
clip_length = 20_000

# Output directory
base_directory = Path(__file__).resolve().parent.parent
output_directory = base_directory / 'dataset' / 'unlabeled' / 'audio'
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
        video_download_path = best_stream.download(download_directory, f'{video_idx:03}.mp4')
        # Create clips from video
        print('    Creating clips...')
        clip_path = output_directory / f'{video_idx:03}_%04d.wav'
        create_clip_command = f'ffmpeg -i {video_download_path} -map 0 -segment_time 00:00:20 -f segment -reset_timestamps 1 -ar 16000 -ac 1 {clip_path}'.split()
        subprocess.run(create_clip_command)
        print('    Finished processing video.')
