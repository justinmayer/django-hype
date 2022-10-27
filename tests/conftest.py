import pytest

from hype.models import ReferralLink


@pytest.fixture(scope="function")
def ref_link():
    yield ReferralLink.objects.create(identifier="Example123")
