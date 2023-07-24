from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('clone/', include('quora_duplicated.urls')),
    path('admin/', admin.site.urls),
]
