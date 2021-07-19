from django.urls import path
from . import views

urlpatterns = [path("", views.VideoItems.as_view()), path("show/", views.show)]
