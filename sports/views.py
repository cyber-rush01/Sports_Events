from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import SportEvent, Registration


def home(request):
    return render(request, "sports/index.html")


def register_user(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check whether username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        # Create new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        # Success message
        messages.success(request, "Success registration!")

        # Go directly to login page
        return redirect("login")

    return render(request, "sports/register.html")


def login_user(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check username and password
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # Login user
            login(request, user)

            # Go to events page
            return redirect("events")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, "sports/login.html")


def logout_user(request):

    logout(request)

    messages.success(request, "You have been logged out.")

    return redirect("home")


@login_required
def events(request):

    event_list = SportEvent.objects.all()

    return render(
        request,
        "sports/events.html",
        {"events": event_list}
    )


@login_required
def event_detail(request, event_id):

    event = get_object_or_404(
        SportEvent,
        id=event_id
    )

    return render(
        request,
        "sports/event_detail.html",
        {"event": event}
    )


@login_required
def register_event(request, event_id):

    event = get_object_or_404(
        SportEvent,
        id=event_id
    )

    # Check whether user already registered
    already_registered = Registration.objects.filter(
        user=request.user,
        event=event
    ).exists()

    if already_registered:

        messages.warning(
            request,
            "You are already registered for this event."
        )

        return redirect(
            "event_detail",
            event_id=event.id
        )

    # Create registration
    Registration.objects.create(
        user=request.user,
        event=event
    )

    messages.success(
        request,
        "Successfully registered for the event!"
    )

    return redirect("dashboard")


@login_required
def dashboard(request):

    registrations = Registration.objects.filter(
        user=request.user
    ).select_related("event")

    return render(
        request,
        "sports/dashboard.html",
        {"registrations": registrations}
    )