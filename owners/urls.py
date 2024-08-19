from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile, name='profile_rest'),
    path("sign-in/", views.sign_in, name='sign-in_rest'),
    path('sign-out/', views.sign_out, name='sign-out_rest'),
    path('<int:restaurant_id>/', views.restaurant_dashboard, name='restaurant_dashboard'),
    path('<int:restaurant_id>/products/', views.restaurant_products, name='restaurant_products'),
    path('<int:restaurant_id>/settings/', views.settings_view, name='settings'),
    path('customers/', views.customers_view, name='customers_view'), 

    path('<int:restaurant_id>/save_table_position/<int:table_id>/', views.save_table_position, name='save_table_position'),
    path('<int:restaurant_id>/add_table/', views.add_table, name='add_table'),
    path('<int:restaurant_id>/delete_table/<int:table_id>/', views.delete_table, name='delete_table'),
    
    path('generate_qr_code/<int:table_id>/', views.generate_qr_code, name='generate_qr_code'),

    path('<int:restaurant_id>/get_order_items/<int:order_id>/', views.get_items_by_order_id, name='get_items_by_order_id'),
    path('<int:restaurant_id>/mark_item_prepared/<int:order_id>/<int:item_id>/', views.mark_item_prepared, name='mark_item_prepared'),
    path('<int:restaurant_id>/mark_order_prepared/<int:order_id>/', views.mark_order_prepared, name='mark_order_prepared'),
    path('<int:restaurant_id>/mark_order_delivered/<int:order_id>/', views.mark_order_delivered, name='mark_order_delivered'),

    path('<int:restaurant_id>/addMenuItem/', views.add_menu_item, name='add_menu_item'),
    path('<int:restaurant_id>/removeMenuItems/', views.remove_menu_items, name='remove_menu_items'),

    path('<int:restaurant_id>/revive_order/<int:table_id>/', views.revive_order, name='revive_order')
]
