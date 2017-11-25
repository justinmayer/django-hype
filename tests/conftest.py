import pytest

from django_reflinks.models import ReferralLink


@pytest.yield_fixture(scope="function")
def ref_link():
	yield ReferralLink.objects.create(identifier="Example123")
