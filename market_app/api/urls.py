from django.contrib import admin
from django.urls import path
from .views import first_view

urlpatterns = [
    path('', first_view)
]