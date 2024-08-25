from django.urls import path
from . import views

urlpatterns = [
#########################################################
#                        HOME                           #
#########################################################
    path('', views.home, name='home'),

#########################################################
#                    PROFILE & AUTH                     #
#########################################################
    path('profile/', views.profile, name='profile'),
    path('profile/settings', views.settings, name='settings'),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-out/', views.sign_out, name='sign-out'),
    path('register/', views.register, name='register'),
    
#########################################################
#                    ORDER PLACING                      #
#########################################################
    path('order/<int:table_id>/', views.order, name='order'),
    path('order/confirmation/', views.order_confirm, name='order_confirm'),
    path('order/placeOrder/', views.place_order, name='place_order'),

#########################################################
#                       QR CODE                         #
#########################################################
    path('scan_qr/', views.scan_qr, name='scan_qr'),
    path('process_qr/', views.process_qr, name='process_qr')
]
