from urllib.parse import urlparse
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('password/', views.change_password, name='change_password'),
    path('<int:pk>/', views.detail, name='detail'),
    path('update/', views.update, name='update'),
]
