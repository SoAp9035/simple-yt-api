import logging
import requests
from bs4 import BeautifulSoup
from .models import VideoMetadata
from .utils import transcript_list_to_text
from youtube_transcript_api import _errors
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from .exceptions import (
    YouTubeAPIError,
    NoVideoFound,
    NoMetadataFound,
    TranscriptsDisabled,
    NoTranscriptFound,
)


class YouTubeAPI:
    """
    A simple API to fetch YouTube video metadata and transcripts.
    """

    def __init__(self) -> None:
        self._user_agent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    def _extract_video_id(self, url_or_id: str) -> str:
        """Returns video id."""
        if not any(x in url_or_id for x in ["://", "youtube.com", "youtu.be"]):
            return url_or_id

        if not url_or_id.startswith(("http://", "https://")):
            url_or_id = "https://" + url_or_id

        result = urlparse(url_or_id)

        params = parse_qs(result.query)
        if "v" in params and params["v"]:
            return params["v"][0]

        path = result.path.strip("/")

        # Shorts, embed, and live
        if any(x in path for x in ["shorts/", "embed/", "live/"]):
            return path.split("/")[-1]

        # Shortened link
        if "youtu.be" in result.hostname:
            return path.split("/")[0]

        raise NoVideoFound("Couldn't extract video id.")

    def fetch_metadata(self, url_or_id: str) -> VideoMetadata:
        """
        Returns a VideoMetadata instance containing:
            - `video_id`: YouTube video ID
            - `title`: Video title
            - `img_url`: Thumbnail URL
            - `short_description`: Short video description

        Args:
            url_or_id (str): The URL or ID of the YouTube video.

        Returns:
            VideoMetadata: Video metadata object

        Raises:
            NoVideoFound: No Video Found
            NoMetadataFound: No Metadata Found
        """
        url: str = url_or_id
        if not any(x in url_or_id for x in ["://", "youtube.com", "youtu.be"]):
            url = f"https://youtu.be/{url_or_id}"

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        response = requests.get(url, headers=self._user_agent, timeout=10)
        if response.status_code != 200:
            raise NoVideoFound

        youtube_html = response.text
        soup = BeautifulSoup(youtube_html, "html.parser")

        video_id: str = self._extract_video_id(url_or_id)
        try:
            title: str = soup.find(name="meta", property="og:title").get("content")
            img_url: str = soup.find(name="meta", property="og:image").get("content")
            short_description: str = soup.find(
                name="meta", property="og:description"
            ).get("content")
        except Exception:
            raise NoMetadataFound

        return VideoMetadata(
            video_id=video_id,
            title=title,
            img_url=img_url,
            short_description=short_description,
        )

    def fetch_transcript(
        self, url_or_id: str, language_code: str = "en", as_dict: bool = True
    ) -> list[dict] | str:
        """
        Returns the transcript of the video in requested language.

        Args:
            url_or_id (str): The URL or ID of the YouTube video.
            language_code (str, optional): The language code for the desired transcript. Defaults to "en".
            as_dict (bool, optional): If `True`, returns the transcript as a list of dictionaries;
                otherwise, returns the transcript as a string. Defaults to `True`.

        Returns:
            list[dict] | str: The transcript in the requested format (list of dictionaries or string).

        Raises:
            YouTubeAPIError: Youtube API Error
            TranscriptsDisabled: Transcripts Disabled
            NoTranscriptFound: No Transcript Found
        """
        try:
            video_id: str = self._extract_video_id(url_or_id)

            ytt_api = YouTubeTranscriptApi()
            transcript_list = ytt_api.list(video_id)
            transcript = transcript_list.find_transcript([language_code])
            transcript_dict_list = transcript.fetch().to_raw_data()
        except _errors.TranscriptsDisabled:
            raise TranscriptsDisabled
        except _errors.NoTranscriptFound:
            try:
                language_codes = [
                    transcript.language_code for transcript in transcript_list
                ]
                if "en" in language_codes:
                    transcript = transcript_list.find_transcript(["en"])
                else:
                    transcript = transcript_list.find_transcript([language_codes[0]])

                translated_transcript = transcript.translate(language_code)
                transcript_dict_list = translated_transcript.fetch().to_raw_data()
            except Exception:
                raise NoTranscriptFound
        except Exception:
            raise YouTubeAPIError

        return (
            transcript_dict_list
            if as_dict
            else transcript_list_to_text(transcript_dict_list)
        )

    def fetch_all(
        self, url_or_id: str, language_code: str = "en", as_dict: bool = True
    ) -> tuple[VideoMetadata | None, list[dict] | str | None]:
        """
        Returns both video metadata and transcript. If there is an error, that spot in the tuple will have `None` instead of a value.

        Args:
            url_or_id (str): The URL or ID of the YouTube video.
            language_code (str, optional): The language code for the desired transcript. Defaults to "en".
            as_dict (bool, optional): If `True`, returns the transcript as a list of dictionaries; otherwise, returns the transcript as a string. Defaults to `True`.

        Returns:
            tuple:
                - data (VideoMetadata | None): Video metadata, `None` if not found
                - transcript (list[dict] | str | None): Video transcript, `None` if not found
        """
        try:
            data = self.fetch_metadata(url_or_id)
            transcript = self.fetch_transcript(
                url_or_id=url_or_id, language_code=language_code, as_dict=as_dict
            )
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            transcript = None
            logging.warning(f"Simple YT API: {e}")
        except Exception as e:
            data = None
            transcript = None
            logging.warning(f"Simple YT API: {e}")

        return data, transcript
