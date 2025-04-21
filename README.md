# Simple YouTube API

An unofficial lightweight Python wrapper for extracting video metadata and transcripts from YouTube videos.

## Features

- 🎥 Extract video metadata (title, thumbnail, short description)
- 📝 Get video transcripts in various languages
- ⚡ Simple and easy to use interface
- 🔒 No API key required

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
print(metadata["title"])

# Get video transcript
transcript = yt.get_transcript(language_code="tr", as_dict=True)  # Get Turkish transcript. Defaults to "en".
print(transcript)

# Get both metadata and transcript at once
data, transcript = yt.get_video_data_and_transcript(
    language_code="es",
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

#### `get_transcript(language_code: str = "en", as_dict: bool = True) -> list[dict] | str`
Get video transcript in specified languages.
- `language_code (str, optional)`: The language code for the desired transcript. Defaults to "en".
- `as_dict (bool, optional)`: If `True`, returns the transcript as a list of dictionaries; otherwise, returns the transcript as a string. Defaults to `True`.

#### `get_video_data_and_transcript(language_code: str = "en", as_dict: bool = True) -> tuple`
Returns both video metadata and transcript for a YouTube video in one call without worrying about errors.

## Error Handling

The library includes custom exceptions:
- `InvalidURL`: For invalid YouTube URL format.
- `NoVideoFound`: When a video is not accessible or doesn't exist.
- `NoMetadataFound`: When no metadata is found for the video.
- `TranscriptsDisabled`: When transcripts are not available for the video.
- `NoTranscriptFound`: When no transcript is available for the video.

## Requirements

- requests==2.32.3
- beautifulsoup4==4.13.4
- youtube-transcript-api==1.0.3

## Warning

Sending too many requests in a short period might lead to your IP address being temporarily blocked by YouTube. Use responsibly.

## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License.

## Links

- [GitHub Repository](https://github.com/SoAp9035/simple-yt-api)
- [PyPI Package](https://pypi.org/project/simple-yt-api/)
- [Buy Me a Coffee](https://buymeacoffee.com/soap9035/)