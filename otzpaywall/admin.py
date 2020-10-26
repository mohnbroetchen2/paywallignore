from django.contrib import admin
from .models import Url
# Register your models here.

@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    """
    ChangeAdmin for Change model
    """
    list_display = ('url', 'ofile', 'pfile',)
    search_fields = ('url', 'ofile', 'pfile',)
    ordering = ('url', 'ofile', 'pfile',)
