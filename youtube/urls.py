
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<str:id>/', views.product, name='product'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_youtube_product/<str:id>/', views.edit_youtube_product, name='edit_youtube_product'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),

]
