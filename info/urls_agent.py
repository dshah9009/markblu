from django.urls import path
from .views_agent import agent_register,agent_login,agent_dashboard, upload_property, edit_video, delete_video, agent_logout

urlpatterns = [
    path('register/', agent_register, name = 'agent-register'),
    path('', agent_login, name = 'agent-login'),
    path('dashboard/', agent_dashboard, name = 'agent-dashboard'),
    path('upload/', upload_property, name='upload_property'),
    path('agent/video/<int:video_id>/edit/', edit_video, name='edit_video'),
    path('agent/video/<int:video_id>/delete/',delete_video, name='delete_video'),
    path('agent/logout/',agent_logout, name='agent-logout')
]