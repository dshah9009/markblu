from django.db.models import Value
from django.shortcuts import redirect, render, get_object_or_404
from .models_agent import PropertyVideo
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



        query = f"?city={city}&area={area}&property_type={property_type}&properties={properties}"
        return redirect('/feed/' + query)

    # Get distinct values from uploaded videos
    cities = PropertyVideo.objects.values_list('city', flat=True).distinct()
    areas = PropertyVideo.objects.values_list('area', flat=True).distinct()
    properties_choices = PropertyVideo._meta.get_field('properties').choices



    return render(request, 'user/filter.html', {
        'cities': cities,
        'areas': areas,
        'properties_choices' : properties_choices
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
        #min_price = request.GET.get('min_price')
        #max_price = request.GET.get('max_price')
        price = request.GET.get('price')
        property_type = request.GET.get('property_type')
        properties = request.GET.get('properties')

    filters = {}
    if city:
        filters["city"] = city
    if area:
        filters["area"] = area
    if price:
        filters["price"] = price
    # if min_price:
    #     filters["price_min__gte"] = min_price
    # if max_price:
    #     filters["price_max__lte"] = max_price
    if property_type:
        filters["property_type"] = property_type
    if properties:
        filters["properties"] = properties

    videos = PropertyVideo.objects.filter(**filters)

    no_results = False
    if not videos.exists() and property_type:
        no_results = True
        videos = PropertyVideo.objects.filter(property_type=property_type)

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

def schedule_whatsapp_redirect(request, video_id):
    if not request.user.is_authenticated:
        return redirect(f"{reverse('user-login')}?next={request.path}")

    video = get_object_or_404(PropertyVideo, id=video_id)
    area = video.area
    city = video.city
    mobile = video.agent.mobile
    full_number = f"91{mobile}"
    message = f"Hi, I want to schedule a visit for the property in {area}, {city}"
    whatsapp_url = f"https://wa.me/{full_number}?text={message.replace(' ', '%20')}"

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
