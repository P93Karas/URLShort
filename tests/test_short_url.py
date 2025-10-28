import pytest
from django.urls import reverse
from rest_framework import status

from url_short.models import ShortURL


@pytest.mark.django_db
def test_create_short_url_success(api_client, valid_url):
    url = reverse("shorten-url")
    response = api_client.post(url, {"original_url": valid_url}, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert "short_url" in response.data
    assert "full_short_url" in response.data
    assert response.data["original_url"] == valid_url


@pytest.mark.django_db
def test_create_short_url_invalid_url(api_client):
    url = reverse("shorten-url")
    response = api_client.post(url, {"original_url": "WRONG_URL"}, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "original_url" in response.data


@pytest.mark.django_db
def test_retrieve_original_url(api_client, short_url_instance, valid_url):
    url = reverse("un-shorten-url", args=[short_url_instance.short_url])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["original_url"] == valid_url


@pytest.mark.django_db
def test_redirect_short_url(api_client, short_url_instance, valid_url):
    url = reverse("redirect-short-url", args=[short_url_instance.short_url])
    response = api_client.get(url)

    assert response.status_code == 302
    assert response.url == valid_url


@pytest.mark.django_db
def test_create_same_url_returns_same_short_url(api_client, valid_url):
    url = reverse("shorten-url")
    response1 = api_client.post(url, {"original_url": valid_url}, format="json")
    response2 = api_client.post(url, {"original_url": valid_url}, format="json")

    assert response1.status_code == status.HTTP_201_CREATED
    assert response2.status_code == status.HTTP_201_CREATED
    assert response1.data["short_url"] == response2.data["short_url"]

    all_objs = ShortURL.objects.filter(original_url=valid_url)
    assert all_objs.count() == 1


@pytest.mark.django_db
def test_retrieve_nonexistent_short_url(api_client):
    retrieve_url = reverse("un-shorten-url", args=["EMPTY_CODE"])
    response = api_client.get(retrieve_url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_existing_url(api_client):
    original_url = "https://www.example.com/old"
    new_url = "https://www.example.com/new"

    obj = ShortURL.objects.create(original_url=original_url)
    old_short = obj.short_url

    obj.original_url = new_url
    obj.save()

    obj.refresh_from_db()
    assert obj.original_url == new_url
    assert obj.short_url != old_short

    retrieve_url = reverse("un-shorten-url", args=[obj.short_url])
    response = api_client.get(retrieve_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["original_url"] == new_url


@pytest.mark.django_db
def test_short_url_collision(api_client, monkeypatch):
    original_url1 = "https://www.example.com/1"
    original_url2 = "https://www.example.com/2"

    short_url1 = "ShortUrl1"
    short_url2 = "ShortUrl2"

    fixed_shorts = [short_url1, short_url2]

    monkeypatch.setattr(
        "url_short.models.generate_short_url", lambda url, salt: fixed_shorts[0]
    )

    obj1 = ShortURL.objects.create(original_url=original_url1)
    assert obj1.short_url == short_url1

    def generate_mock(url, salt):
        return fixed_shorts.pop(0)

    monkeypatch.setattr("url_short.models.generate_short_url", generate_mock)

    obj2 = ShortURL.objects.create(original_url=original_url2)
    assert obj2.short_url == short_url2
    assert obj2.short_url != obj1.short_url

    all_objs = ShortURL.objects.all()
    assert all_objs.count() == 2
    assert all_objs.filter(short_url=obj1.short_url).exists()
    assert all_objs.filter(short_url=obj2.short_url).exists()
