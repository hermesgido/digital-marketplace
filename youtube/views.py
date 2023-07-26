from datetime import datetime
from django.shortcuts import redirect, render
from youtube.form import YoutubeProductForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from youtube.models import UserInfo, YoutubeProduct

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





# Create your views here.
def home(request):
    return render(request, 'index.html')


def product(request):
    return render(request, 'product.html')

def add_product(request):
    form = YoutubeProductForm()
    if request.method == 'POST':
        form = YoutubeProductForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            video_id = form.cleaned_data['any_video_id']
            channel_info = get_channel_info_from_video_id(video_id)
            if channel_info:
                print('Channel ID:', channel_info['id'])
                print('Channel Snippet:', channel_info['snippet'])
                print('Channel Statistics:', channel_info['statistics'])
                # Extracting data from channel_info dictionary
                channel_name = channel_info['snippet']['title']
                channel_id = channel_info['id']
                total_views = channel_info['statistics']['viewCount']
                subscribers = channel_info['statistics']['subscriberCount']
                channel_category = channel_info['snippet'].get('categoryId', None)
                channel_description = channel_info['snippet'].get('description', None)
                channel_country = channel_info['snippet'].get('country', None)
                channel_published_date = channel_info['snippet'].get('publishedAt', None)
                channel_video_count = channel_info['statistics']['videoCount']
                channel_custom_url = channel_info['snippet'].get('customUrl', None)
                thumbnail_default_url = channel_info['snippet']['thumbnails']['default']['url']
                print(f"channel_name:{channel_name}, channel_id:{channel_id}, channel_published_date:\
                    {channel_published_date}, channel_video_count:{channel_video_count}, \
                        channel_custom_url:{channel_custom_url}, thumbnail_default_url:{thumbnail_default_url}, \
                            channel_country:{channel_country}, channel_description:{channel_description}, \
                                channel_category:{channel_category}, subscribers:{subscribers},\
                                    total_views:{total_views}")
                
                
                datetime_obj = datetime.strptime(channel_published_date, "%Y-%m-%dT%H:%M:%SZ")
                formatted_date = datetime_obj.strftime("%Y-%m-%d")
                print(formatted_date) 
                YoutubeProduct.objects.create(
                    channel_id=channel_id,
                    channel_name=channel_name,
                    views=total_views,
                    subscibers=subscribers,
                    category=channel_category,
                    description=channel_description,
                    channel_country=channel_country,
                    started_date=formatted_date,
                    total_video_number=channel_video_count,
                    channel_custom_url=channel_custom_url,
                    thumbnail_default_url=thumbnail_default_url,
                    your_description = form.cleaned_data["your_description"],
                    price = form.cleaned_data["price"],
                    revenue_per_month = form.cleaned_data["revenue_per_month"],
                    any_video_id = form.cleaned_data["any_video_id"],
                    monetization = form.cleaned_data["monetization"]
                    )
                
            else:
                print('Channel not found.')
                messages.error(request, "Channel not found enter valid video id")
                form = YoutubeProductForm()
                return redirect(add_product)
        else:
            form = YoutubeProductForm()
            messages.error(request, "Form not valid")
        
    context = {'form': form}
    return render(request, 'add_product.html', context)

def profile(request):
    form = YoutubeProductForm()
    if request.method == 'POST':
        form = YoutubeProductForm(request.POST)
        
        
    context = {'form': form}
    return render(request, 'profile.html', context)


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email is not None and password is not None:
            user = authenticate(username= email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in")
                return redirect(home)
            messages.error(request, "Enter corect credentials")
            return redirect(login_view)
        messages.error(request, "Enter corect credentials")
        return redirect(login_view)
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        if email is not None and password is not None and phone is not None:
            if User.objects.filter(username=email).exists():
                messages.success(request, "User already exists")
                return redirect(register_view)
            user = User.objects.create_user(username=email, password=password, email=email)
            user.save()
            user_info = UserInfo.objects.create(user=user)
            user_info.save()
            messages.error(request, "Successfully registered")
        return redirect(register_view)
    
    return render(request, 'register.html')


