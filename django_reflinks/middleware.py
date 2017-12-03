from urllib.parse import urlencode
from uuid import UUID

from django.shortcuts import redirect

from .models import ReferralHit, ReferralLink
from .settings import COOKIE_KEY, URL_PARAM


class AnonymousReferralMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)

		if request.user and request.user.is_authenticated:
			if COOKIE_KEY in request.COOKIES:
				value = request.COOKIES[COOKIE_KEY]

				try:
					value = UUID(value)
				except ValueError:
					# A bad ID was stored in the cookie (non-uuid). Harmless.
					pass
				else:
					ReferralHit.objects.filter(pk=value, hit_user=None).update(
						hit_user=request.user
					)

				response.delete_cookie(COOKIE_KEY)

		return response


class ReferralLinkMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		if request.method == "GET" and URL_PARAM in request.GET:
			ref_id = request.GET[URL_PARAM]
			try:
				ref_link = ReferralLink.objects.get(identifier=ref_id)
			except ReferralLink.DoesNotExist:
				return self.get_response(request)

			params = request.GET.copy()
			del params[URL_PARAM]
			orig_path = request.path
			if params:
				orig_path += "?" + urlencode(params)

			final_path = ref_link.get_absolute_url() + "?" + urlencode({"next": orig_path})

			response = redirect(final_path)
		else:
			response = self.get_response(request)

		return response
