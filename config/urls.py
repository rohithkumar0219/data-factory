"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.shortcuts import render
from django.contrib import admin
from django.urls import path, include
from datasets.views import dashboard, upload, download

def home(request):
    return render(request, "home.html")

def features(request):
    return render(request, "features.html")

def how_it_works(request):
    return render(request, "how_it_works.html")

def use_cases(request):
    return render(request, "use_cases.html")

def security(request):
    return render(request, "security.html")

urlpatterns = [
    path('', home, name='home'),
    path('features/', features, name='features'),
    path('how-it-works/', how_it_works, name='how_it_works'),
    path('use-cases/', use_cases, name='use_cases'),
    path('security/', security, name='security'),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),

    path('dashboard/', dashboard),
    path('upload/', upload),
    path('download/<int:id>/', download),
]