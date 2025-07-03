from django.urls import path
from .views import user_filter_page, property_filter_view,user_login,user_register,schedule_whatsapp_redirect, detail_view

urlpatterns = [
    path('', user_filter_page, name='filter'),
    path('feed/',property_filter_view, name='feed'),
    path('login/',user_login, name= 'user-login'),
    path('registeration/',user_register, name='register'),
    path("schedule/<int:video_id>/whatsapp/", schedule_whatsapp_redirect, name="schedule_whatsapp"),
    path('video/<int:video_id>/', detail_view, name='details'),


]