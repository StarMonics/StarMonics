from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # Importação necessária
from django.conf.urls.static import static  # Importação necessária

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('starsite.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]

# Adicione esta configuração para servir arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
