from django.shortcuts import render
from rest_framework import generics
from . models import Account
from . serializers import AccountSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

class CreateAccountAPIView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]


class GetUserIdAPIView(generics.RetrieveAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'

    def get_queryset(self):
        print(self.kwargs)
        return Account.objects.filter(username=self.kwargs['username'])