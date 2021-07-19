from django.conf import settings
import os
from django_cron import CronJobBase, Schedule
import requests
from requests.models import Response
from datetime import datetime, timedelta

from apiclient.discovery import build
import apiclient

from .models import Videos


class YoutubeApiRequest(CronJobBase):
    RUN_EVERY_MINS = 5  # runs after every 5 minutes
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "api.youtube_api_request"

    def do(self):
        def get_update_timestamp():
            return datetime.now() - timedelta(minutes=5)

        search_query = settings.BACKGROUND_UPDATE["search_query"]
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
                youtube = build("youtube", "v3", developerKey=api_key)
                request = youtube.search().list(
                    q=search_query,
                    part="snippet",
                    order="date",
                    maxResults=maxResults,
                    publishedAfter=(publishedAfter.replace(microsecond=0).isoformat() + "Z"),
                )
                response = request.execute()
                status = True
            except apiclient.errors.HttpError as err:
                error_code = err.resp.status
                if not (error_code == 400 or error_code == 403):
                    break

        if status:
            for item in response.json()["items"]:
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
