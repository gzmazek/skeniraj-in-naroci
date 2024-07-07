from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile, name='profile_rest'),
    path("sign-in/", views.sign_in, name='sign-in_rest'),
    path('sign-out/', views.sign_out, name='sign-out_rest'),
    path('<int:unique_id>/', views.restaurant_dashboard, name='restaurant_dashboard'),
]