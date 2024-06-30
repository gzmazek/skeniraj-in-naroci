from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("register/", views.register, name='register'),
    path("sign-in/", views.sign_in, name='sign-in'),
    path("profile/", views.profile, name='profile'),
    path('sign-out/', views.sign_out, name='sign-out'),
]
