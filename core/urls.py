from django.urls import path

from . import views

app_name = 'core'


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('team/', views.team, name='team'),
    path('services/', views.services, name='services'),
    path('why/', views.why, name='why'),
    path('profile/', views.profile, name='profile'),
]
