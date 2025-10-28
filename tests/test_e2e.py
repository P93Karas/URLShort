import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_full_flow(api_client, valid_url):

    create_url = reverse("shorten-url")
    response_create = api_client.post(
        create_url, {"original_url": valid_url}, format="json"
    )
    assert response_create.status_code == status.HTTP_201_CREATED
    short_url_code = response_create.data["short_url"]

    retrieve_url = reverse("un-shorten-url", args=[short_url_code])
    response_retrieve = api_client.get(retrieve_url)
    assert response_retrieve.status_code == status.HTTP_200_OK
    assert response_retrieve.data["original_url"] == valid_url

    redirect_url = reverse("redirect-short-url", args=[short_url_code])
    response_redirect = api_client.get(redirect_url, follow=False)
    assert response_redirect.status_code == 302
    assert response_redirect.url == valid_url
