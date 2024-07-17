from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('profile/', views.profile, name='profile'),
    path('sign-out/', views.sign_out, name='sign-out'),
    path('order/<int:table_id>/', views.order, name='order'),
    path('order/confirmation/', views.order_confirm, name='order_confirm'),
    path('order/placeOrder/', views.place_order, name='place_order'),

    path('scan_qr/', views.scan_qr, name='scan_qr'),
    path('process_qr/', views.process_qr, name='process_qr')
]
