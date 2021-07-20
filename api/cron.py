from django.conf import settings
import os
from django_cron import CronJobBase, Schedule
import requests
from requests.models import Response
from datetime import datetime, timedelta

# Client library for Google's discovery based APIs
# Constructs a Resource object for interacting with the Google APIs.
from apiclient.discovery import build
import apiclient

from .models import Videos


# CronJob to call the YouTube API request every 5 mins
class YoutubeApiRequest(CronJobBase):
    RUN_EVERY_MINS = 5  # runs after every 5 minutes
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "api.youtube_api_request"

    def do(self):
        def get_update_timestamp():
            # Returns a timestamp for 5 mins ago
            return datetime.now() - timedelta(minutes=5)

        # See : https://github.com/youtube/api-samples/blob/master/python/search.py
        YOUTUBE_API_SERVICE_NAME = 'youtube'
        YOUTUBE_API_VERSION = 'v3'
        search_query = settings.BACKGROUND_UPDATE["search_query1"]
        API_KEYS = settings.API_KEY
        maxResults = 25
        publishedAfter = get_update_timestamp()
        status = False

        for api_key in API_KEYS:
            # Alternatively, this can be used
            # request = get_request(
            #    api_key=api_key,
            #    part="snippet",
            #    maxResults=maxResults,
            #    search_query=search_query,
            #    order="date",
            #    publishedAfter=publishedAfter,
            # )
            # status = True
            # error_code = request.status_code
            # if not (error_code == 400 or error_code == 403):
            # break

            try:
                youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key)
                # search.list method to retrieve results matching the specified keyword.
                request = youtube.search().list(
                    q=search_query,
                    part="snippet",
                    order="date",
                    maxResults=maxResults,
                    publishedAfter=(publishedAfter.replace(microsecond=0).isoformat() + "Z"),
                )
                response = request.execute()
                # To create an entry in db for a valid api_key
                status = True
            except apiclient.errors.HttpError as err:
                error_code = err.resp.status
                # Changes API KEY if error_code is 400 or 403
                if not (error_code == 400 or error_code == 403):
                    break

        if status:
            for item in response["items"]:
                try:
                    Videos.objects.create(
                        video_id=item["id"]["videoId"],
                        title=item["snippet"]["title"],
                        description=item["snippet"]["description"],
                        published_at=item["snippet"]["publishedAt"],
                        thumbnail_url=item["snippet"]["thumbnails"]["default"]["url"],
                        channel_title=item["snippet"]["channelTitle"],
                        channel_id=item["snippet"]["channelId"],
                    )
                except Exception as e:
                    print(e)
                    continue


# Another way for GET Request
def get_request(
    api_key: str, part: str, order: str, search_query: str, maxResults: int, publishedAfter: str
) -> Response:
    url = (
        f"https://youtube.googleapis.com/youtube/v3/search?"
        f"part={part}&"
        f"maxResults={maxResults}&"
        f"order={order}&"
        f"publishedAfter={publishedAfter}&"
        f"q={search_query}&"
        f"key={api_key}"
    )

    return requests.get(url=url)
