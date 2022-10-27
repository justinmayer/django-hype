import pytest

from hype import settings
from hype.models import ReferralHit


@pytest.mark.django_db
def test_anonymous_middleware(client, admin_user, ref_link):
    ref_link_url = ref_link.get_absolute_url()

    response = client.get(ref_link_url, HTTP_USER_AGENT="TestAgent")
    assert response.status_code == 302
    assert response.url == "/"

    assert ReferralHit.objects.count() == 1
    hit = ReferralHit.objects.latest("created")
    assert not hit.authenticated
    assert not hit.hit_user

    cookie = response.cookies[settings.COOKIE_KEY]
    assert cookie.value == str(hit.pk)

    client.force_login(admin_user)
    response = client.get("/foo")
    assert ReferralHit.objects.count() == 1
    assert response.status_code == 404

    # Cookie should have been deleted
    assert response.cookies[settings.COOKIE_KEY].value == ""

    # And old request should have been updated
    hit = ReferralHit.objects.get(pk=hit.pk)
    assert hit.hit_user == admin_user


def test_anonymous_middleware_bad_cookie(admin_client, ref_link):
    admin_client.cookies.load({settings.COOKIE_KEY: "looks nothing like a uuid"})
    response = admin_client.get("/foo")
    assert response.status_code == 404

    admin_client.cookies.load(
        {settings.COOKIE_KEY: "00000000-0000-0000-0000-000000000000"}
    )
    response = admin_client.get("/foo")
    assert response.status_code == 404


def test_referral_link_middleware(admin_client, ref_link):
    ref_link_url = ref_link.get_absolute_url()

    response = admin_client.get("/foo?ref=" + ref_link.identifier)
    assert response.status_code == 302
    assert response.url == ref_link_url + "?next=%2Ffoo"

    response = admin_client.post("/foo?ref=" + ref_link.identifier)
    assert response.status_code == 404
