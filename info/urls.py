from django.urls import path
from .views import user_filter_page, property_filter_view,user_login,user_register,log_whatsapp_and_redirect, detail_view,log_call_and_redirect
from django.contrib import admin

urlpatterns = [
    path('', user_filter_page, name='filter'),
    path('feed/',property_filter_view, name='feed'),
    path('login/',user_login, name= 'user-login'),
    path('registeration/',user_register, name='register'),
    path('video/<int:video_id>/', detail_view, name='details'),
    
    path('contact-call/<int:video_id>/', log_call_and_redirect, name='log-call'),
    path('contact-whatsapp/<int:video_id>/', log_whatsapp_and_redirect, name='log-whatsapp'),
    
   
]