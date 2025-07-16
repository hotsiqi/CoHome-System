from django.urls import path
from . import views
from users import views as user_views

urlpatterns = [
    path('', user_views.user_redirect, name='user-redirect'),
    path('home/', views.home, name='home'),
]
