from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import the custom dashboard view
from app.views import admin_dashboard

urlpatterns = [
    # Custom dashboard URL - completely separate from admin
    path('dashboard/', admin_dashboard, name='custom_dashboard'),
    
    # Django admin
    path('admin/', admin.site.urls),
    
    # ERP modules
    path('erp/', include('app.urls')),
    
    # Website URLs
    path('', include('website.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
