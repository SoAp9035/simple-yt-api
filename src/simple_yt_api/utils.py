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
    return transcript_text.replace("  ", " ").strip()
