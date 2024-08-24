from django.urls import path
from . import views


urlpatterns = [
#########################################################
#                     PROFILE & AUTH                    #
#########################################################
    path("", views.profile, name='profile_rest'),
    path("sign-in/", views.sign_in, name='sign-in_rest'),
    path('sign-out/', views.sign_out, name='sign-out_rest'),

#########################################################
#                  RESTAURANT DASHBOARD                 #
#########################################################
    path('<int:restaurant_id>/', views.restaurant_dashboard, name='restaurant_dashboard'),
    path('<int:restaurant_id>/products/', views.restaurant_products, name='restaurant_products'),

#########################################################
#                 TABLE MANAGEMENT ROUTES               #
#########################################################
    path('<int:restaurant_id>/save_table_position/<int:table_id>/', views.save_table_position, name='save_table_position'),
    path('<int:restaurant_id>/add_table/', views.add_table, name='add_table'),
    path('<int:restaurant_id>/delete_table/<int:table_id>/', views.delete_table, name='delete_table'),

#########################################################
#                      QR CODE ROUTES                   #
#########################################################
    path('generate_qr_code/<int:table_id>/', views.generate_qr_code, name='generate_qr_code'),

#########################################################
#                      ORDER MANAGEMENT                 #
#########################################################
    path('<int:restaurant_id>/get_order_items/<int:order_id>/', views.get_items_by_order_id, name='get_items_by_order_id'),
    path('<int:restaurant_id>/mark_item_prepared/<int:order_id>/<int:item_id>/', views.mark_item_prepared, name='mark_item_prepared'),
    path('<int:restaurant_id>/mark_order_prepared/<int:order_id>/', views.mark_order_prepared, name='mark_order_prepared'),
    path('<int:restaurant_id>/mark_order_delivered/<int:order_id>/', views.mark_order_delivered, name='mark_order_delivered'),

#########################################################
#                    MENU MANAGEMENT                    #
#########################################################
    path('<int:restaurant_id>/addMenuItem/', views.add_menu_item, name='add_menu_item'),
    path('<int:restaurant_id>/removeMenuItems/', views.remove_menu_items, name='remove_menu_items'),

#########################################################
#                    ORDER REVIVAL                      #
#########################################################
    path('<int:restaurant_id>/revive_order/<int:table_id>/', views.revive_order, name='revive_order'),

#########################################################
#                   KITCHEN SETTINGS                    #
#########################################################
    path('<int:restaurant_id>/kitchen_settings/', views.kitchen_settings, name='kitchen_settings'),
    path('<int:restaurant_id>/add_kitchen/', views.add_kitchen, name='add_kitchen'),
    path('<int:restaurant_id>/get_items_for_kitchen/<int:kitchen_id>/', views.get_items_for_kitchen, name='get_items_for_kitchen'),
    path('<int:restaurant_id>/kitchen/<int:kitchen_id>/add_item/', views.add_item_to_kitchen, name='add_item_to_kitchen'),
    path('<int:restaurant_id>/kitchen/<int:kitchen_id>/delete_item/<int:item_id>/', views.delete_item_from_kitchen, name='delete_item_from_kitchen'),

    path('<int:restaurant_id>/get_kitchen_items/<int:kitchen_id>/', views.get_kitchen_items, name='get_kitchen_items'),
    path('<int:restaurant_id>/get_items_not_in_kitchen/<int:kitchen_id>/', views.get_items_not_in_kitchen, name='get_items_not_in_kitchen'),
    path('<int:restaurant_id>/delete_kitchen/<int:kitchen_id>/', views.delete_kitchen, name='delete_kitchen'),
    path('<int:restaurant_id>/delete_item_from_kitchen/<int:kitchen_id>/<int:item_id>/', views.delete_item_from_kitchen, name='delete_item_from_kitchen'),

#########################################################
#                   KITCHEN VIEW                        #
#########################################################
    path('<int:restaurant_id>/kitchen_view/', views.kitchen_view, name='kitchen_view'),
    path('<int:restaurant_id>/kitchen_view/<int:kitchen_id>/', views.kitchen_view, name='kitchen_view_filtered'),

#########################################################
#                   ANALYTICS                           #
#########################################################
    path('<int:restaurant_id>/analytics/', views.analytics_view, name='analytics_view'),
]
