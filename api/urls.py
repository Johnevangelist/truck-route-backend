from django.urls import path
from .views import fuel_plan

urlpatterns = [
    path("fuel-plan/", fuel_plan),
]
