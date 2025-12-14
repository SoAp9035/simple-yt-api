from simple_yt_api import YouTubeAPI

yt = YouTubeAPI()

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

metadata, transcript = yt.fetch_all(url_or_id=url)

print(f"Metadata: {metadata.to_dict()}")
print(f"Transcript: {transcript}")
