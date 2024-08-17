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
    path('<int:unique_id>/products/', views.restaurant_products, name='restaurant_products'),
    path('update_table_position/', views.update_table_position, name='update_table_position'),
    path('table_orders/', views.table_orders, name='table_orders'),
    path('mark_order_finished/<int:order_id>/', views.mark_order_finished, name='mark_order_finished'),
    path('customers/', views.customers_view, name='customers_view'), 
    path('<int:unique_id>/get-order-details/<int:table_id>/', views.get_order_details, name='get_order_details'),
    path('<int:restaurant_id>/settings/', views.settings_view, name='settings'),
    path('generate_qr_code/<int:table_id>/', views.generate_qr_code, name='generate_qr_code'),

    path('<int:restaurant_id>/get_items/<int:order_id>/', views.get_items_by_order_id, name='get_items_by_order_id'),
    path('<int:restaurant_id>/addMenuItem/', views.add_menu_item, name='add_menu_item'),
    path('<int:restaurant_id>/removeMenuItems/', views.remove_menu_items, name='remove_menu_items'),

    path('mark_item_prepared/<int:order_id>/<int:item_id>/', views.mark_item_prepared, name='mark_item_prepared'),
    path('mark_order_prepared/<int:order_id>/', views.mark_order_prepared, name='mark_order_prepared'),
    path('mark_order_delivered/<int:order_id>/', views.mark_order_delivered, name='mark_order_delivered')
]
