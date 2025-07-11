"""
URL configuration for markblu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from info import views as info_views  # ✅ Import views separately
import info.admin as info_admin   
urlpatterns = [
    path("admin/", admin.site.urls),
    path('agent/', include('info.urls_agent')),
    path('',include('info.urls')),
    path('admin-panel/contacts/', info_admin.admin_contact_logs, name='admin-contact-logs'),
    path('admin-panel/video/<int:video_id>/', info_admin.admin_video_details, name='admin-video-details'),

    
]


handler404 = 'info.views.custom_404'


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)