from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import MenuItem, OpeningHours, Profile, Restaurant

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """Extends the default UserCreationForm with a required email."""

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "avatar"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3, "placeholder": "A short bio..."}),
        }


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            "name",
            "description",
            "address",
            "phone",
            "price_range",
            "category",
            "location",
            "image",
            "image_url",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "address": forms.TextInput(attrs={"placeholder": "Street, building, etc."}),
            "phone": forms.TextInput(attrs={"placeholder": "+90 ..."}),
        }


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["name", "description", "price", "category"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }


class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = OpeningHours
        fields = ["day", "open_time", "close_time", "is_closed"]
        widgets = {
            "open_time": forms.TimeInput(attrs={"type": "time"}),
            "close_time": forms.TimeInput(attrs={"type": "time"}),
        }
