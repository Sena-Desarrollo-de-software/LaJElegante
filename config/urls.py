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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView 
from core import views as core_views
from finance import views as finance_views
from restaurant import views as restaurant_views
from rooms import views as rooms_views
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/hotel/lobby/', permanent=False)),
    path("hotel/", include("core.urls")),
    path("finance/", include("finance.urls")),
    path("restaurant/", include("restaurant.urls")),
    path("rooms/", include("rooms.urls")),
    path("users/", include("users.urls")),
]
