from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
]