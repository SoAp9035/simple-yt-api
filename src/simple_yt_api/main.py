import logging
import requests
from bs4 import BeautifulSoup
from .models import VideoMetadata
from .utils import extract_transcript_text
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled as YtTranscriptsDisabled,
    NoTranscriptFound as YtNoTranscriptFound,
    RequestBlocked as YtRequestBlocked,
    IpBlocked as YtIpBlocked,
)
from .exceptions import (
    YouTubeAPIError,
    IpBlocked,
    RequestBlocked,
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
            raise NoVideoFound()

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
            raise NoMetadataFound()

        return VideoMetadata(
            video_id=video_id,
            title=title,
            img_url=img_url,
            short_description=short_description,
        )

    def fetch_transcript(
        self, url_or_id: str, language_code: str = "en", output_format: str = "json"
    ) -> list[dict] | str:
        """
        Returns the transcript of the video in requested language.

        Args:
            url_or_id (str): The URL or ID of the YouTube video.
            language_code (str, optional): The language code for the desired transcript. Defaults to "en".
            output_format (str, optional): The format of the output. Can be "json" (list of dictionaries)
                or "text" (string). Defaults to "json".

        Returns:
            list[dict] | str: The transcript in the requested format.

        Raises:
            YouTubeAPIError: If the format is invalid or an API error occurs.
            IpBlocked: Ip Blocked
            RequestBlocked: Request Blocked
            TranscriptsDisabled: Transcripts Disabled
            NoTranscriptFound: No Transcript Found
        """
        if output_format not in ["json", "text"]:
            raise YouTubeAPIError(
                f"Invalid output format '{output_format}'. Use 'json' or 'text'."
            )

        try:
            video_id: str = self._extract_video_id(url_or_id)

            transcript_list = YouTubeTranscriptApi().list(video_id)
            transcript = transcript_list.find_transcript([language_code])
            transcript_items = transcript.fetch().to_raw_data()
        except YtTranscriptsDisabled:
            raise TranscriptsDisabled()
        except YtNoTranscriptFound:
            try:
                logging.warning(
                    "YouTubeAPI: Requested language not found; attempting translation."
                )
                available_langs = [t.language_code for t in transcript_list]
                if not available_langs:
                    raise NoTranscriptFound()

                source_lang = "en" if "en" in available_langs else available_langs[0]
                transcript = transcript_list.find_transcript([source_lang])

                translated_transcript = transcript.translate(language_code)
                transcript_items = translated_transcript.fetch().to_raw_data()
            except YtRequestBlocked:
                raise RequestBlocked()
            except YtIpBlocked:
                raise IpBlocked()
            except NoTranscriptFound:
                if not available_langs:
                    raise NoTranscriptFound()
                raise NoTranscriptFound(
                    f"The requested language is not available for this video. Available languages: {', '.join(available_langs)}"
                )
        except YtRequestBlocked:
            raise RequestBlocked()
        except YtIpBlocked:
            raise IpBlocked()
        except Exception as e:
            raise YouTubeAPIError(e)

        if format == "json":
            return transcript_items
        elif format == "text":
            return extract_transcript_text(transcript_items)

        return transcript_items

    def fetch_all(
        self, url_or_id: str, language_code: str = "en", output_format: str = "json"
    ) -> tuple[VideoMetadata | None, list[dict] | str | None]:
        """
        Returns both video metadata and transcript. If there is an error, that spot in the tuple will have `None` instead of a value.

        Args:
            url_or_id (str): The URL or ID of the YouTube video.
            language_code (str, optional): The language code for the desired transcript. Defaults to "en".
            output_format (str, optional): The format of the output. Can be "json" (list of dictionaries)
                or "text" (string). Defaults to "json".

        Returns:
            tuple:
                - data (VideoMetadata | None): Video metadata, `None` if not found
                - transcript (list[dict] | str | None): Video transcript, `None` if not found
        """
        data = None
        transcript = None
        try:
            data = self.fetch_metadata(url_or_id)
            transcript = self.fetch_transcript(
                url_or_id=url_or_id,
                language_code=language_code,
                output_format=output_format,
            )
        except (
            YouTubeAPIError,
            RequestBlocked,
            IpBlocked,
            TranscriptsDisabled,
            NoTranscriptFound,
        ) as e:
            transcript = None
            logging.warning(f"YouTubeAPI: {e}")
        except (NoVideoFound, NoMetadataFound) as e:
            data = None
            logging.warning(f"YouTubeAPI: {e}")
        except Exception as e:
            data = None
            transcript = None
            logging.warning(f"YouTubeAPI: {e}")

        return data, transcript
