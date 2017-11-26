from django.conf.urls import url

from .views import ReferralView


# app_name = "django_reflinks"

urlpatterns = [
	url(r"^(?P<identifier>\w+)$", ReferralView.as_view(), name="django_reflinks_reflink"),
]
