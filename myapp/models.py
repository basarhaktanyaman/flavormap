from django.db import models
from django.core.validators import RegexValidator


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
    image_url = models.URLField(blank=True, help_text="External image URL for the restaurant")
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
