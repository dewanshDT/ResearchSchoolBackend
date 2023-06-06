from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("scholar/", include("scholar.urls")),
]

handler404 = "scholar.views.custom_404_view"
