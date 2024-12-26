from django.urls import path, include
from django.contrib import admin
from users.views import RegisterView, home_view, CheckUsernameView, LoginView
from shopowner.views import ShopOwnerRegistrationAPIView
from hardware_data import views  # Import the views module from the hardware_data app

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/check_username/<str:username>/', CheckUsernameView.as_view(), name='check_username'),    
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/', include('recommendations.urls')),  # Include the app's URLs
    path('api/register-shop-owner/', ShopOwnerRegistrationAPIView.as_view(), name='register-shop-owner'),
    path('api/hardware-data/', include('hardware_data.urls')),  # Include hardware_data URLs
]