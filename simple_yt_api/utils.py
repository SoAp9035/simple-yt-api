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
        "https://youtube.com/watch?v=",
        "https://www.youtube.com/watch?v=",
        "https://youtube.com/shorts/",
        "https://www.youtube.com/shorts/"
        )):
        return True
    else:
        return False

def transcript_list_to_text(transcript_dict_list: list[dict]) -> str:
    """
    Convert a list of transcript dictionaries to a single text string.

    Args:
        transcript_dict_list (list[dict]): List of dictionaries, each containing a "text" key.

    Returns:
        str: Linked transcript text.
    """
    transcript_text = ""
    for tct in transcript_dict_list:
        transcript_text += " " + tct["text"]
    return transcript_text.replace("  ", " ")
