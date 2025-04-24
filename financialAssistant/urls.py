from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("paginasweb.urls")),    #páginas estáticas
    path("core/", include("core.urls")),     #CRUD de domínio
]
