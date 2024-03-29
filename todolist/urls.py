from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('bot/', include('bot.urls', namespace='bot')),
    path("oauth/", include("social_django.urls", namespace="social")),
    path("goals/", include("goals.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
