from django.urls import path
from WeatherAPI import views

urlpatterns = [
    path('', views.main, name='main'),
    path('city/<str:city>/', views.city, name='city'),
    path('city/<str:city>/day/<int:day>/', views.atDay, name='day'),
]