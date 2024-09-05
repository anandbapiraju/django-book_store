from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib.auth import views as auth_views


schema_view = get_schema_view(
   openapi.Info(
      title="Book_Store API Endpoints",
      default_version='v1',
      description="This Book Store is helpful in purchasing books online through this site",

   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/', include('book_store_app.api.urls')),
]

# Internationalization and static file URL patterns
urlpatterns += i18n_patterns(
    path('', include(('book_store_app.urls', 'book_store_app'), namespace='book_store_app')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
