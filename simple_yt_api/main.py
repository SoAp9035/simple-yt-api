import time
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api import _errors
from .exceptions import NoVideoFound, NoMetadataFound, TranscriptsDisabled, NoTranscriptFound
from .utils import transcript_list_to_text


class YouTubeAPI:
    """
    A simple API to fetch YouTube video metadata and transcripts.
    """
    def __init__(self) -> None:
        self._user_agent = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

    def data(self, url: str) -> dict:
        """
        Returns video metadata dictionary containing:
            - `video_id`: YouTube video ID
            - `title`: Video title
            - `img_url`: Thumbnail URL
            - `short_description`: Short video description
        
        Args:
            url (str): The URL of the YouTube video.
        
        Returns:
            dict: Video metadata

        Raises:
            NoVideoFound: No Video Found
            NoMetadataFound: No Metadata Found
        """
        response = requests.get(url, headers=self._user_agent, timeout=10)
        if response.status_code != 200:
            raise NoVideoFound
        
        youtube_html = response.text
        soup = BeautifulSoup(youtube_html, "html.parser")
        try:
            video_id = soup.find(name="meta", property="og:url").get("content")[32:]
            title = soup.find(name="meta", property="og:title").get("content")
            img_url = soup.find(name="meta", property="og:image").get("content")
            description = soup.find(name="meta", property="og:description").get("content")
        except Exception:
            raise NoMetadataFound

        data = {
            "video_id": video_id,
            "title": title,
            "img_url": img_url,
            "short_description": description
        }

        return data

    def get_transcript(self, url: str, language_code: str = "en", as_dict: bool = True) -> list[dict] | str:
        """
        Returns the transcript of the video in requested language.
        
        Args:
            url (str): The URL of the YouTube video.
            language_code (str, optional): The language code for the desired transcript. Defaults to "en".
            as_dict (bool, optional): If `True`, returns the transcript as a list of dictionaries;
                otherwise, returns the transcript as a string. Defaults to `True`.
        
        Returns:
            list[dict] | str: The transcript in the requested format (list of dictionaries or string).
        
        Raises:
            TranscriptsDisabled: Transcripts Disabled
            NoTranscriptFound: No Transcript Found
        """        
        try:
            data = self.data(url)
            time.sleep(1)

            video_id = data["video_id"]

            ytt_api = YouTubeTranscriptApi()
            transcript_list = ytt_api.list(video_id)
            transcript = transcript_list.find_transcript([language_code])
            transcript_dict_list = transcript.fetch().to_raw_data()
        except _errors.TranscriptsDisabled:
            raise TranscriptsDisabled
        except _errors.NoTranscriptFound:
            language_codes = [transcript.language_code for transcript in transcript_list]
            try:
                if "en" in language_codes:
                    transcript = transcript_list.find_transcript(["en"])
                else:
                    transcript = transcript_list.find_transcript([language_codes[0]])

                translated_transcript = transcript.translate(language_code)
                transcript_dict_list = translated_transcript.fetch().to_raw_data()
            except Exception:
                raise NoTranscriptFound
        except Exception:
            raise NoTranscriptFound

        return transcript_dict_list if as_dict else transcript_list_to_text(transcript_dict_list)
        
    def get_video_data_and_transcript(self, url: str, language_code: str = "en", as_dict: bool = True) -> tuple:
        """
        Returns both video metadata and transcript. If there is an error, that spot in the tuple will have `None` instead of a value.
        
        Args:
            url (str): The URL of the YouTube video.
            language_code (str, optional): The language code for the desired transcript. Defaults to "en".
            as_dict (bool, optional): If `True`, returns the transcript as a list of dictionaries; otherwise, returns the transcript as a string. Defaults to `True`.

        Returns:
            tuple:
                - data (dict): Video metadata, `None` if not found
                - transcript (list[dict] | str): Video transcript, `None` if not found
        """
        try:
            data = self.data(url)
            time.sleep(1)
            transcript = self.get_transcript(url=url, language_code=language_code, as_dict=as_dict)
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            transcript = None
            print("Warning! Simple YT API:", e)
        except Exception as e:
            data = None
            transcript = None
            print("Warning! Simple YT API:", e)

        return data, transcript
