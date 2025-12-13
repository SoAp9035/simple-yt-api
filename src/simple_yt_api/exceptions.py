class YouTubeAPIError(Exception):
    """Custom exception for YouTubeAPI related errors."""

    def __init__(self, message: str = "YouTubeAPI error."):
        self.message = message
        super().__init__(self.message)


class IpBlocked(Exception):
    """Custom exception when IP blocked by YouTube."""

    def __init__(self, message: str = "YouTube has blocked your IP address."):
        self.message = message
        super().__init__(self.message)


class RequestBlocked(Exception):
    """Custom exception when request blocked by YouTube."""

    def __init__(self, message: str = "YouTube is blocking requests from your IP address."):
        self.message = message
        super().__init__(self.message)


class NoVideoFound(Exception):
    """Custom exception when a video is not accessible or doesn't exist."""

    def __init__(self, message: str = "Video is not accessible or does not exist."):
        self.message = message
        super().__init__(self.message)


class NoMetadataFound(Exception):
    """Custom exception when no metadata is found for the video."""

    def __init__(self, message: str = "No metadata found for this video."):
        self.message = message
        super().__init__(self.message)


class TranscriptsDisabled(Exception):
    """Custom exception when transcripts are not available for the video."""

    def __init__(self, message: str = "Transcripts are not available for this video."):
        self.message = message
        super().__init__(self.message)


class NoTranscriptFound(Exception):
    """Custom exception when the requested transcript is not available for the video."""

    def __init__(self, message: str = "The requested transcript is not available for this video."):
        self.message = message
        super().__init__(self.message)
