from django.core.exceptions import ValidationError

from .models import ReferralHit, ReferralLink
from .settings import REFERRAL_COOKIE_KEY, REFERRAL_URL_PARAM


class AnonymousReferralMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)

		if request.user.is_authenticated:
			if REFERRAL_COOKIE_KEY in request.cookies:
				value = request.cookies[self.REFERRAL_COOKIE_KEY]
				try:
					ReferralHit.objects.filter(uuid=value).update(user=request.user)
				except ValidationError:
					# A bad ID was stored in the cookie (non-uuid)
					pass
				response.delete_cookie(self.REFERRAL_COOKIE_KEY)

		return response


class ReferralLinkMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		if request.method == "GET" and REFERRAL_URL_PARAM in request.GET:
			ref_id = request.GET[REFERRAL_URL_PARAM]
			try:
				ref_link = ReferralLink.objects.get(identifier=ref_id)
			except ReferralLink.DoesNotExist:
				return self.get_response(request)

			params = request.GET.copy()
			del params[REFERRAL_URL_PARAM]
			orig_path = makeparams(request.path, params)

			final_path = makeparams(ref_link.get_absolute_url(), {"next": orig_path})

			return redirect(final_path)

		# Check the original IP; only proceed if it's not a "real" IP
		ip = request.META.get("REMOTE_ADDR", "127.0.0.1")
		if ip in self.INTERNAL_IPS and self.HEADER in request.META:
			value = request.META[self.HEADER]
			# HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs. The
			# client's IP will be the first one.
			real_ip = value.split(",")[0].strip()
			request.META["REMOTE_ADDR"] = real_ip

		response = self.get_response(request)
		return response
