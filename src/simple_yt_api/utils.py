def extract_transcript_text(transcript_items: list[dict]) -> str:
    """
    Convert a list of transcript dictionaries to a single text string.

    Args:
        transcript_items (list[dict]): List of dictionaries, each containing a "text" key.

    Returns:
        str: Concatenated transcript text.
    """
    return " ".join(tct["text"] for tct in transcript_items).replace("  ", " ").strip()
