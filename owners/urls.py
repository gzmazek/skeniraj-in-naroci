from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile, name='profile_rest'),
    path("sign-in/", views.sign_in, name='sign-in_rest'),
    path('sign-out/', views.sign_out, name='sign-out_rest'),
    path('<int:unique_id>/', views.restaurant_dashboard, name='restaurant_dashboard'),
    path('<int:unique_id>/save_table_position/<int:table_id>/', views.save_table_position, name='save_table_position'),
    path('<int:unique_id>/add_table/', views.add_table, name='add_table'),
    path('<int:unique_id>/delete_table/<int:table_id>/', views.delete_table, name='delete_table'),
    path('update_table_position/', views.update_table_position, name='update_table_position'),
    path('table_orders/', views.table_orders, name='table_orders'),
    path('mark_order_finished/<int:order_id>/', views.mark_order_finished, name='mark_order_finished'),
    path('customers/', views.customers_view, name='customers_view'), 
]
