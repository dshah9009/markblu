from django.db.models import Value, Prefetch
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models_agent import PropertyVideo, ContactLog
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.core.cache import cache
from django.views.decorators.cache import cache_page

def user_filter_page(request):
    if request.method == "POST":
        city = request.POST.get("city", "")
        area = request.POST.get("area", "")
        property_type = request.POST.get("property_type", "")
        properties = request.POST.get("properties", "")
        budget = request.POST.get("budget", "")
        query = f"?city={city}&area={area}&property_type={property_type}&properties={properties}&budget={budget}"
        return redirect('/' + query)

    # Cache filter options for 1 hour
    cities = cache.get('filter_cities')
    if not cities:
        cities = list(PropertyVideo.objects.values_list('city', flat=True).distinct())
        cache.set('filter_cities', cities, 3600)
    
    areas = cache.get('filter_areas')
    if not areas:
        areas = list(PropertyVideo.objects.values_list('area', flat=True).distinct())
        cache.set('filter_areas', areas, 3600)
    
    properties_choices = PropertyVideo._meta.get_field('properties').choices
    budget_ranges = [
        ("0-1000000", "Below ₹10 Lakh"),
        ("1000000-3000000", "₹10 Lakh - ₹30 Lakh"),
        ("3000000-5000000", "₹30 Lakh - ₹50 Lakh"),
        ("5000000-10000000", "₹50 Lakh - ₹1 Cr"),
        ("10000000-", "Above ₹1 Cr"),
    ]

    return render(request, 'user/filter.html', {
        'cities': cities,
        'areas': areas,
        'properties_choices': properties_choices,
        'budget_ranges': budget_ranges
    })

def property_filter_view(request):
    # Cache distinct values for dropdowns (1 hour cache)
    cities = cache.get('property_cities')
    if not cities:
        cities = list(PropertyVideo.objects.values_list('city', flat=True).distinct())
        cache.set('property_cities', cities, 3600)
    
    areas = cache.get('property_areas')
    if not areas:
        areas = list(PropertyVideo.objects.values_list('area', flat=True).distinct())
        cache.set('property_areas', areas, 3600)
    
    property_types = cache.get('property_types')
    if not property_types:
        property_types = list(PropertyVideo.objects.values_list('property_type', flat=True).distinct())
        cache.set('property_types', property_types, 3600)
    
    if request.method == 'GET':
        city = request.GET.get('city')
        area = request.GET.get('area')
        price = request.GET.get('price')
        property_type = request.GET.get('property_type')
        properties = request.GET.get('properties')
        budget = request.GET.get('budget')
        page = request.GET.get('page', 1)
        
        filters = {}
        if city:
            filters["city"] = city
        if area:
            filters["area"] = area
        if price:
            filters["price"] = price
        if property_type:
            filters["property_type"] = property_type
        if properties:
            filters["properties"] = properties
        if budget:
            try:
                budget_value = int(budget) * 10000
                if budget_value > 0:
                    filters["price__lte"] = budget_value
            except:
                pass
        
        # Optimize query with select_related and only fetch needed fields for listing
        videos = PropertyVideo.objects.filter(**filters).select_related(
            'agent', 'agent__user'
        ).only(
            'id', 'city', 'area', 'price', 'property_type', 'properties',
            'video', 'uploaded_at', 'property_size_sqft', 'project_name',
            'agent__id', 'agent__company_name', 'agent__mobile', 'agent__user__first_name',
            'agent__user__last_name'
        ).order_by('-uploaded_at')
        
        no_results = False
        if not videos.exists() and property_type:
            no_results = True
        
        # Pagination - increased to 6 videos per page for better performance
        paginator = Paginator(videos, 6)
        page_obj = paginator.get_page(page)
        
        # Check if this is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            videos_html = render_to_string('user/video_items.html', {
                'videos': page_obj,
                'request': request,
                'user': request.user
            })
            return JsonResponse({
                'videos_html': videos_html,
                'has_more': page_obj.has_next(),
                'next_page': page_obj.next_page_number() if page_obj.has_next() else None
            })
        
        # Regular page load
        return render(request, "user/feed.html", {
            "videos": page_obj,
            "no_results": no_results,
            "has_more": page_obj.has_next(),
            "next_page": page_obj.next_page_number() if page_obj.has_next() else None,
        })

