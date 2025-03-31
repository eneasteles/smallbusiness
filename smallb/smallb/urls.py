from django.contrib import admin
from django.urls import path, include
from cadastro.api import api  # ou onde estiver o arquivo api.py

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/", api.urls),  # Django Ninja aqui

]

