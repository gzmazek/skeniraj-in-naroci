from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile, name='profile_rest'),
    path("sign-in/", views.sign_in, name='sign-in_rest'),
    path('sign-out/', views.sign_out, name='sign-out_rest'),
    path('<int:unique_id>/', views.restaurant_dashboard, name='restaurant_dashboard'),
    path('dashboard/<int:unique_id>/tables/', views.tables_list, name='tables_list'),
    path('dashboard/<int:unique_id>/add_table/', views.add_table, name='add_table'),
    path('dashboard/<int:unique_id>/delete_table/<int:table_id>/', views.delete_table, name='delete_table'),
]