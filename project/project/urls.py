"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from service_nlp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add-document/', views.request_add_document),
    path('update-IDF/', views.request_update_IDF),
    path('update-TF-IDF/', views.request_update_TF_IDF),
    path('test/', views.request_test),
    path('start-TF/', views.request_start_TF),
]
