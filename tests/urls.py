from django.urls import include, re_path
from django.contrib import admin


urlpatterns = [
	re_path(r"^admin/", admin.site.urls),
	re_path(r"^ref/", include("django_reflinks.urls")),
]
