from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('city/<str:location>/', views.city_detail, name='city_detail'),
]
