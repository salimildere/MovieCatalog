from django.contrib import admin

from .models import *


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title',)
    list_editable = ('title', 'is_active', 'order')
    readonly_fields = ("contents",)
