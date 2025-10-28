from rest_framework import serializers
from .models import ShortURL
from urllib.parse import urlparse


class ShortURLSerializer(serializers.ModelSerializer):

    full_short_url = serializers.SerializerMethodField(read_only=True)

    original_url = serializers.URLField(
        required=True,
        allow_blank=False,
        help_text="Enter a valid URL starting with http:// or https://",
    )

    class Meta:
        model = ShortURL
        fields = ["id", "original_url", "short_url", "full_short_url", "created_at"]
        read_only_fields = ["id", "short_url", "full_short_url", "created_at"]

    def get_full_short_url(self, obj) -> str:
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/shrt/{obj.short_url}/")
        return f"https://example.com/shrt/{obj.short_url}"

    def validate_original_url(self, value: str) -> str:
        parsed = urlparse(value)
        if parsed.scheme not in ("http", "https"):
            raise serializers.ValidationError("URL must start with http:// or https://")
        if not parsed.netloc:
            raise serializers.ValidationError("URL must have a valid domain")
        return value


class ShortURLRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ["original_url"]
