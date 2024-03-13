from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('verify/', VerifyView.as_view()),
    path('resend_verify/', ResendVerifyView.as_view()),
]
