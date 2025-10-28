import pytest
from rest_framework.test import APIClient
from url_short.models import ShortURL


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def valid_url():
    return "https://www.djangoproject.com/"


@pytest.fixture
def short_url_instance(valid_url):
    return ShortURL.objects.create(original_url=valid_url)
