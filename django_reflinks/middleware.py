from .models import ReferralHit, ReferralLink


class AnonymousReferralMiddleware:
	REFERRAL_COOKIE_KEY = "django-reflinks__rk"

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		if request.user.is_authenticated:
			if self.REFERRAL_COOKIE_KEY in request.cookies:
				value = request.cookies[self.REFERRAL_COOKIE_KEY]
				# XXX test with invalid uuid
				hits = ReferralHit.objects.filter(uuid=value).update(user=request.user)
				delete_cookie(self.REFERRAL_COOKIE_KEY, request)

		response = self.get_response(request)
		return response


class ReferralLinkMiddleware:
	REFERRAL_KEY = "ref"

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		if request.method == "GET" and self.REFERRAL_KEY in request.GET:
			ref_id = request.GET[self.REFERRAL_KEY]
			try:
				ref_link = ReferralLink.objects.get(identifier=ref_id)
			except ReferralLink.DoesNotExist:
				return self.get_response(request)

			params = request.GET.copy()
			del params[self.REFERRAL_KEY]
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
