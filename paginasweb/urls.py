from django.urls import path
from .views import IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", IndexView.as_view(), name="about"),
]
