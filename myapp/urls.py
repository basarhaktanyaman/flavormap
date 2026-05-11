from django.urls import path

from . import views

app_name = "myapp"

urlpatterns = [
    path("", views.home, name="home"),
    path("restaurants/", views.restaurant_list, name="restaurant_list"),
    path("restaurants/new/", views.restaurant_create, name="restaurant_create"),
    path("restaurants/<int:pk>/", views.restaurant_detail, name="restaurant_detail"),
    path("restaurants/<int:pk>/edit/", views.restaurant_edit, name="restaurant_edit"),
    path("restaurants/<int:pk>/delete/", views.restaurant_delete, name="restaurant_delete"),
    path("restaurants/<int:pk>/favorite/", views.favorite_toggle, name="favorite_toggle"),
    path("restaurants/<int:pk>/review/", views.review_create_or_update, name="review_create"),
    path("restaurants/<int:pk>/menu/new/", views.menu_item_create, name="menu_item_create"),
    path("restaurants/<int:pk>/hours/", views.opening_hours_edit, name="opening_hours_edit"),
    path("menu/<int:item_id>/edit/", views.menu_item_edit, name="menu_item_edit"),
    path("menu/<int:item_id>/delete/", views.menu_item_delete, name="menu_item_delete"),
    path("reviews/<int:review_id>/delete/", views.review_delete, name="review_delete"),
    path("reviews/<int:review_id>/reply/", views.review_reply, name="review_reply"),
    path("favorites/", views.favorites_list, name="favorites_list"),
    path("profile/", views.profile, name="profile"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
