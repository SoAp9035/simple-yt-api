from simple_yt_api import YouTubeAPI


def main():
    yt = YouTubeAPI()

    # A TED Talk video (usually has good captions)
    url = "https://www.youtube.com/watch?v=8jPQjjsBbIc"

    metadata = yt.fetch_metadata(url)
    print(f"Fetching transcript for '{metadata.title}' video.")

    transcript_text = yt.fetch_transcript(url, output_format="text")

    print("\n--- Transcript Start ---\n")
    # Print first 500 characters to avoid cluttering the console
    print(transcript_text[:500] + "...")
    print("\n--- Transcript End ---")


if __name__ == "__main__":
    main()
