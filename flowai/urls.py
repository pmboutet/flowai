from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ai_middleware.urls')),
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    path('', include('social_django.urls', namespace='social')),  # Ajout des URLs d'authentification sociale
]