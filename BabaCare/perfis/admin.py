from django.contrib import admin
from .models import Perfil_Baba, Agenda

# Register your models here.

admin.site.register(Perfil_Baba)


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('baba', 'dia', 'periodo')
    list_filter = ('baba', 'dia', 'periodo')
    search_fields = ('baba__username',)