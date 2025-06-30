from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ultralg.core.urls')),   # inclui as URLs da app core na raiz
]