from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('daily_data', views.daily_data, name='daily_data'),
    path('daily_users', views.daily_users, name='daily_users')
]