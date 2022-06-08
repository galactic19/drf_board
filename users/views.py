from django.contrib.auth.models import User
from rest_framework import generics

from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):  # generics APIVew 를 사용하여 구현
    queryset = User.objects.all()
    serializer_class = RegisterSerializer