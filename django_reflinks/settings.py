"""
Settings for django-reflinks
"""

REFERRAL_COOKIE_KEY = "django-reflinks__rk"
REFERRAL_COOKIE_HTTPONLY = True
REFERRAL_COOKIE_MAX_AGE = None  # Expires at session end
REFERRAL_URL_PARAM = "ref"
