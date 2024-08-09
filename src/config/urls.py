from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

import config.settings.base as settings
from manage import DEBUG


urlpatterns = [
    path('api/', include('apps.drf_utils.urls')),
    path('api/', include('apps.warehouses.urls')),
    path('api/', include('apps.api.urls')),
    path('api/', include('apps.accounts.urls')),
    path('api/', include('apps.tasks.urls')),
    path('admin/', admin.site.urls),
]


if DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
