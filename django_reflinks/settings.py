"""
Settings for django-reflinks
"""

REFERRAL_COOKIE_KEY = "django-reflinks__rk"
REFERRAL_COOKIE_HTTPONLY = True
REFERRAL_COOKIE_MAX_AGE = 60 * 60 * 24 * 365
REFERRAL_URL_PARAM = "ref"
