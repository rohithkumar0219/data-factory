from django.urls import path
from .views import register, face_login
from .views import logout_view

urlpatterns = [
    path('register/', register),
    path('face-login/', face_login),
    path('logout/', logout_view, name='logout'),
]
