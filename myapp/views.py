from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Avg, Count, Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import (
    MenuItemForm,
    OpeningHoursForm,
    ProfileForm,
    RestaurantForm,
    ReviewForm,
    ReviewReplyForm,
    UserRegistrationForm,
)
from .models import (
    Category,
    Favorite,
    MenuItem,
    OpeningHours,
    Profile,
    Restaurant,
    Review,
    ReviewReply,
)


# ----- Helpers ----------------------------------------------------------------


def _restaurant_queryset():
    """Base queryset with rating annotations (no visibility filter)."""
    return (
        Restaurant.objects.select_related("category", "location", "owner")
        .annotate(avg_rating=Avg("reviews__rating"), n_reviews=Count("reviews"))
    )


def _visible_restaurants(user=None):
    """Public-facing queryset: only verified restaurants are listed.

    Staff still manage pending entries through the /admin/ panel and via direct
    detail URLs (handled by _can_view_restaurant), not through public listings.
    """
    return _restaurant_queryset().filter(is_verified=True)


def _owner_required(restaurant, user):
    """Return True if user can edit this restaurant."""
    if user.is_superuser or user.is_staff:
        return True
    return restaurant.owner_id == user.id


def _can_view_restaurant(restaurant, user):
    """Pending restaurants are visible only to their owner or staff."""
    if restaurant.is_verified:
        return True
    if not user.is_authenticated:
        return False
    return user.is_staff or restaurant.owner_id == user.id


# ----- Public pages -----------------------------------------------------------


def home(request):
    base_qs = _visible_restaurants(request.user)
    top_rated = base_qs.filter(n_reviews__gt=0).order_by("-avg_rating", "-n_reviews")[:6]
    newest = base_qs.order_by("-created_at")[:6]
    categories = Category.objects.all()
    context = {
        "top_rated": top_rated,
        "newest": newest,
        "categories": categories,
    }
    return render(request, "myapp/home.html", context)


