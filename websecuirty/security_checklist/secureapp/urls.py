from django.urls import path

from secureapp.views import home, register, dashboard, logout, account_locked

urlpatterns = [
    path('', home, name=''),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('user-logout/', logout, name='user-logout'),
    path('user-locked/', account_locked, name='user-locked'),
]
