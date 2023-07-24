from django.contrib import admin

from bot.models import TGUser


@admin.register(TGUser)
class TGUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'user')
    readonly_fields = ['verification_code']
    search_fields = ['chat_id']
