from django.urls import re_path

from .views import ReferralView


# app_name = "hype"

urlpatterns = [
    re_path(r"^(?P<identifier>\w+)$", ReferralView.as_view(), name="hype_reflink"),
]
