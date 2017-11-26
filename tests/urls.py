from django.conf.urls import url
from django.contrib import admin

from django_reflinks.views import ReferralView


urlpatterns = [
	url(r"^admin/", admin.site.urls),
	url(r"^ref/(?P<id>\w+)$", ReferralView.as_view()),
]
