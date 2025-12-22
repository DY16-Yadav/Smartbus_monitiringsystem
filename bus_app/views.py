from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import BusData
import json
from datetime import timedelta

def home(request):
    return render(request, "accounts/home.html")


def register(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=email).exists():
            messages.error(request, "User already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=email,      
            email=email,
            password=password,
            first_name=firstname,
            last_name=lastname
        )

       
        auth_login(request, user)

        messages.success(request, "Registration successful")
        return redirect("dashboard")   

    return render(request, "accounts/register.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid email or password")
            return redirect("login")

    return render(request, "accounts/login.html")

@login_required(login_url='login')
def dashboard(request):
    return render(request, "accounts/dashboard.html")



@csrf_exempt
def receive_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            latitude = data.get("latitude")
            longitude = data.get("longitude")
            speed = data.get("speed")
            temperature = data.get("temperature")
            fuel_percent = data.get("fuel_percent")

            # TANK_HEIGHT = 30
            # fuel_percent = None
            # if fuel_percent is not None:
            #     fuel_height = max(TANK_HEIGHT - float(fuel_percent), 0)
            #     fuel_percent = (fuel_height / TANK_HEIGHT) * 100

            BusData.objects.create(
                latitude=latitude,
                longitude=longitude,
                speed=speed,
                temperature=temperature,
                fuel_percent=fuel_percent,
                fuel_level=fuel_percent,
            )

            return JsonResponse({
                "message": "Data saved successfully",
                "fuel_percent": fuel_percent
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=405)


def get_data(request):
    latest = BusData.objects.last()
    if not latest:
        return JsonResponse({"message": "No data found"})

    return JsonResponse({
        "timestamp": latest.timestamp,
        "latitude": latest.latitude,
        "longitude": latest.longitude,
        "speed": latest.speed,
        "temperature": latest.temperature,
        "fuel_percent": latest.fuel_percent,
    })


def history_latest(request):
    time_limit = timezone.now() - timedelta(hours=2)
    records = BusData.objects.filter(timestamp__gte=time_limit)

    data = [{
        "timestamp": r.timestamp,
        "latitude": r.latitude,
        "longitude": r.longitude,
        "speed": r.speed,
        "temperature": r.temperature,
        "fuel_percent": r.fuel_percent,
    } for r in records]

    return JsonResponse({"history": data})


def history_timely(request):
    minutes = int(request.GET.get("minutes", 30))
    time_limit = timezone.now() - timedelta(minutes=minutes)
    records = BusData.objects.filter(timestamp__gte=time_limit)

    data = [{
        "timestamp": r.timestamp,
        "latitude": r.latitude,
        "longitude": r.longitude,
        "speed": r.speed,
        "temperature": r.temperature,
        "fuel_percent": r.fuel_percent,
    } for r in records]

    return JsonResponse({"minutes": minutes, "history": data})








