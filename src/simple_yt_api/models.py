class VideoMetadata:
    """Youtube video metadata."""

    def __init__(
        self, video_id: int, title: str, img_url: str, short_description: str
    ) -> None:
        self.video_id = video_id
        self.title = title
        self.img_url = img_url
        self.short_description = short_description

    def to_dict(self) -> dict[str, any]:
        return {
            "video_id": self.video_id,
            "title": self.title,
            "img_url": self.img_url,
            "short_description": self.short_description,
        }
