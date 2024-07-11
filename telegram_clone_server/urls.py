from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from telegram_clone_server import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/authentication/', include('authentication.api.urls')),
    path('api/user/', include('user.api.urls')),
    path('api/chat/', include('chat.api.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
