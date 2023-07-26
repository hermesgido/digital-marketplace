from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    
    
class YoutubeProduct(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    channel_name = models.CharField(max_length=200, blank=True, null=True)
    any_video_id = models.CharField(max_length=200, blank=True, null=True)
    channel_id = models.CharField(max_length=200, blank=True, null=True)
    subscibers = models.PositiveIntegerField(null=True, blank=True)
    views = models.PositiveIntegerField(null=True, blank=True)
    started_date = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    channel_country = models.CharField(max_length=200, blank=True, null=True)
    your_description = models.TextField(max_length=200, blank=True, null=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    revenue_per_month = models.PositiveIntegerField(null=True, blank=True)
    total_video_number = models.PositiveIntegerField(null=True, blank=True)
    channel_custom_url = models.CharField(max_length=200, blank=True, null=True)
    thumbnail_default_url = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    ch = (("Adsence", "Adsence"), ("No Monetization", "No Monetization"),("Affiliation", "Affiliation"),)
    monetization = models.CharField(max_length=200, blank=True, null=True, choices=ch, default="No Monetization")
    post_views = models.PositiveIntegerField(null=True, blank=True)
    ch = (("Pending", "Pending"), ("Approved", "Approved"),("Sold", "Sold"),)
    status = models.CharField(max_length=200, blank=True, null=True, choices=ch, default="Pending")
    
    