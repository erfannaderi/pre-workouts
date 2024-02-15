from django.urls import path

from getotp.views import RequestOtp, VerifyOtp

urlpatterns = [
    path('request/', RequestOtp.as_view()),
    path('verify/', VerifyOtp.as_view()),
]
