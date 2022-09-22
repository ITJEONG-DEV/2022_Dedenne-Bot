from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

from util import parse_json

API_KEY = parse_json("../json/info.json")["youtube"]["api_key"]


def build_youtube_search():
    return build("youtube", "v3", developerKey=API_KEY)


def get_search_response(youtube, query):
    search_response = youtube.search().list(
        q=query,
        order="relevance",
        part="snippet",
        maxResults=10
    ).execute()

    return search_response


def get_video_info(search_response):
    result_json = []
    for i in range(10):
        item = search_response['items'][i]

        if item['id']['kind'] == 'youtube#video':
            result_json.append({
                "videoId": item['id']['videoId'],
                "title": item['snippet']['title'],
                # "description": item['snippet']['description'],
                "url": item['snippet']['thumbnails']['medium']['url']
            })

    return result_json

if __name__ == "__main__":
    query = "아이유"

    youtube = build_youtube_search()
    search_response = get_search_response(youtube, query)

    print(get_video_info(search_response))
