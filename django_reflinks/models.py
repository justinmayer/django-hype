from uuid import uuid4

from django.conf import settings
from django.db import models


COOKIE_KEY = "django_reflinks__rk"


class ReferralHitManager(models.Manager):
	pass


class ReferralLink(models.Model):
	identifier = models.CharField(max_length=50, blank=True, unique=True)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
	)
	disabled = models.BooleanField(default=False)

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def get_absolute_url(self):
		return "/ref/{}".format(self.identifier)


class ReferralHit(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	referral_link = models.ForeignKey(ReferralLink, on_delete=models.CASCADE)
	hit_user = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
	)
	ip = models.GenericIPAddressField(help_text="IP address at hit time")
	user_agent = models.TextField(blank=True, help_text="UA at hit time")
	next = models.URLField(blank=True, help_text="The ?next parameter when the link was hit.")

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)


class ConfirmedReferral(models.Model):
	referral_hit = models.ForeignKey(ReferralHit, on_delete=models.CASCADE)
	referred_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	ip = models.GenericIPAddressField(help_text="IP address at subscription time")
	user_agent = models.TextField(help_text="UA at subscription time")

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
