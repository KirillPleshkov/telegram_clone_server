import json
import datetime
import jwt

from channels.generic.websocket import AsyncWebsocketConsumer

from telegram_clone_server import settings


def qr_access_token(channel_name):
    access_token_payload = {
        'channel_name': channel_name,
        'exp': datetime.datetime.utcnow() + settings.QR_TOKEN_LIFETIME,
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
    return access_token


class QrAuthConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data == 'update_qr':
            token = qr_access_token(self.channel_name)
            await self.send(json.dumps({'qr_data': token}))

    async def qr_login(self, event):
        await self.send(json.dumps({'refresh': event["text"]}))
