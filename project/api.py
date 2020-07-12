import os
from datetime import timedelta 
from googleapiclient.discovery import build
import re
api_key='PLACE YOUR GOOGLE API KEY'

youtube=build('youtube','v3',developerKey=api_key)

hours_pattern=re.compile(r'(\d+)H')
minutes_pattern=re.compile(r'(\d+)M')
seconds_pattern=re.compile(r'(\d+)S')

nextPageToken=None 
total_seconds=0
while True:
    pl_request=youtube.playlistItems().list(
        part='contentDetails',
        playlistId='PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH',
        maxResults=50,
        pageToken=nextPageToken

    )
    pl_response=pl_request.execute()

    vid_ids=[]
    for item in pl_response['items']:
        vid_ids.append(item['contentDetails']['videoId'])
        
    vid_request=youtube.videos().list(
        part="contentDetails",
        id=','.join(vid_ids) 
    )
    vid_response = vid_request.execute()

    for item in vid_response['items']:
        duration=item['contentDetails'] ['duration']

        hours=hours_pattern.search(duration)
        minutes=minutes_pattern.search(duration)
        seconds=seconds_pattern.search(duration)

        hours=int(hours.group(1)) if hours else 0
        minutes=int(minutes.group(1)) if minutes else 0
        seconds=int(seconds.group(1)) if seconds else 0

        video_seconds=timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds 
        ).total_seconds()

        total_seconds+=video_seconds
    nextPageToken=pl_response.get('nextPageToken')

    if not nextPageToken:
        break 

total_seconds=int(total_seconds)

def convert(seconds): 
    min, sec = divmod(seconds, 60) 
    hour, min = divmod(min, 60) 
    return "%d:%02d:%02d" % (hour, min, sec) 
      
print(convert(total_seconds))
