"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib import admin
from django.urls import path
from users.views import RegisterView,home_view,CheckUsernameView,LoginView
from .views import get_hardware_recommendations
from shopowner.views import ShopOwnerRegistrationAPIView


urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/check_username/<str:username>/', CheckUsernameView.as_view(), name='check_username'),    
    path('api/login/', LoginView.as_view(), name='login'),  # Add this line
    #path('api/recommendations/', get_hardware_recommendations, name='get_hardware_recommendations'),
    path('api/', include('recommendations.urls')),  # Include the app's URLs
    path('api/register-shop-owner/', ShopOwnerRegistrationAPIView.as_view(), name='register-shop-owner'),
    
    
]




