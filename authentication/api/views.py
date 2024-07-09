import re
import requests
import jwt

from allauth.account.adapter import get_adapter
from asgiref.sync import async_to_sync
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.yandex.views import YandexAuth2Adapter
from dj_rest_auth.utils import jwt_encode
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from channels.layers import get_channel_layer

from telegram_clone_server import settings


class CustomGithubOAuth2Adapter(GitHubOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        login = super().complete_login(request, app, token, **kwargs)
        login.user.image = login.account.extra_data['avatar_url']
        return login


class CustomYandexOAuth2Adapter(YandexAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        login = super().complete_login(request, app, token, **kwargs)

        if login.account.extra_data['is_avatar_empty']:
            return login

        img = f'https://avatars.mds.yandex.net/get-yapic/' + login.account.extra_data[
            'default_avatar_id'] + '/'

        login.user.image = img
        return login


def download_image(user):
    img = str(user.image)

    if img.startswith('profile_image') or not img:
        return

    file_name = img
    if img.endswith('/'):
        file_name = img[:-1]

    # Добавление аватарки при первом заходе
    file_name = file_name.split('/')[-1]
    file_name = re.sub(r'[|*?<>:\\\n\r\t\v]', '', file_name)

    r = requests.get(img)

    img_temp = NamedTemporaryFile()
    img_temp.write(r.content)
    img_temp.flush()

    user.image.save(f'{file_name}.png', File(img_temp), save=True)


class GithubLogin(SocialLoginView):
    adapter_class = CustomGithubOAuth2Adapter
    callback_url = "http://127.0.0.1:3000/"
    client_class = OAuth2Client

    def process_login(self):
        get_adapter(self.request).login(self.request, self.user)
        download_image(self.user)


class YandexLogin(SocialLoginView):
    adapter_class = CustomYandexOAuth2Adapter
    callback_url = "http://127.0.0.1:3000/"
    client_class = OAuth2Client

    def process_login(self):
        get_adapter(self.request).login(self.request, self.user)
        download_image(self.user)


channel_layer = get_channel_layer()


class LoginByQR(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        channel_name = ''
        try:
            qr_token = request.data['qr_token']
            decoded_jwt = jwt.decode(qr_token, settings.SECRET_KEY, algorithms=["HS256"])
            channel_name = decoded_jwt['channel_name']
        except:
            return Response({'success': False})
        user = request.user
        _, refresh_token = jwt_encode(user)
        async_to_sync(channel_layer.send)(channel_name, {'type': 'qr.login', 'text': str(refresh_token)})

        return Response({'success': True})
