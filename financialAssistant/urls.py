from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("paginasweb.urls")),    #páginas estáticas
    path("core/", include("core.urls")),     #CRUD de domínio
    path("", include("user.urls")),     #URLs de usuário
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
