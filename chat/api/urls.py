from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chat.api.views import ChatViewSet

router = DefaultRouter()
router.register(r'', ChatViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
