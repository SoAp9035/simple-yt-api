import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter


class NotValidURL(Exception):
    def __init__(self, message: str="Not a valid Youtube URL"):
        self.message = message
        super().__init__(self.message)

class NoVideoFound(Exception):
    def __init__(self, message: str="No video found"):
        self.message = message
        super().__init__(self.message)

# class NoMetadataFound(Exception):
#     def __init__(self, message: str="No Metadata found"):
#         self.message = message
#         super().__init__(self.message)

class NoTranscriptFound(Exception):
    def __init__(self, message: str="No transcript found"):
        self.message = message
        super().__init__(self.message)


class YouTubeAPI:
    def __init__(self, url: str) -> None:
        self.user_agent = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        self.url = url
        if not self._url_check():
            raise NotValidURL

    def _url_check(self) -> bool:
        if self.url.startswith(("https://www.youtube.com/watch?v=", "https://youtu.be/")):
            return True
        else:
            return False

    def data(self) -> dict:
        """
        Returns video metadata.
                
        Returns:
            dict: Video metadata
        """
        response = requests.get(self.url, headers=self.user_agent)
        if response.status_code != 200:
            raise NoVideoFound
        
        youtube_html = response.text
        soup = BeautifulSoup(youtube_html, "html.parser")
        try:
            self._video_id = soup.find(name="meta", property="og:url").get("content")[32:]
            title = soup.find(name="meta", property="og:title").get("content")
            img_url = soup.find(name="meta", property="og:image").get("content")
            description = soup.find(name="meta", property="og:description").get("content")
        except Exception:
            raise NoVideoFound

        return {
            "video_id": self._video_id,
            "title": title,
            "img_url": img_url,
            "short_description": description
        }
    
    def get_transcript(self, languages: list = [], as_dict: bool = False) -> str | dict:
        """
        Returns the transcript found in languages.
        If no language is found, returns the transcript in any language.
        
        Args:
            languages (list): List of language codes to search for transcripts
            as_dict (bool): If True, returns transcript as dictionary, if False returns as plain text

        Returns:
            str|dict: Video transcript either as plain text (str) or as dictionary (dict)
        """
        self.data()
        language_codes = []
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(self._video_id)
            for transcript in transcript_list:
                language_codes.append(transcript.language_code)
            
            if not language_codes:
                raise NoTranscriptFound
            
            transcript = YouTubeTranscriptApi.get_transcript(self._video_id, languages=languages + ["en"] + language_codes)
            text_formatted_transcript = TextFormatter().format_transcript(transcript)
            if text_formatted_transcript:
                return text_formatted_transcript.replace("\n", " ") if not as_dict else transcript
            else:
                raise NoTranscriptFound
        except Exception:
            raise NoTranscriptFound

    def get_video_data_and_transcript(self, languages: list = [], as_dict: bool = False) -> tuple:
        """
        Returns both video metadata and transcript for a YouTube video in one call without worrying about errors.
        
        Args:
            languages (list): List of language codes to search for transcripts
            as_dict (bool): If True, returns transcript as dictionary, if False returns as plain text

        Returns:
            tuple:
                - data (dict): Video metadata, None if not found
                - transcript (str|dict): Video transcript if available, None if not found
        """
        try:
            yt = YouTubeAPI(self.url)
            data = yt.data()
            transcript = yt.get_transcript(languages=languages, as_dict=as_dict)
        except NoTranscriptFound as e:
            transcript = None
            print("Error:", e)
        except Exception as e:
            data = None
            transcript = None
            print("Error:", e)

        return data, transcript
