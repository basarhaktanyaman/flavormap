from django.contrib import admin
from .models import Category, Location, Restaurant, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["city", "district"]
    list_filter = ["city"]
    search_fields = ["city", "district"]


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "location", "price_range", "average_rating", "created_at"]
    list_filter = ["category", "location__city", "price_range"]
    search_fields = ["name", "description", "address"]
    inlines = [ReviewInline]

    @admin.display(description="Avg. Rating")
    def average_rating(self, obj):
        rating = obj.average_rating()
        return f"{rating}/5" if rating else "–"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["restaurant", "author_name", "rating", "created_at"]
    list_filter = ["rating"]
    search_fields = ["author_name", "comment"]
