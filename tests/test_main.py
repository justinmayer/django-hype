import pytest

from django_reflinks import settings
from django_reflinks.models import ReferralHit


@pytest.mark.django_db
def test_referral_logged_in(admin_client, ref_link):
	ref_link_url = ref_link.get_absolute_url()
	client = admin_client

	response = client.get(ref_link_url, HTTP_USER_AGENT="TestAgent")
	assert response.status_code == 302
	assert response.url == "/"
	assert response.cookies[settings.REFERRAL_COOKIE_KEY].value == ""

	assert ReferralHit.objects.count() == 1
	hit = ReferralHit.objects.latest("created")
	assert hit.authenticated
	assert hit.hit_user == response.wsgi_request.user
	assert hit.ip == "127.0.0.1"
	assert hit.user_agent == response.wsgi_request.META["HTTP_USER_AGENT"]
	assert not hit.next
	assert not hit.confirmed

	next = "/foo"
	response = client.get(ref_link_url + "?next=" + next)
	assert response.status_code == 302
	assert response.url == next

	assert ReferralHit.objects.count() == 2
	hit = ReferralHit.objects.latest("created")
	assert hit.authenticated
	assert hit.hit_user == response.wsgi_request.user
	assert hit.next == next
	assert not hit.confirmed
	assert response.cookies[settings.REFERRAL_COOKIE_KEY].value == ""


@pytest.mark.django_db
def test_referral_logged_out(client, ref_link):
	ref_link_url = ref_link.get_absolute_url()

	response = client.get(ref_link_url, HTTP_USER_AGENT="TestAgent")
	assert response.status_code == 302
	assert response.url == "/"

	assert ReferralHit.objects.count() == 1
	hit = ReferralHit.objects.latest("created")
	assert not hit.authenticated
	assert not hit.hit_user
	assert hit.ip == "127.0.0.1"
	assert hit.user_agent == response.wsgi_request.META["HTTP_USER_AGENT"]
	assert not hit.next
	assert not hit.confirmed

	cookie = response.cookies[settings.REFERRAL_COOKIE_KEY]
	assert cookie.value == str(hit.pk)

	next = "/foo"
	response = client.get(ref_link_url + "?next=" + next)
	assert response.status_code == 302
	assert response.url == next

	assert ReferralHit.objects.count() == 2
	hit = ReferralHit.objects.latest("created")
	assert not hit.authenticated
	assert not hit.hit_user
	assert hit.next == next
	assert not hit.confirmed

	cookie = response.cookies[settings.REFERRAL_COOKIE_KEY]
	assert cookie.value == str(hit.pk)
