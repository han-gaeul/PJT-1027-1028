from urllib.parse import urlparse
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
]
