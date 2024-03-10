from django.shortcuts import render
from .serializers import *
from rest_framework.generics import CreateAPIView
from .models import *

class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer