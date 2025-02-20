from simple_yt_api import YouTubeAPI


youtube_link = "https://www.youtube.com/watch?v=BryspbM6s3E&list=PLQJij7idQLKxB0uXzHfiAgFP4OIPBiH5e"
data, transcript = YouTubeAPI(youtube_link).get_video_data_and_transcript()

print("Data:", data)
print("Video transcript:", transcript)
