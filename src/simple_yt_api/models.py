class VideoMetadata:
    """Youtube video metadata."""

    def __init__(
        self, video_id: str, title: str, img_url: str, description: str
    ) -> None:
        self.video_id: str = video_id
        self.title: str = title
        self.img_url: str = img_url
        self.description: str = description

    def to_dict(self) -> dict[str, str]:
        return {
            "video_id": self.video_id,
            "title": self.title,
            "img_url": self.img_url,
            "description": self.description,
        }
