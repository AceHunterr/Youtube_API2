# Youtube Trending in Playlist : Enter playlist link and returns the top videos of that playlist

from googleapiclient.discovery import build
import re

api_key = "AIzaSyCSdtXwwN3yrfIl0gwle_yG8ifI-mlx25A"
youtube = build('youtube','v3', developerKey=api_key)


playlist_link = "https://youtube.com/playlist?list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS"
x = re.split("list=", playlist_link)
playlist_id = x[-1]


videos =[]


nextPageToken = None
while True:
    pl_request = youtube.playlistItems().list(
        part = 'contentDetails',
        playlistId = playlist_id,
        maxResults = 50,
        pageToken = nextPageToken
    )

    pl_response = pl_request.execute()

    vid_ids = []

    for item in pl_response['items']:
        vid_ids.append(item['contentDetails']['videoId'])

    vid_request = youtube.videos().list(
            part = "statistics",
            id= ','.join(vid_ids)
        )

    vid_response = vid_request.execute()

    for item in vid_response['items']:
        vid_views = item['statistics']['viewCount']

        vid_id = item['id']
        yt_link = f"https://youtu.be/{vid_id}"

        videos.append(
            {
                "views" : int(vid_views),
                "url" : yt_link
            }
        )



    nextPageToken = pl_response.get('nextPageToken')

    if not nextPageToken:
        break

videos.sort(key=lambda vid: vid['views'],reverse=True)

for video in videos[:10]:
    print(video['url'],video['views'])
