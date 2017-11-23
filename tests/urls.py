from django.conf.urls import url

from django_reflinks.views import ReferralView


urlpatterns = [
	url(r"^ref/(?P<id>\w+)$", ReferralView.as_view()),
]
