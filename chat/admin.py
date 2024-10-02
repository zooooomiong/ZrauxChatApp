from django.contrib import admin
from .models import DuoChat, DuoMessage

admin.site.register(DuoChat)


@admin.register(DuoMessage)
class  DuoMessageAdmin(admin.ModelAdmin):
    list_filter=("created_at",)
    ordering = ("created_at",)