def user_register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        mobile = request.POST.get("mobile")

        if User.objects.filter(username=email).exists():
            return render(request, "user/register.html", {"error": "Email already registered"})

        user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
        UserProfile.objects.create(user=user, mobile=mobile)
        return redirect("user-login")

    return render(request, "user/register.html")

def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "filter")
            return redirect(next_url)
        else:
            if User.objects.filter(username=email).exists():
                return render(request, "user/login.html", {
                    "error": "Wrong password. Please try again."
                })
            else:
                return render(request, "user/login.html", {
                    "error": "Email not registered."
                })
    return render(request, "user/login.html")

@login_required
def log_call_and_redirect(request, video_id):
    video = get_object_or_404(
        PropertyVideo.objects.select_related('agent'), 
        id=video_id
    )
    ContactLog.objects.create(
        agent=video.agent,
        user=request.user,
        video=video,
        contact_type='Call',
        agent_mobile=video.agent.mobile,
        user_mobile=getattr(request.user.userprofile, 'mobile', '')
    )
    return render(request, 'user/call_redirect.html', {
        'agent_mobile': video.agent.mobile
    })

@login_required
def log_whatsapp_and_redirect(request, video_id):
    video = get_object_or_404(
        PropertyVideo.objects.select_related('agent'), 
        id=video_id
    )
    ContactLog.objects.create(
        agent=video.agent,
        user=request.user,
        video=video,
        contact_type='WhatsApp',
        agent_mobile=video.agent.mobile,
        user_mobile=getattr(request.user.userprofile, 'mobile', '')
    )
    mobile = video.agent.mobile
    city = video.city
    area = video.area
    message = f"Hi, I want to schedule a visit for the property in {area}, {city}"
    whatsapp_url = f"https://wa.me/91{mobile}?text={message.replace(' ', '%20')}"
    return redirect(whatsapp_url)

def detail_view(request, video_id):
    # Load the video with its agent
    video = get_object_or_404(PropertyVideo, pk=video_id)
    agent_videos = PropertyVideo.objects.filter(agent=video.agent).exclude(pk=video_id)

    # Capture the feed URL to return back
    from_url = request.GET.get('from', '/')

    return render(request, 'user/details.html', {
        'video': video,
        'agent': video.agent,
        'agent_videos': agent_videos,
        'from_url': from_url,
    })

# def detail_view(request, video_id):
#     video = get_object_or_404(
#         PropertyVideo.objects.select_related('agent', 'agent__user'), 
#         id=video_id
#     )
#     agent = video.agent
#     from_url = request.GET.get('from', reverse('feed'))
    
#     # Optimize agent videos query
#     agent_videos = PropertyVideo.objects.filter(
#         agent=agent
#     ).exclude(
#         id=video.id
#     ).select_related('agent').only(
#         'id', 'city', 'area', 'price', 'property_type', 
#         'video', 'property_size_sqft', 'project_name'
#     )[:6]  # Limit to 6 related videos
    
#     return render(request, 'user/details.html', {
#         'video': video,
#         'agent': agent,
#         'from_url': from_url,
#         'agent_videos': agent_videos
#     })

def custom_404(request, exception):
    return render(request, 'user/404.html', status=404)

from django.contrib.auth import login, get_user_model

User = get_user_model()

def mobile_login(request):
    if request.method == "POST":
        mobile = request.POST.get("mobile")
        if not mobile:
            return render(request, "user/mobile_login.html", {
                "error": "Please enter a mobile number."
            })

        # try to find user by mobile
        try:
            profile = UserProfile.objects.select_related('user').get(mobile=mobile)
            user = profile.user
        except UserProfile.DoesNotExist:
            # create user + profile if not found
            user = User.objects.create(username=mobile)
            profile = UserProfile.objects.create(user=user, mobile=mobile)

        # log them in
        login(request, user)
        next_url = request.GET.get("next", "filter")
        return redirect(next_url)

    return render(request, "user/login.html")

def user_filter_by_button(request, filter_type):
    """
    Handles quick filter buttons (Buy / Rent).
    Redirects to feed page with property_type applied.
    """
    if filter_type not in ["Buy", "Rent"]:
        return redirect("feed")

    return redirect(f"{reverse('feed')}?property_type={filter_type}")