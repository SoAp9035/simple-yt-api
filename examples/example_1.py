from simple_yt_api import YouTubeAPI


url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
yt = YouTubeAPI(url)

data, transcript = yt.get_video_data_and_transcript()
print("Data:", data)
print("Video transcript:", transcript)
