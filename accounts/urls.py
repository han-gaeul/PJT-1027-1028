from urllib.parse import urlparse
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
