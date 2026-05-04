"""A simple and easy-to-use unofficial YouTube API Wrapper."""

from .main import YouTubeAPI
from .models import VideoMetadata
from .exceptions import (
    YouTubeAPIError,
    IpBlocked,
    RequestBlocked,
    NoVideoFound,
    NoMetadataFound,
    TranscriptsDisabled,
    NoTranscriptFound,
)
