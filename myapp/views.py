from django.shortcuts import render, get_object_or_404
from .models import Restaurant, Category


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

    category_id = request.GET.get("category")
    city = request.GET.get("city")
    price = request.GET.get("price")

    if category_id:
        restaurants = restaurants.filter(category_id=category_id)
    if city:
        restaurants = restaurants.filter(location__city=city)
    if price:
        restaurants = restaurants.filter(price_range=price)

    categories = Category.objects.all()

    context = {
        "restaurants": restaurants,
        "categories": categories,
        "selected_category": category_id,
        "selected_city": city,
        "selected_price": price,
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
