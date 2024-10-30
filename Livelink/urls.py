"""Livelink URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_link, name='create_link'),
    path('<str:short_code>/', views.redirect_link, name='redirect_link'),
    path('<str:short_code>/edit/', views.edit_link, name='edit_link'),
    path('<str:short_code>/delete/', views.delete_link, name='delete_link'),
    path('bio/', views.link_in_bio, name='link_in_bio'),
    path('admin/', admin.site.urls),
]
