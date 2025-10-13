from simple_yt_api import YouTubeAPI

# Initialize
yt = YouTubeAPI()

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Get video metadata
metadata = yt.data(url=url)
print(metadata["title"])

# Get video transcript
transcript = yt.get_transcript(
    url=url,
    language_code="tr",
    as_dict=True
) # Get Turkish transcript. Defaults to "en".
print(transcript)

# Or get both metadata and transcript at once
data, transcript = yt.get_video_data_and_transcript(
    url=url,
    language_code="es",
    as_dict=False  # Return transcript as plain text
)
