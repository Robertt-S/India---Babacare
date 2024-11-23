from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from users.models import BaseUser, Baba, Responsavel

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = BaseUser
        fields = ["email", "nome", "cpf", "nascimento", "telefone", "endereco"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Senhas nao batem")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class ListandoBabas(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "bioBaba")
    list_display_links = ("id","nome")
    search_fields = ("nome",)
    list_filter = ("id",)
    list_editable = ("bioBaba",)
    list_per_page = 10

admin.site.register(Baba, ListandoBabas)


class ListandoResponsaveis(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "bioResp")
    list_display_links = ("id","nome")
    search_fields = ("nome",)
    list_filter = ("id",)
    list_editable = ("bioResp",)
    list_per_page = 10

admin.site.register(Responsavel, ListandoResponsaveis)
