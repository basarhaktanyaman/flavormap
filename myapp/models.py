from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Bootstrap icon class, e.g. bi-cup-hot")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Location(models.Model):
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    class Meta:
        ordering = ["city", "district"]
        unique_together = ["city", "district"]

    def __str__(self):
        return f"{self.district}, {self.city}"


class Restaurant(models.Model):
    PRICE_CHOICES = [
        ("€", "€ – Budget"),
        ("€€", "€€ – Mid-range"),
        ("€€€", "€€€ – Fine Dining"),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=300)
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(r"^\+?[\d\s\-()]+$", "Enter a valid phone number.")],
    )
    price_range = models.CharField(max_length=3, choices=PRICE_CHOICES, default="€€")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="restaurants")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="restaurants")
    image = models.ImageField(upload_to="restaurants/", blank=True, null=True)
    image_url = models.URLField(blank=True, help_text="Optional external image URL (used if no upload)")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="owned_restaurants",
        null=True,
        blank=True,
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Only verified restaurants are visible to the public. Admin/staff submissions are auto-verified.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.category})"

    def average_rating(self):
        """Return the average rating from related reviews.
        Returns None when there are no reviews yet.
        """
        reviews = self.reviews.all()
        if not reviews.exists():
            return None
        return round(reviews.aggregate(avg=models.Avg("rating"))["avg"], 1)

    def review_count(self):
        return self.reviews.count()

    def display_image(self):
        """Return uploaded image URL or fallback external URL."""
        if self.image:
            return self.image.url
        return self.image_url or ""


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="reviews")
    author_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author_name} – {self.restaurant.name} ({self.rating}/5)"


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ("starter", "Starter"),
        ("main", "Main Course"),
        ("dessert", "Dessert"),
        ("drink", "Drink"),
        ("other", "Other"),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu_items")
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="main")

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} – {self.price}"


class OpeningHours(models.Model):
    DAY_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="opening_hours")
    day = models.PositiveSmallIntegerField(choices=DAY_CHOICES)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False, help_text="Tick if closed all day")

    class Meta:
        ordering = ["day"]
        unique_together = ["restaurant", "day"]
        verbose_name_plural = "Opening hours"

    def __str__(self):
        return f"{self.restaurant.name} – {self.get_day_display()}"

    def display_hours(self):
        if self.is_closed:
            return "Closed"
        if self.open_time and self.close_time:
            return f"{self.open_time.strftime('%H:%M')} – {self.close_time.strftime('%H:%M')}"
        return "—"


class Profile(models.Model):
    """Optional bio/avatar attached to a user."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.user}"
