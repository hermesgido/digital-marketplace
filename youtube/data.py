from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# YOUTUBE_API_KEY = "AIzaSyA0ldDX0J6CYiiDxnyNjlKJo8qy2Z_s3lc"


# def get_youtube_client():
#     return build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# def get_channel_id_from_video_id(video_id):
#     try:
#         response = youtube.videos().list(
#             part='snippet',
#             id=video_id
#         ).execute()
#         if 'items' in response and len(response['items']) > 0:
#             return response['items'][0]['snippet']['channelId']
#         else:
#             return None
#     except HttpError as e:
#         print('An HTTP error occurred:\n', e)


# def get_channel_statistics(youtube, channel_id):
#     try:
#         response = youtube.channels().list(
#             part='statistics,snippet',
#             id=channel_id
#         ).execute()
#         return response['items'][0]
#     except HttpError as e:
#         print('An HTTP error occurred:\n', e)
#     video_id = 'B2G6PppB6RI'
#     youtube = get_youtube_client()
#     channel_id = get_channel_id_from_video_id(video_id)    
#     if channel_id:
#         print('Channel ID:', channel_id)
#         channel_info = get_channel_statistics(youtube, channel_id)

#         # Extracting variables from channel_info dictionary
#         channel_snippet = channel_info['snippet']
#         channel_statistics = channel_info['statistics']

#         # Print the extracted variables
#         print('Channel Snippet:', channel_snippet)
#         print('Channel Statistics:', channel_statistics)
#     else:
#         print('Channel not found.')

# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

YOUTUBE_API_KEY = "AIzaSyA0ldDX0J6CYiiDxnyNjlKJo8qy2Z_s3lc"

def get_channel_info_from_video_id(video_id):
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

        response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        if 'items' in response and len(response['items']) > 0:
            channel_id = response['items'][0]['snippet']['channelId']
            channel_info = youtube.channels().list(
                part='snippet,statistics',
                id=channel_id
            ).execute()
            return channel_info['items'][0]
        else:
            return None

    except HttpError as e:
        print('An HTTP error occurred:\n', e)

# Example usage
video_id = 'B2G6PppB6RI'
channel_info = get_channel_info_from_video_id(video_id)
if channel_info:
    print('Channel ID:', channel_info['id'])
    print('Channel Snippet:', channel_info['snippet'])
    print('Channel Statistics:', channel_info['statistics'])
else:
    print('Channel not found.')
