from django.db.models import Value
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from .models_agent import PropertyVideo, ContactLog
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def user_filter_page(request):
    if request.method == "POST":
        city = request.POST.get("city", "")
        area = request.POST.get("area", "")
        # price_min = request.POST.get("price_min", "")
        # price_max = request.POST.get("price_max", "")
        property_type = request.POST.get("property_type", "")
        properties = request.POST.get("properties", "")
        budget = request.POST.get("budget", "")



        query = f"?city={city}&area={area}&property_type={property_type}&properties={properties}&budget={budget}"
        return redirect('/feed/' + query)

    # Get distinct values from uploaded videos
    cities = PropertyVideo.objects.values_list('city', flat=True).distinct()
    areas = PropertyVideo.objects.values_list('area', flat=True).distinct()
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
        'properties_choices' : properties_choices,
        'budget_ranges': budget_ranges
    })
 

def property_filter_view(request):
    # Get distinct values for dropdowns
    cities = PropertyVideo.objects.values_list('city', flat=True).distinct()
    areas = PropertyVideo.objects.values_list('area', flat=True).distinct()
    property_types = PropertyVideo.objects.values_list('property_type', flat=True).distinct()

    videos = PropertyVideo.objects.all()

    if request.method == 'GET':
        city = request.GET.get('city')
        area = request.GET.get('area')
        price = request.GET.get('price')
        property_type = request.GET.get('property_type')
        properties = request.GET.get('properties')
        budget = request.GET.get('budget')

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
            min_price, max_price = budget.split("-")
            if min_price:
                filters["price__gte"] = int(min_price)
            if max_price:
                filters["price__lte"] = int(max_price)
        except:
            pass

    videos = PropertyVideo.objects.filter(**filters).order_by('-uploaded_at')

    no_results = False
    if not videos.exists() and property_type:
        no_results = True
        videos = PropertyVideo.objects.filter(property_type=property_type).order_by('-uploaded_at')
    return render(request, "user/feed.html", {
        "videos": videos,
        "no_results": no_results,
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
    video = get_object_or_404(PropertyVideo, id=video_id)
    ContactLog.objects.create(
        agent=video.agent,
        user=request.user,
        video=video,
        contact_type='Call'
    )
    return render(request, 'user/call_redirect.html', {
        'agent_mobile': video.agent.mobile
    })



@login_required
def log_whatsapp_and_redirect(request, video_id):
    video = get_object_or_404(PropertyVideo, id=video_id)
    ContactLog.objects.create(
        agent=video.agent,
        user=request.user,
        video=video,
        contact_type='WhatsApp'
    )
    mobile = video.agent.mobile
    city = video.city
    area = video.area
    message = f"Hi, I want to schedule a visit for the property in {area}, {city}"
    whatsapp_url = f"https://wa.me/91{mobile}?text={message.replace(' ', '%20')}"
    return redirect(whatsapp_url)

def detail_view(request, video_id):
    video = get_object_or_404(PropertyVideo, id=video_id)
    agent = video.agent
    from_url = request.GET.get('from', reverse('feed'))  # fallback to feed if not provided
    agent_videos = PropertyVideo.objects.filter(agent=agent).exclude(id=video.id)
    return render(request, 'user/details.html', {
        'video': video,
        'agent': agent,
        'from_url': from_url,
        'agent_videos': agent_videos
    })

def custom_404(request, exception):
    return render(request, 'user/404.html', status=404)
