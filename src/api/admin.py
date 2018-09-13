from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Channel, UserInfo


class UserInfoInline(admin.StackedInline):
    model = UserInfo
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UserInfoInline,)


admin.site.register(Channel)
admin.site.register(UserInfo)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
