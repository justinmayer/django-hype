from django.urls import re_path

from .views import ReferralView


# app_name = "django_reflinks"

urlpatterns = [
	re_path(r"^(?P<identifier>\w+)$", ReferralView.as_view(), name="django_reflinks_reflink"),
]
