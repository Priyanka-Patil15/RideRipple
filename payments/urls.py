from django.urls import path
from . import views

urlpatterns = [
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('stripe/', views.checkout, name='stripe_payment'),
    path('wallet/', views.wallet_pay, name='wallet_payment'),
    path('index/', views.index, name='payment_index'),
    path('select/<int:ride_id>/', views.select_payment_method, name='select-payment'),
]
