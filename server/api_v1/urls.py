from django.contrib import admin
from django.urls import path, include
from .views import image

urlpatterns = [
        path("gen/image", image.generate_image),
    
]
