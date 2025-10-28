from django.shortcuts import get_object_or_404, redirect
from django.views import View
from rest_framework import generics, status
from .models import ShortURL
from .serializers import ShortURLSerializer, ShortURLRetrieveSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ShortURLCreateView(generics.CreateAPIView):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer

    @swagger_auto_schema(
        operation_summary="Create a shortened URL",
        operation_description="Receives a long URL and returns a shortened URL code.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ShortURLListView(generics.ListAPIView):
    queryset = ShortURL.objects.all().order_by("-created_at")
    serializer_class = ShortURLSerializer

    @swagger_auto_schema(
        operation_summary="List all shortened URLs",
        operation_description="Returns a list of all shortened URLs with original URLs",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ShortURLRetrieveView(generics.GenericAPIView):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLRetrieveSerializer
    lookup_field = "short_url"

    @swagger_auto_schema(
        operation_summary="Get original URL from short code",
        operation_description="Reverse lookup to get the original URL using the short URL code.",
        manual_parameters=[
            openapi.Parameter(
                "short_url",
                openapi.IN_PATH,
                description="Short code of the URL",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={200: ShortURLRetrieveSerializer},
    )
    def get(self, request, short_url: str):
        obj = get_object_or_404(self.get_queryset(), short_url=short_url)
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShortURLRedirectView(View):
    def get(self, request, short_url: str):
        url = get_object_or_404(ShortURL, short_url=short_url)
        return redirect(url.original_url)
