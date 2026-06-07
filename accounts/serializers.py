from rest_framework import serializers
from . models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'password','avater']
        extra_kwargs = {'password':{'write_only':True}}
    
    def create(self, validated_data):
        account = Account.objects.create_user(**validated_data)
        return account