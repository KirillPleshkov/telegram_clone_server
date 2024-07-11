from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.api.serializers import ChatCreateSerializer, GroupChannelCreateSerializer, ChatShortSerializer
from chat.models import Chat


class ChatViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['post'])
    def create_chat(self, request):
        data_to_serialize = {'user1Id': request.user.id, 'user2Id': request.data.get('userId')}
        serializer = ChatCreateSerializer(data=data_to_serialize)
        if serializer.is_valid():
            serializer.save()
            return Response(None, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def create_group(self, request):
        data_to_serialize = {
            **request.data,
            'owner_id': request.user.id,
            'type': Chat.Type.GROUP
        }
        serializer = GroupChannelCreateSerializer(data=data_to_serialize)
        if serializer.is_valid():
            serializer.save()
            return Response(None, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def create_channel(self, request):
        data_to_serialize = {
            **request.data,
            'owner_id': request.user.id,
            'type': Chat.Type.CHANNEL
        }
        serializer = GroupChannelCreateSerializer(data=data_to_serialize)
        if serializer.is_valid():
            serializer.save()
            return Response(None, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        chats = Chat.objects.filter(chatuserm2m__user=request.user).prefetch_related('users')
        chats = [{
            **chat.__dict__,
            'name': chat.name if chat.name else next(filter(lambda x: x != request.user, chat.users.all())).username,
            'settings': next(filter(lambda x: x.user == request.user, chat.chatuserm2m_set.all()))
        } for chat in list(chats)]
        serializer = ChatShortSerializer(chats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
