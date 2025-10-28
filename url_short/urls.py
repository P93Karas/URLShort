from django.shortcuts import redirect
from django.urls import path
from .views import (
    ShortURLCreateView,
    ShortURLListView,
    ShortURLRedirectView,
    ShortURLRetrieveView,
)

urlpatterns = [
    path("api/v1/url/shorten/", ShortURLCreateView.as_view(), name="shorten-url"),
    path(
        "api/v1/url/unshorten/<str:short_url>",
        ShortURLRetrieveView.as_view(),
        name="un-shorten-url",
    ),
    path("api/v1/url/list/", ShortURLListView.as_view(), name="list-short-url"),
    path(
        "shrt/<str:short_url>/",
        ShortURLRedirectView.as_view(),
        name="redirect-short-url",
    ),
    path("", lambda request: redirect("schema-swagger-ui")),
]
