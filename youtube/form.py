from django import forms

from .models import *

class MainForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget_class = 'form-control'
            if isinstance(field.widget, forms.CheckboxInput):
                widget_class = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                widget_class = 'form-control form-small select'
            elif isinstance(field.widget, forms.Textarea) and isinstance(field, forms.CharField):
                field.widget.attrs['rows'] = 1
                field.widget.attrs['cols'] = 1
            field.widget.attrs['class'] = widget_class
            
class YoutubeProductForm(MainForm):
    class Meta:
        model = YoutubeProduct
        fields = ['any_video_id', 'your_description', 'revenue_per_month',  'monetization', 'price',]
        
class UserInfoForm(MainForm):
    class Meta:
        model = UserInfo
        exclude = ['user']


class ContactForm(MainForm):
    class Meta:
        model = Contact
        exclude = ['user', 'product']
        
class WebsiteProductForm(MainForm):
    class Meta:
        model = WebsiteProduct
        fields = ['domain', 'description', 'revenue_per_month',  'monetization', 'price',]
        
class InstagramAccountForm(MainForm):
    class Meta:
        model = InstagramAccount
        fields = ['username', 'description',  'price',]
        
        
class TikTokAccountAccountForm(MainForm):
    class Meta:
        model = TikTokAccount
        fields = ['username', 'description',  'price',]
        
class TwitterAccountAccountForm(MainForm):
    class Meta:
        model = TwitterAccount
        fields = ['username', 'description',  'price',]