from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # Importação necessária
from django.conf.urls.static import static  # Importação necessária

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('starsite.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])


