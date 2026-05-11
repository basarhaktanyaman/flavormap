from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    Category,
    Location,
    MenuItem,
    OpeningHours,
    Profile,
    Restaurant,
    Review,
)


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
    extra = 0
    readonly_fields = ("created_at",)


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1


class OpeningHoursInline(admin.TabularInline):
    model = OpeningHours
    extra = 0
    max_num = 7


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "location",
        "price_range",
        "owner",
        "is_verified",
        "average_rating",
        "created_at",
        "quick_delete",
    ]
    list_display_links = ["name"]
    list_filter = ["is_verified", "category", "location__city", "price_range"]
    list_editable = ["is_verified"]
    search_fields = ["name", "description", "address", "owner__username"]
    inlines = [MenuItemInline, OpeningHoursInline, ReviewInline]
    autocomplete_fields = ["category", "location"]
    raw_id_fields = ["owner"]
    actions = ["mark_verified", "mark_unverified"]

    @admin.display(description="Avg. Rating")
    def average_rating(self, obj):
        rating = obj.average_rating()
        return f"{rating}/5" if rating else "–"

    @admin.display(description="Actions")
    def quick_delete(self, obj):
        url = reverse("admin:myapp_restaurant_delete", args=[obj.pk])
        return format_html(
            '<a class="deletelink" href="{}" style="background:#ba2121;color:#fff;'
            'padding:4px 10px;border-radius:4px;text-decoration:none;font-size:11px;">'
            '🗑 Delete</a>',
            url,
        )

    @admin.action(description="Verify selected restaurants (publish)")
    def mark_verified(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} restaurant(s) marked as verified.")

    @admin.action(description="Unverify selected restaurants (hide)")
    def mark_unverified(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f"{updated} restaurant(s) marked as unverified.")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["restaurant", "author_name", "rating", "created_at"]
    list_filter = ["rating"]
    search_fields = ["author_name", "comment"]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ["name", "restaurant", "category", "price"]
    list_filter = ["category"]
    search_fields = ["name", "restaurant__name"]


@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ["restaurant", "get_day_display", "open_time", "close_time", "is_closed"]
    list_filter = ["day", "is_closed"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at"]
    search_fields = ["user__username"]
