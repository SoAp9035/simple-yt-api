def is_valid_youtube_url(url: str) -> bool:
    """
    Check if the given URL is a valid YouTube video.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is a valid YouTube link, False otherwise.
    """
    if url.startswith((
        "https://youtu.be/",
        "https://www.youtube.com/watch?v=",
        "https://www.youtube.com/shorts/"
        )):
        return True
    else:
        return False
