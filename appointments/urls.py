from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patient/edit/<int:id>/', views.edit_patient, name='edit_patient'),
    path('patient/delete/<int:id>/', views.delete_patient, name='delete_patient'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
]