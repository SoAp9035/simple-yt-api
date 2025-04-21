class InvalidURL(Exception):
    """Custom exception for invalid YouTube URL format."""
    def __init__(self, message: str="Invalid YouTube URL format"):
        self.message = message
        super().__init__(self.message)

class NoVideoFound(Exception):
    """Custom exception when a video is not accessible or doesn't exist."""
    def __init__(self, message: str="Video is not accessible or doesn't exist"):
        self.message = message
        super().__init__(self.message)

class NoMetadataFound(Exception):
    """Custom exception when no metadata is found for the video."""
    def __init__(self, message: str="No metadata found for the video"):
        self.message = message
        super().__init__(self.message)

class TranscriptsDisabled(Exception):
    """Custom exception when transcripts are not available for the video."""
    def __init__(self, message: str="Transcripts are not available for the video"):
        self.message = message
        super().__init__(self.message)

class NoTranscriptFound(Exception):
    """Custom exception when no transcript is available for the video."""
    def __init__(self, message: str="No transcript available for the video"):
        self.message = message
        super().__init__(self.message)
