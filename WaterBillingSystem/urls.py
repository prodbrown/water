from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('water@/admin/', admin.site.urls),
    path('', include('accounts.urls')),  # URLs for accounts app
    path('', include('bills.urls')),  # URLs for bills app
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
