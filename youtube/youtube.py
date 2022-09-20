from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

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

        return search_response



    def __get_video_info(self, search_response):
        result = []

        for i in range(10):
            item = search_response["items"][i]

            if item["id"]["kind"] == "youtube#video":
                result.append({
                    "id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "url": item["thumbnails"]["default"]["url"]
                })

        return result