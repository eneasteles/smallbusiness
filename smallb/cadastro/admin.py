from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Perfil, Categoria, Lancamento

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'celular')
    search_fields = ('user__username', 'celular')

admin.site.register(Categoria)
admin.site.register(Lancamento)
