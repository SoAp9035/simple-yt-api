# Simple YouTube API

A lightweight Python wrapper for extracting video metadata and transcripts from YouTube videos.

## Features

- 🎥 Extract video metadata (title, thumbnail, description)
- 📝 Get video transcripts in multiple languages
- ⚡ Simple and easy to use interface
- 🔒 No API key required
- 🌐 Support for both YouTube URL formats (`youtube.com` and `youtu.be`)

## Installation

```bash
pip install simple-yt-api
```

## Quick Start

```python
from simple_yt_api import YouTubeAPI

# Initialize with a YouTube URL
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
yt = YouTubeAPI(url)

# Get video metadata
metadata = yt.data()
print(metadata['title'])

# Get video transcript
transcript = yt.get_transcript(languages=['en'])  # Get English transcript
print(transcript)

# Get both metadata and transcript at once
data, transcript = yt.get_video_data_and_transcript(
    languages=['en', 'tr'],  # Priority languages
    as_dict=False  # Return transcript as plain text
)
```

## API Reference

### YouTubeAPI Class

#### `YouTubeAPI(url: str)`
Initialize the API with a YouTube video URL.

#### `data() -> dict`
Returns video metadata dictionary containing:
- `video_id`: YouTube video ID
- `title`: Video title
- `img_url`: Thumbnail URL
- `short_description`: Video description

#### `get_transcript(languages: list = [], as_dict: bool = False) -> str | dict`
Get video transcript in specified languages.
- `languages`: List of language codes (e.g., ['en', 'tr'])
- `as_dict`: If True, returns timestamp dictionary format

#### `get_video_data_and_transcript(languages: list = [], as_dict: bool = False) -> tuple`
Returns both video metadata and transcript for a YouTube video in one call without worrying about errors.

## Error Handling

The library includes custom exceptions:
- `InvalidURL`: Invalid YouTube URL format
- `NoVideoFound`: Video not accessible or doesn't exist
- `NoTranscriptFound`: No transcript available for the video

## Requirements

- requests>=2.32.3
- beautifulsoup4>=4.13.3
- youtube-transcript-api>=0.6.3

## Disclaimer

This is an unofficial tool created by independent developers with no affiliation to any video platforms. The creators take no responsibility for how it is used. Users must ensure their usage complies with applicable terms of service and laws. The package may stop working if underlying platforms change their structure. Use at your own risk.

## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License.

## Links

- [GitHub Repository](https://github.com/SoAp9035/simple-yt-api)
- [PyPI Package](https://pypi.org/project/simple-yt-api/)
- [Buy Me a Coffee](https://buymeacoffee.com/soap9035/)