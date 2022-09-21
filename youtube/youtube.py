import json

import asyncio

import discord

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import urllib

import youtube_dl

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ffmpeg_executable_url = "D:/ffmpeg-5.1.1-full_build/bin/ffmpeg.exe"

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options, executable=ffmpeg_executable_url), data=data)


class YoutubeHandler:
    def __init__(self, API_KEY):
        self.youtube = build("youtube", "v3", developerKey=API_KEY)

    def get_search_result(self, keyword):
        search_response = self.youtube.search().list(
            q=keyword,
            order="relevance",
            part="snippet",
            maxResults=10
        ).execute()

        return self.__get_video_info(search_response)

    def get_video_info(self, url):
        params = {
            "format": "json",
            "url": url
        }

        oembed_url = "https://www.youtube.com/oembed"
        query = urllib.parse.urlencode(params)
        oembed_url += "?" + query

        try:
            with urllib.request.urlopen(oembed_url) as response:
                response_text = response.read()
                item = json.loads(response_text.decode('utf-8'))

                return {
                    "id": url.split("=")[1],
                    "title": item["title"],
                    "url": item['thumbnail_url']
                }
        except Exception as e:
            print(e)
            return {
                "error": e
            }

    @staticmethod
    def __get_video_info(search_response):
        result = []

        for i in range(10):
            item = search_response["items"][i]

            if item["id"]["kind"] == "youtube#video":
                result.append({
                    "id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "url": item["snippet"]["thumbnails"]["high"]["url"]
                })

        return result
