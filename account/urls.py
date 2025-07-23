from django.urls import path
from . import views

urlpatterns = [
    path('', views.account_web, name='account-web'),
    path('account/personal-info/', views.personal_info, name='account-personal-info')
]
