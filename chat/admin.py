from django.contrib import admin

from .models import Chat, ChatUserM2M


class UsersInline(admin.TabularInline):
    model = ChatUserM2M
    fields = ("user", "role")
    autocomplete_fields = ("user",)
    extra = 0


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("__str__", "type")
    inlines = (UsersInline,)
    search_fields = ("__str__",)


@admin.register(ChatUserM2M)
class ChatUserM2MAdmin(admin.ModelAdmin):
    autocomplete_fields = ("user", 'chat')
