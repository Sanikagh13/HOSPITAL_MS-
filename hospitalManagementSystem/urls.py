from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views
from appointments import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('appointments.urls')),
    path('register/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Now 'views' is defined
    path('appointments/', include('appointments.urls')),
    path('', include('users.urls')),  # Handles login, registration, and user dashboard
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), # Add this!
]