from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from chat.models import Chat, ChatUserM2M

user_model = get_user_model()


class ChatCreateSerializer(serializers.Serializer):
    user1Id = serializers.IntegerField()
    user2Id = serializers.IntegerField()

    def validate(self, attrs):
        get_object_or_404(user_model, id=attrs['user2Id'])

        if attrs['user1Id'] == attrs['user2Id']:
            raise serializers.ValidationError("Пользователи должны быть уникальны.")

        if len(ChatUserM2M.objects.filter(user_id=attrs['user1Id'], chat__chatuserm2m__user_id=attrs['user2Id'])):
            raise serializers.ValidationError("Такой чат уже существует")

        return attrs

    def create(self, validated_data):
        chat = Chat.objects.create(type=Chat.Type.CHAT)
        ChatUserM2M.objects.create(chat=chat, user_id=validated_data['user1Id'])
        ChatUserM2M.objects.create(chat=chat, user_id=validated_data['user2Id'])
        return chat


class GroupChannelCreateSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField()

    class Meta:
        model = Chat
        fields = ('name', 'logo', 'public', 'owner_id', 'type')
        extra_kwargs = {"name": {"required": True}}

    def create(self, validated_data):
        owner_id = validated_data.pop('owner_id')
        chat = Chat.objects.create(**validated_data)
        ChatUserM2M.objects.create(
            chat=chat,
            user_id=owner_id,
            role=ChatUserM2M.Role.OWNER
        )
        return chat


class ChatSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatUserM2M
        exclude = ('id', 'user', 'chat')


class ChatShortSerializer(serializers.ModelSerializer):
    settings = ChatSettingsSerializer()

    class Meta:
        model = Chat
        fields = ('id', 'name', 'type', 'settings')
