from django.urls import path
from . import views
import os

root = os.environ.get('DJANGO_ROOT','')

urlpatterns = [
#########################################################
#                        HOME                           #
#########################################################
    path(root + '', views.home, name='home'),

#########################################################
#                    PROFILE & AUTH                     #
#########################################################
    path(root + 'profile/', views.profile, name='profile'),
    path(root + 'profile/settings', views.settings, name='settings'),
    path(root + 'sign-in/', views.sign_in, name='sign-in'),
    path(root + 'sign-out/', views.sign_out, name='sign-out'),
    path(root + 'register/', views.register, name='register'),
    
#########################################################
#                    ORDER PLACING                      #
#########################################################
    path(root + 'order/<int:table_id>/', views.order, name='order'),
    path(root + 'order/confirmation/', views.order_confirm, name='order_confirm'),
    path(root + 'order/placeOrder/', views.place_order, name='place_order'),

#########################################################
#                       QR CODE                         #
#########################################################
    path(root + 'scan_qr/', views.scan_qr, name='scan_qr'),
    path(root + 'process_qr/', views.process_qr, name='process_qr')
]
