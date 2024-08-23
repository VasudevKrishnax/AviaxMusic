import asyncio
import re
from typing import Union
import aiohttp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from AashikaMusic.utils.formatters import time_to_seconds

FASTAPI_URL = 'http://157.230.5.237:8000/'

async def fetch_from_api(endpoint: str, data: dict = None) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{FASTAPI_URL}/{endpoint}', json=data) as response:
            return await response.json()

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.tbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if re.search(self.regex, link):
            return True
        else:
            return False

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        text = ""
        offset = None
        length = None
        for message in messages:
            if offset:
                break
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        if offset in (None,):
            return None
        return text[offset : offset + length]

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        if "?si=" in link:
            link = link.split("?si=")[0]
        response = await fetch_from_api('fetch', {'url': link})
        title = response.get('title', 'Unknown Title')
        duration_min = response.get('duration', '0')
        thumbnail = response.get('thumbnail', 'No Thumbnail')
        vidid = response.get('id', '')
        duration_sec = int(time_to_seconds(duration_min)) if duration_min != 'None' else 0
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        if "?si=" in link:
            link = link.split("?si=")[0]
        response = await fetch_from_api('fetch', {'url': link})
        title = response.get('title', 'Unknown Title')
        return title

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        if "?si=" in link:
            link = link.split("?si=")[0]
        response = await fetch_from_api('fetch', {'url': link})
        duration = response.get('duration', '0')
        return duration

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        if "?si=" in link:
            link = link.split("?si=")[0]
        response = await fetch_from_api('fetch', {'url': link})
        thumbnail = response.get('thumbnail', 'No Thumbnail')
        return thumbnail

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        if "?si=" in link:
            link = link.split("?si=")[0]
        response = await fetch_from_api('download', {'url': link, 'video': True})
        file_path = response.get('file_path', '')
        return file_path if file_path else (0, 'Error')

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        if "?si=" in link:
            link = link.split("?si=")[0]
        response = await fetch_from_api('playlist', {'url': link, 'limit': limit})
        return response.get('playlist', [])

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        if "?si=" in link:
            link = link.split("?si=")[0]
        response = await fetch_from_api('track', {'url': link})
        title = response.get('title', 'Unknown Title')
        duration_min = response.get('duration', '0')
        vidid = response.get('id', '')
        yturl = response.get('link', '')
        thumbnail = response.get('thumbnail', 'No Thumbnail')
        track_details = {
            "title": title,
            "link": yturl,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail,
        }
        return track_details, vidid

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        if "?si=" in link:
            link = link.split("?si=")[0]
        response = await fetch_from_api('formats', {'url': link})
        formats_available = response.get('formats', [])
        return formats_available, link

    async def slider(
        self,
        link: str,
        query_type: int,
        videoid: Union[bool, str] = None,
    ):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        if "?si=" in link:
            link = link.split("?si=")[0]
        response = await fetch_from_api('slider', {'url': link})
        result = response.get('result', [])
        if len(result) > query_type:
            item = result[query_type]
            title = item.get('title', 'Unknown Title')
            duration_min = item.get('duration', '0')
            vidid = item.get('id', '')
            thumbnail = item.get('thumbnail', 'No Thumbnail')
            return title, duration_min, thumbnail, vidid
        return '', '', '', ''

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> str:
        if videoid:
            link = self.base + link
        response = await fetch_from_api('download', {'url': link, 'video': video, 'songaudio': songaudio, 'songvideo': songvideo, 'format_id': format_id, 'title': title})
        file_path = response.get('file_path', '')
        return file_path
