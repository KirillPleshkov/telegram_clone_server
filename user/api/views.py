from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.api.serializers import UserDetailSerializer

user_model = get_user_model()


class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer
    queryset = user_model

    def list(self, request):
        user = get_object_or_404(self.queryset, id=request.user.id)
        serializer = self.serializer_class(user)
        return Response(serializer.data)
