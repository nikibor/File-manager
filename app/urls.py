from django.contrib import admin
from django.urls import path, include

from file_manager import urls as file_manager_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(file_manager_urls))
]
