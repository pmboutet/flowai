from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import RedirectView

schema_view = get_schema_view(
    openapi.Info(
        title="FlowAI API",
        default_version='v1',
        description="API documentation for FlowAI",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@flowai.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
    url=f'https://127.0.0.1:8000' if settings.DEBUG else None
)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin-site'),
    path('api/', include('ai_middleware.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
    
    # API Documentation
    path('api/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Root URL
    path('', RedirectView.as_view(url='/admin/'), name='index'),
]