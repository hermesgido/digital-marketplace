from datetime import datetime
from django.shortcuts import redirect, render
from youtube.form import UserInfoForm, YoutubeProductForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from youtube.models import UserInfo, YoutubeProduct

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
    channels = YoutubeProduct.objects.all()
    
    
    context = {'channels': channels}
    return render(request, 'index.html', context)


def product(request, id):
    channel = YoutubeProduct.objects.get(id=id)
    context = {'channel': channel}
    return render(request, 'product.html', context)

    
def parse_iso8601_timestamp(timestamp):
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None

    
@login_required
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
                thumbnail_default_url = channel_info['snippet']['thumbnails']['high']['url']
                print(f"channel_name:{channel_name}, channel_id:{channel_id}, channel_published_date:\
                    {channel_published_date}, channel_video_count:{channel_video_count}, \
                        channel_custom_url:{channel_custom_url}, thumbnail_default_url:{thumbnail_default_url}, \
                            channel_country:{channel_country}, channel_description:{channel_description}, \
                                channel_category:{channel_category}, subscribers:{subscribers},\
                                    total_views:{total_views}")
                
                print(f"Date: {channel_published_date}")
                # datetime_obj = datetime.strptime(channel_published_date, "%Y-%m-%dT%H:%M:%SZ")
                # formatted_date = datetime_obj.strftime("%Y-%m-%d")
                formatted_date = parse_iso8601_timestamp(channel_published_date)
                print(f"Date fom: {formatted_date}")
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
                    monetization = form.cleaned_data["monetization"],
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

@login_required
def edit_youtube_product(request, id):
    current_channel = YoutubeProduct.objects.get(id=id)
    form = YoutubeProductForm(instance = current_channel)
    if request.method == 'POST':
        form = YoutubeProductForm(request.POST, instance = current_channel)
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
                thumbnail_default_url = channel_info['snippet']['thumbnails']['high']['url']
                ##thumbnail_default_url = channel_info['snippet']['thumbnails']['default']['url'] 
                print(f"channel_name:{channel_name}, channel_id:{channel_id}, channel_published_date:\
                    {channel_published_date}, channel_video_count:{channel_video_count}, \
                        channel_custom_url:{channel_custom_url}, thumbnail_default_url:{thumbnail_default_url}, \
                            channel_country:{channel_country}, channel_description:{channel_description}, \
                                channel_category:{channel_category}, subscribers:{subscribers},\
                                    total_views:{total_views}")
                
                
                datetime_obj = datetime.strptime(channel_published_date, "%Y-%m-%dT%H:%M:%SZ")
                formatted_date = datetime_obj.strftime("%Y-%m-%d")
                print(formatted_date)
                
                current_channel.channel_id = channel_id
                current_channel.channel_name = channel_name
                current_channel.views = total_views
                current_channel.subscibers = subscribers
                current_channel.category = channel_category
                current_channel.description = channel_description
                current_channel.channel_country = channel_country
                current_channel.started_date = formatted_date
                current_channel.total_video_number = channel_video_count
                current_channel.channel_custom_url = channel_custom_url
                current_channel.thumbnail_default_url = thumbnail_default_url
                current_channel.your_description = form.cleaned_data["your_description"]
                current_channel.price = form.cleaned_data["price"]
                current_channel.revenue_per_month = form.cleaned_data["revenue_per_month"]
                current_channel.any_video_id = form.cleaned_data["any_video_id"]
                current_channel.monetization = form.cleaned_data["monetization"]
                current_channel.save()
                messages.success(request, "Channel updated successfully")
                return redirect(profile)
            else:
                print('Channel not found.')
                messages.error(request, "Channel not found enter valid video id")
                form = YoutubeProductForm()
                return redirect(add_product)
        else:
            form = YoutubeProductForm(instance = current_channel)
            messages.error(request, "Form not valid")
    context = {'form': form}    
    
    return render(request, 'edit_youtube_product.html', context)





@login_required
def profile(request):
    your_products = YoutubeProduct.objects.all()
    form = UserInfoForm(instance=request.user.userinfo)
    if request.method == 'POST':
        form = UserInfoForm(request.POST, instance=request.user.userinfo)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated successfully")
            return redirect(profile)
        else:
            messages.error(request, f"ERROR: {form.errors}")
            form = UserInfoForm(instance=request.user.userinfo)
        
    context = {'form': form, 'your_products':your_products}
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
            messages.error(request, "Invalid credentials")
            return redirect(login_view)
        messages.error(request, "Enter corect credentials")
        return redirect(login_view)
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone_number')
        if email is not None and password is not None and phone is not None:
            if User.objects.filter(username=email).exists():
                messages.success(request, "User already exists")
                return redirect(register_view)
            user = User.objects.create_user(username=email, password=password, email=email)
            user.save()
            user_info = UserInfo.objects.create(user=user, phone_number=phone, email=email)
            user_info.save()
            messages.success(request, "Successfully registered")
            return redirect(login_view)
        else:
            messages.error(request, "All fields are required")
    
    return render(request, 'register.html')


