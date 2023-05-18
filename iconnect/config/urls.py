from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import redirect_to_user_acc

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_user_acc),
    path('posts/', include('posts.urls')),
    path('accounts/', include('accounts.urls')),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

