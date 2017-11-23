from django.utils.http import is_safe_url
from django.utils.shortcuts import redirect
from django.views import View

from .models import ReferralHit, ReferralLink


class ReferralView(View):
	success_url = "/"

	def get(self, request, id):
		try:
			ref_link = ReferralLink.objects.get(identifier=id)
		except ReferralLink.DoesNotExist:
			# metrics.send("broken_referral", ...)
			return self.fail("broken_referral")

		if ref_link.disabled:
			return self.fail("referral_disabled")

		return self.success(ref_link)

	def get_success_url(self):
		success_url = self.request.GET.get("next", "")
		if success_url and is_safe_url(success_url):
			return success_url
		return self.success_url

	def success(self, ref_link):
		self.hit(ref_link)
		return redirect(self.get_success_url())

	def fail(self, code):
		return redirect(self.get_success_url())

	def hit(self, ref_link):
		user = self.request.user if self.request.user.is_authenticated else None
		ip = self.request.META["REMOTE_ADDR"]
		ua = self.request.META.get("HTTP_USER_AGENT", "")
		hit = ReferralHit.objects.create(
			referral_link=ref_link, hit_user=user, hit_ip=ip, hit_user_agent=ua
		)

		# TODO: set_cookie()
		return hit
