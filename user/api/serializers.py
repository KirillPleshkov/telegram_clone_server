from django.contrib.auth import get_user_model
from rest_framework import serializers

user_model = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'image')
