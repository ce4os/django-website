from django.urls import path
from .views import detail_view, home_view

urlpatterns = [
    path("", home_view, name="home"),
    path("<int:post_id>/", detail_view, name="detail"),
]