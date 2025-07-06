from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models_agent import AgentProfile, PropertyVideo, DealType
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .form_agent import PropertyVideoForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth import logout

def agent_register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("email")
        email = request.POST.get("email")
        password = request.POST.get("password")
        mobile = request.POST.get("mobile")
        company_name = request.POST.get("company_name")
        office_address = request.POST.get("office_address")
        project_location = request.POST.get("project_location")
        company_logo = request.FILES.get("company_logo")
        company_rera_id = request.POST.get("company_rera_id")
        experience = request.POST.get("experience")
        deal_ids = request.POST.getlist("deal")

        if User.objects.filter(email= email).exists():
            messages.error(request, "Email already registered")
            return redirect("agent-register")
        if not mobile.isdigit() or len(mobile) != 10:
            messages.error(request, "Mobile number must be at least 10 digits and contain only numbers.")
            return redirect("agent-register")
        
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,last_name=last_name)
        profile = AgentProfile.objects.create(
            user=user,
            mobile=mobile,
            company_name=company_name,
            office_address=office_address,
            project_location=project_location,
            company_logo=company_logo,
            company_rera_id=company_rera_id,
            experience = experience
        )
        profile.deal.set(deal_ids)
        messages.success(request, "Registration successful. Please login.")
        return redirect("agent-login")
    deal_types = DealType.objects.all()
    return render(request, "agent/register.html",{"deal_types": deal_types})

def agent_login(request):
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect("agent-dashboard")
        else:
            if User.objects.filter(username=username).exists():
                return render(request, "agent/login.html", {
                    "error": "Wrong password. Please try again."
                })
            else:
                return render(request, "agent/login.html", {
                    "error": "Email not registered."
                })
    return render(request, "agent/login.html")

@login_required
def agent_dashboard(request):
    agent = AgentProfile.objects.get(user=request.user)
    video_count = PropertyVideo.objects.filter(agent=agent).count()
    videos = PropertyVideo.objects.filter(agent=agent).order_by('-uploaded_at')  # latest first

    return render(request, 'agent/dashboard.html', {
        'agent': agent,
        'video_count': video_count,
        'videos': videos
    })


@login_required
def upload_property(request):
    agent_profile = AgentProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = PropertyVideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.agent = agent_profile  # ✅ updated field
            video.save()
            return redirect('agent-dashboard')
    else:
        form = PropertyVideoForm()

    return render(request, 'agent/upload_property.html', {'form': form})


@login_required
def edit_video(request, video_id):
    video = get_object_or_404(PropertyVideo, id=video_id, agent__user=request.user)

    if request.method == 'POST':
        form = PropertyVideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated successfully.")
            return redirect('agent-dashboard')
    else:
        form = PropertyVideoForm(instance=video)

    return render(request, 'agent/edit_property.html', {'form': form})


@login_required
def delete_video(request, video_id):
    video = get_object_or_404(PropertyVideo, id=video_id, agent__user=request.user)
    video.delete()
    messages.success(request, "Property deleted successfully.")
    return redirect('agent-dashboard')

def agent_logout(request):
    logout(request)
    return redirect('agent-login')
