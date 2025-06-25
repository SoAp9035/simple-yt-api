from simple_yt_api import YouTubeAPI


yt = YouTubeAPI()

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
data, transcript = yt.get_video_data_and_transcript(url=url)

print("Data:", data)
print("Video transcript:", transcript)
