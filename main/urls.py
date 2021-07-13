from django.urls import path

from . import views


app_name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('layout', views.my_view, name='layout'),
]
