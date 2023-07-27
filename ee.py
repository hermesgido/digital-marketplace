from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

YOUTUBE_API_KEY = "AIzaSyA0ldDX0J6CYiiDxnyNjlKJo8qy2Z_s3lc"

def get_youtube_client():
    return build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_channel_info(channel_id):
    try:
        youtube = get_youtube_client()

        response = youtube.channels().list(
            part='snippet,statistics',
            id=channel_id
        ).execute()

        if 'items' in response and len(response['items']) > 0:
            return response['items'][0]
        else:
            return None

    except HttpError as e:
        print('An HTTP error occurred:\n', e)

def get_channel_category_name(channel_id):
    channel_info = get_channel_info(channel_id)
    if channel_info:
        category_id = channel_info['snippet'].get('categoryId', None)
        print(f"category id: {channel_id}")
        if category_id:
            youtube = get_youtube_client()

            response = youtube.videoCategories().list(
                part='snippet',
                id=category_id
            ).execute()

            if 'items' in response and len(response['items']) > 0:
                return response['items'][0]['snippet']['title']
    return None

# Example usage
if __name__ == '__main__':
    channel_id = 'UCfbWyw92wBVgA7vvdpL4Agg'
    category_name = get_channel_category_name(channel_id)
    if category_name:
        print('Channel Category Name:', category_name)
    else:
        print('Channel category not found or invalid channel ID.')
