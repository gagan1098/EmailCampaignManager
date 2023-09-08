from django.urls import path

from .apps import CampaignmanagerConfig

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
