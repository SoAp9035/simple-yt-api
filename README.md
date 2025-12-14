# Simple YouTube API

[![PyPI version](https://badge.fury.io/py/simple-yt-api.svg)](https://badge.fury.io/py/simple-yt-api) [![Downloads](https://pepy.tech/badge/simple-yt-api)](https://pepy.tech/project/simple-yt-api) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An unofficial lightweight Python wrapper for extracting video metadata and transcripts from YouTube videos.

## Features

- 🎥 Extract video metadata (title, thumbnail, short description)
- 📝 Get video transcripts in various languages
- ⚡ Simple and easy to use interface
- 🔒 No API key required

---

## Installation

[uv](https://docs.astral.sh/uv/) (a Python package and project manager) is recommended for managing and installing packages in isolated environments.

```bash
uv add simple-yt-api
```

You can also install it using pip:

```bash
pip install simple-yt-api
```

## Quick Start

```python
from simple_yt_api import YouTubeAPI

yt = YouTubeAPI()

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

metadata, transcript = yt.fetch_all(url_or_id=url)

print(f"Metadata: {metadata.to_dict()}")
print(f"Transcript: {transcript}")
```

###### Example Output:
```
Metadata: {
    'video_id': 'dQw4w9WgXcQ',
    'title': 'Rick Astley - Never Gonna Give You Up (Official Video) (4K Remaster)',
    'img_url': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',
    'short_description': 'The official video for “Never Gonna Give You Up” by Rick Astley. Never: The Autobiography 📚 OUT NOW! Follow this link to get your copy and listen to Rick’s ...'
}
Transcript: [
    {'text': '[♪♪♪]', 'start': 1.36, 'duration': 1.68},
    {'text': "♪ We're no strangers to love ♪", 'start': 18.64, 'duration': 3.24},
    ...
]
```

More examples can be found in the [examples](examples/) directory.

---

## API Reference

### `YouTubeAPI` Class

#### `YouTubeAPI()`
Initializes the API client.

#### `fetch_metadata(url_or_id: str) -> VideoMetadata`
Retrieves metadata for a specific video.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `url_or_id` | `str` | The URL or ID of the YouTube video. |

**Returns:** `VideoMetadata` object containing `video_id`, `title`, `img_url`, and `short_description`. Use `.to_dict()` to convert to a dictionary.

#### `fetch_transcript(url_or_id: str, language_code: str = "en", output_format: str = "json") -> list[dict] | str`
Retrieves the transcript for a specific video.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `url_or_id` | `str` | - | The URL or ID of the YouTube video. |
| `language_code` | `str` | `"en"` | The language code for the desired transcript. |
| `output_format` | `str` | `"json"` | Output format: `"json"` (list of dicts) or `"text"` (string). |

**Returns:** A list of dictionaries (JSON) or a plain string containing the transcript.

#### `fetch_all(url_or_id: str, language_code: str = "en", output_format: str = "json") -> tuple`
Convenience method to retrieve both metadata and transcript simultaneously.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `url_or_id` | `str` | - | The URL or ID of the YouTube video. |
| `language_code` | `str` | `"en"` | The language code for the desired transcript. |
| `output_format` | `str` | `"json"` | Output format: `"json"` (list of dicts) or `"text"` (string). |

**Returns:** A tuple `(metadata, transcript)`. If an error occurs for either part, that element will be `None`.

---

## Error Handling

The library includes custom exceptions:
- `YouTubeAPIError`: For YouTube API related errors.
- `IpBlocked`: When IP is blocked by YouTube.
- `RequestBlocked`: When request is blocked by YouTube.
- `NoVideoFound`: When a video is not accessible or doesn't exist.
- `NoMetadataFound`: When no metadata is found for the video.
- `TranscriptsDisabled`: When transcripts are not available for the video.
- `NoTranscriptFound`: When no transcript is available for the video.

---

## Limitations & gotchas

- Not all videos have transcripts available.
- Transcripts may not be available in all languages.
- Some videos only have auto-generated transcripts which may not be accurate.
- The library relies on web scraping techniques, which may break if YouTube changes its page structure.

---

## Warning

Sending too many requests in a short period might lead to your IP address being temporarily blocked by YouTube. Use responsibly.

---

## License

This project is licensed under the [MIT](LICENSE) License.

---

## Links

- [GitHub Repository](https://github.com/SoAp9035/simple-yt-api)
- [PyPI Package](https://pypi.org/project/simple-yt-api/)
- [Buy Me a Coffee](https://buymeacoffee.com/soap9035/)
- [Visit My Website](https://ahmetburhan.com/)
