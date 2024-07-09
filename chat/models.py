from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

user_model = get_user_model()


class Chat(models.Model):
    """Модель чата"""
    name = models.CharField(max_length=120, null=True, blank=True, verbose_name='название')
    logo = models.ImageField(upload_to='chat_logo/%Y/%m/%d', null=True, blank=True, verbose_name='аватарка')
    users = models.ManyToManyField(to=user_model, through='ChatUserM2M', related_name='chats', verbose_name='участники')

    # Настройки чата (тип чата, публичный он или закрытый...)
    class Type(models.TextChoices):
        CHAT = "CT", _("Чат")
        GROUP = "GP", _("Группа")
        CHANNEL = "CL", _("Канал")

    type = models.CharField(max_length=2, choices=Type.choices, default=Type.CHAT, verbose_name='тип')
    public = models.BooleanField(default=False, blank=True, verbose_name='публичный')

    class Meta:
        verbose_name = 'чат'
        verbose_name_plural = 'чаты'

    def __str__(self):
        if self.name:
            return self.name
        elif len(self.users.all()):
            return " и ".join([str(user) for user in self.users.all()])
        else:
            return "Пустой"

    def clean(self):
        if self.type == self.Type.CHAT and self.name is not None:
            raise ValidationError(_("У чата не может быть названия"))

        if self.type == self.Type.CHAT and self.public:
            raise ValidationError(_("Чат не может быть публичным"))

        if self.type != self.Type.CHAT and self.name is None:
            raise ValidationError(_("Для группы и канала поле название обязательно"))


class ChatUserM2M(models.Model):
    """Связь чата и пользователя (пользователь состоит в определенном чате)"""
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, verbose_name='чат')
    user = models.ForeignKey(user_model, on_delete=models.CASCADE, verbose_name='пользователь')

    # Настройки чата от лица пользователя (роль пользователя в чате, получать ли уведомления...)
    class Role(models.TextChoices):
        OWNER = "O", _("Владелец")
        ADMIN = "A", _("Админ")
        USER = "U", _("Пользователь")

    role = models.CharField(max_length=1, choices=Role.choices, default=Role.USER, verbose_name='роль')
    notifications = models.BooleanField(default=True, verbose_name='уведомления')

    class Meta:
        verbose_name = 'чат пользователя'
        verbose_name_plural = 'чаты пользователей'
        unique_together = ('chat', 'user')

    def __str__(self):
        return f'Пользователь: {self.user}, чат: {self.chat}'
