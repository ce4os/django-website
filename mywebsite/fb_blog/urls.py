from django.urls import path
from .views import detail_view, home_view, month_view

urlpatterns = [
    path("", home_view, name="home"),
    path("detail/<int:post_id>/", detail_view, name="detail"),
    path("month/<str:month_id>/", month_view, name="month")
]