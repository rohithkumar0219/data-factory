from django.urls import path
from .views import register, face_login

urlpatterns = [
    path('register/', register),
    path('face-login/', face_login),
]
