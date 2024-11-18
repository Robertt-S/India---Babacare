from django.contrib import admin

from users.models import Baba, Responsavel

class ListandoBabas(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "verificado")
    list_display_links = ("id","nome")
    search_fields = ("nome",)
    list_filter = ("id",)
    list_editable = ("verificado",)
    list_per_page = 10

admin.site.register(Baba, ListandoBabas)


class ListandoResponsaveis(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "verificado")
    list_display_links = ("id","nome")
    search_fields = ("nome",)
    list_filter = ("id",)
    list_editable = ("verificado",)
    list_per_page = 10

admin.site.register(Responsavel, ListandoBabas)
