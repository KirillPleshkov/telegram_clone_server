from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

user_model = get_user_model()


@admin.register(user_model)
class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm

    list_display = ('username', 'first_last_name', 'is_active',)
    list_filter = ('is_staff', 'is_active',)

    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Информация', {'fields': ('first_name', 'last_name', 'email', 'account_status', 'image')}),
        ('Права', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
         ),
    )

    def first_last_name(self, obj):
        return f'{obj.first_name} {obj.last_name}' if obj.first_name and obj.last_name else ''

    first_last_name.short_description = 'Имя и фамилия'


admin.site.unregister(Group)

