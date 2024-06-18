from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenVerifyView
from django.urls import path

from authentication.api.views import GithubLogin, YandexLogin
from telegram_clone_server import settings

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),

    path("github/", GithubLogin.as_view(), name="github_login"),
    path("yandex/", YandexLogin.as_view(), name="yandex_login"),
]