def restaurant_list(request):
    restaurants = _visible_restaurants(request.user)

    q = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "")
    city = request.GET.get("city", "").strip()
    price = request.GET.get("price", "")
    sort = request.GET.get("sort", "")

    if q:
        restaurants = restaurants.filter(
            Q(name__icontains=q)
            | Q(description__icontains=q)
            | Q(location__city__icontains=q)
            | Q(location__district__icontains=q)
        )
    if category_id:
        restaurants = restaurants.filter(category_id=category_id)
    if city:
        restaurants = restaurants.filter(location__city__icontains=city)
    if price:
        restaurants = restaurants.filter(price_range=price)

    if sort == "rating":
        restaurants = restaurants.order_by("-avg_rating", "-n_reviews")
    elif sort == "newest":
        restaurants = restaurants.order_by("-created_at")
    elif sort == "name":
        restaurants = restaurants.order_by("name")

    categories = Category.objects.all()
    context = {
        "restaurants": restaurants,
        "categories": categories,
        "q": q,
        "selected_category": category_id,
        "selected_city": city,
        "selected_price": price,
        "selected_sort": sort,
    }
    return render(request, "myapp/restaurant_list.html", context)


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(_restaurant_queryset(), pk=pk)
    if not _can_view_restaurant(restaurant, request.user):
        return HttpResponseForbidden(
            "This restaurant is awaiting admin verification and is not publicly visible yet."
        )
    reviews = (
        restaurant.reviews.select_related("user")
        .prefetch_related("replies__user")
        .all()
    )
    menu_items = restaurant.menu_items.all()
    opening_hours = restaurant.opening_hours.all()

    user_review = None
    is_favorite = False
    if request.user.is_authenticated:
        user_review = restaurant.reviews.filter(user=request.user).first()
        is_favorite = Favorite.objects.filter(user=request.user, restaurant=restaurant).exists()

    review_form = ReviewForm(instance=user_review)
    reply_form = ReviewReplyForm()

    context = {
        "restaurant": restaurant,
        "reviews": reviews,
        "avg_rating": restaurant.average_rating(),
        "menu_items": menu_items,
        "opening_hours": opening_hours,
        "user_review": user_review,
        "is_favorite": is_favorite,
        "review_form": review_form,
        "reply_form": reply_form,
        "can_edit": request.user.is_authenticated and _owner_required(restaurant, request.user),
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


# ----- Restaurant CRUD --------------------------------------------------------


@login_required
def restaurant_create(request):
    is_staff_user = request.user.is_staff or request.user.is_superuser
    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    restaurant = form.save(commit=False)
                    restaurant.owner = request.user
                    restaurant.is_verified = is_staff_user
                    restaurant.save()
                    for day, _ in OpeningHours.DAY_CHOICES:
                        OpeningHours.objects.create(restaurant=restaurant, day=day, is_closed=True)
            except IntegrityError:
                messages.error(request, "Could not create restaurant due to a database conflict.")
                return render(
                    request,
                    "myapp/restaurant_form.html",
                    {"form": form, "mode": "create", "is_staff_user": is_staff_user},
                )
            if is_staff_user:
                messages.success(request, f"Restaurant '{restaurant.name}' created and published.")
            else:
                messages.info(
                    request,
                    f"Your submission '{restaurant.name}' has been sent for admin review. "
                    "It will appear on the site once approved.",
                )
            return redirect("myapp:restaurant_detail", pk=restaurant.pk)
    else:
        form = RestaurantForm()
    return render(
        request,
        "myapp/restaurant_form.html",
        {"form": form, "mode": "create", "is_staff_user": is_staff_user},
    )


@login_required
def restaurant_edit(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if not _owner_required(restaurant, request.user):
        return HttpResponseForbidden("You are not allowed to edit this restaurant.")

    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, "Restaurant updated.")
            return redirect("myapp:restaurant_detail", pk=restaurant.pk)
    else:
        form = RestaurantForm(instance=restaurant)
    return render(
        request,
        "myapp/restaurant_form.html",
        {"form": form, "mode": "edit", "restaurant": restaurant},
    )


@login_required
def restaurant_delete(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if not _owner_required(restaurant, request.user):
        return HttpResponseForbidden("You are not allowed to delete this restaurant.")
    if request.method == "POST":
        name = restaurant.name
        restaurant.delete()
        messages.success(request, f"Restaurant '{name}' deleted.")
        return redirect("myapp:restaurant_list")
    return render(request, "myapp/restaurant_confirm_delete.html", {"restaurant": restaurant})


# ----- Reviews ----------------------------------------------------------------


@login_required
@require_POST
def review_create_or_update(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    existing = Review.objects.filter(restaurant=restaurant, user=request.user).first()
    form = ReviewForm(request.POST, instance=existing)
    if form.is_valid():
        try:
            with transaction.atomic():
                review = form.save(commit=False)
                review.restaurant = restaurant
                review.user = request.user
                review.save()
        except IntegrityError:
            messages.error(request, "You have already reviewed this restaurant.")
            return redirect("myapp:restaurant_detail", pk=pk)
        messages.success(request, "Your review has been saved.")
    else:
        messages.error(request, "Please correct the errors in your review.")
    return redirect("myapp:restaurant_detail", pk=pk)


@login_required
@require_POST
def review_delete(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if review.user_id != request.user.id and not request.user.is_superuser:
        return HttpResponseForbidden("You can only delete your own review.")
    restaurant_id = review.restaurant_id
    review.delete()
    messages.success(request, "Your review has been removed.")
    return redirect("myapp:restaurant_detail", pk=restaurant_id)


@login_required
@require_POST
def review_reply(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    form = ReviewReplyForm(request.POST)
    if form.is_valid():
        reply = form.save(commit=False)
        reply.review = review
        reply.user = request.user
        reply.save()
        messages.success(request, "Reply posted.")
    else:
        messages.error(request, "Reply could not be saved.")
    return redirect("myapp:restaurant_detail", pk=review.restaurant_id)


# ----- Menu items -------------------------------------------------------------


@login_required
def menu_item_create(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if not _owner_required(restaurant, request.user):
        return HttpResponseForbidden("Only the owner can manage menu items.")
    if request.method == "POST":
        form = MenuItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.restaurant = restaurant
            item.save()
            messages.success(request, f"Added '{item.name}' to the menu.")
            return redirect("myapp:restaurant_detail", pk=pk)
    else:
        form = MenuItemForm()
    return render(
        request,
        "myapp/menu_item_form.html",
        {"form": form, "restaurant": restaurant, "mode": "create"},
    )


@login_required
def menu_item_edit(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    if not _owner_required(item.restaurant, request.user):
        return HttpResponseForbidden("Only the owner can manage menu items.")
    if request.method == "POST":
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu item updated.")
            return redirect("myapp:restaurant_detail", pk=item.restaurant_id)
    else:
        form = MenuItemForm(instance=item)
    return render(
        request,
        "myapp/menu_item_form.html",
        {"form": form, "restaurant": item.restaurant, "mode": "edit", "item": item},
    )


@login_required
@require_POST
def menu_item_delete(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    if not _owner_required(item.restaurant, request.user):
        return HttpResponseForbidden("Only the owner can manage menu items.")
    restaurant_id = item.restaurant_id
    item.delete()
    messages.success(request, "Menu item removed.")
    return redirect("myapp:restaurant_detail", pk=restaurant_id)


# ----- Opening hours ----------------------------------------------------------


@login_required
def opening_hours_edit(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if not _owner_required(restaurant, request.user):
        return HttpResponseForbidden("Only the owner can manage opening hours.")

    existing_by_day = {oh.day: oh for oh in restaurant.opening_hours.all()}
    days = OpeningHours.DAY_CHOICES

    if request.method == "POST":
        try:
            with transaction.atomic():
                for day_value, _ in days:
                    instance = existing_by_day.get(day_value)
                    prefix = f"day_{day_value}"
                    is_closed = request.POST.get(f"{prefix}_is_closed") == "on"
                    open_time = request.POST.get(f"{prefix}_open") or None
                    close_time = request.POST.get(f"{prefix}_close") or None
                    defaults = {
                        "open_time": open_time,
                        "close_time": close_time,
                        "is_closed": is_closed,
                    }
                    OpeningHours.objects.update_or_create(
                        restaurant=restaurant,
                        day=day_value,
                        defaults=defaults,
                    )
        except IntegrityError:
            messages.error(request, "Could not save opening hours.")
        else:
            messages.success(request, "Opening hours updated.")
            return redirect("myapp:restaurant_detail", pk=pk)

    rows = []
    for day_value, day_label in days:
        oh = existing_by_day.get(day_value)
        rows.append(
            {
                "day": day_value,
                "label": day_label,
                "open_time": oh.open_time if oh else None,
                "close_time": oh.close_time if oh else None,
                "is_closed": oh.is_closed if oh else True,
            }
        )

    return render(
        request,
        "myapp/opening_hours_form.html",
        {"restaurant": restaurant, "rows": rows},
    )


# ----- Favorites --------------------------------------------------------------


@login_required
@require_POST
def favorite_toggle(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)
    if not created:
        fav.delete()
        messages.info(request, f"Removed '{restaurant.name}' from favorites.")
    else:
        messages.success(request, f"Added '{restaurant.name}' to favorites.")
    next_url = request.POST.get("next") or reverse("myapp:restaurant_detail", args=[pk])
    return redirect(next_url)


@login_required
def favorites_list(request):
    favorites = (
        Favorite.objects.filter(user=request.user)
        .select_related("restaurant__category", "restaurant__location")
    )
    return render(request, "myapp/favorites.html", {"favorites": favorites})


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

    user_reviews = (
        Review.objects.filter(user=request.user)
        .select_related("restaurant")
        .order_by("-created_at")
    )
    favorites = (
        Favorite.objects.filter(user=request.user)
        .select_related("restaurant")
        .order_by("-created_at")
    )
    owned = Restaurant.objects.filter(owner=request.user).order_by("-created_at")
    pending = owned.filter(is_verified=False)
    published = owned.filter(is_verified=True)

    return render(
        request,
        "myapp/profile.html",
        {
            "form": form,
            "profile_obj": profile_obj,
            "user_reviews": user_reviews,
            "favorites": favorites,
            "owned": owned,
            "pending": pending,
            "published": published,
        },
    )
