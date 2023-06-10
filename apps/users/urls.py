from django.urls import path

from apps.users.views import SendVerificationCode

urlpatterns = [
    path('verification', SendVerificationCode.as_view(), name='verification'),
]
