from django.contrib import admin
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import user_passes_test, login_required
from .models_agent import ContactLog, PropertyVideo

@user_passes_test(lambda u: u.is_staff or u.is_superuser)
@login_required
def admin_contact_logs(request):
    logs = ContactLog.objects.select_related('agent__user', 'user', 'video').prefetch_related('user__userprofile').order_by('-contact_datetime')
    return render(request, 'admin/contact_logs.html', {'logs': logs})

@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_video_details(request, video_id):
    video = get_object_or_404(PropertyVideo, id=video_id)
    return render(request, 'admin/video_details.html', {'video': video})
