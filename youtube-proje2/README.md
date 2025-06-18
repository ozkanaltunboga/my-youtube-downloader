# YouTube Downloader Pro

A professional YouTube video downloader with a clean, modern interface.

## Features

- **Clean YouTube-themed Interface**: Red and white color scheme matching YouTube's design
- **Multiple Resolution Options**: View and select from all available video qualities
- **Subtitle Support**: Download subtitles in multiple languages (manual and auto-generated)
- **Format Conversion**: Convert downloaded videos to MP4, AVI, MOV, MKV, WebM, MP3, WAV, or FLAC
- **Progress Tracking**: Real-time download progress with speed and ETA
- **Video Preview**: Thumbnail, title, channel, and duration display

## Installation

1. Install Python 3.8 or higher
2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Install FFmpeg (required for format conversion):
- **Windows**: Download from https://ffmpeg.org/download.html
- **Mac**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

## Usage

Run the application:
```bash
python youtube_downloader.py
```

1. Enter a YouTube URL in the input field
2. Click "Analyze" to fetch video information
3. Select desired video quality from the Quality & Format tab
4. Optionally select subtitles from the Subtitles tab
5. Choose download location (defaults to Downloads folder)
6. Click "Download" to start downloading
7. After download, optionally convert to another format

## Requirements

- Python 3.8+
- customtkinter 5.2.1
- yt-dlp 2024.1.0
- Pillow 10.2.0
- moviepy 1.0.3
- requests 2.31.0
- FFmpeg (for video conversion)