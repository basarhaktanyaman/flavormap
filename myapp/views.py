from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileForm, UserRegistrationForm
from .models import Category, Profile, Restaurant


# ----- Public pages -----------------------------------------------------------


def home(request):
    featured_restaurants = Restaurant.objects.select_related("category", "location")[:6]
    categories = Category.objects.all()
    context = {
        "featured_restaurants": featured_restaurants,
        "categories": categories,
    }
    return render(request, "myapp/home.html", context)


def restaurant_list(request):
    restaurants = Restaurant.objects.select_related("category", "location").all()
    categories = Category.objects.all()
    context = {
        "restaurants": restaurants,
        "categories": categories,
    }
    return render(request, "myapp/restaurant_list.html", context)


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(
        Restaurant.objects.select_related("category", "location"),
        pk=pk,
    )
    reviews = restaurant.reviews.all()
    context = {
        "restaurant": restaurant,
        "reviews": reviews,
        "avg_rating": restaurant.average_rating(),
    }
    return render(request, "myapp/restaurant_detail.html", context)


def about(request):
    return render(request, "myapp/about.html")


def contact(request):
    return render(request, "myapp/contact.html")


# ----- Auth -------------------------------------------------------------------


def register(request):
    if request.user.is_authenticated:
        return redirect("myapp:home")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect("myapp:home")
    else:
        form = UserRegistrationForm()

    return render(request, "registration/register.html", {"form": form})


# ----- Profile ----------------------------------------------------------------


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("myapp:profile")
    else:
        form = ProfileForm(instance=profile_obj)

    return render(
        request,
        "myapp/profile.html",
        {
            "form": form,
            "profile_obj": profile_obj,
        },
    )
