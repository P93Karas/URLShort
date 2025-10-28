import uuid
from django.db import IntegrityError, models
from url_short.utils import generate_short_url
from django.conf import settings


class ShortURL(models.Model):
    original_url = models.URLField(unique=True)
    short_url = models.CharField(max_length=12, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.short_url} -> {self.original_url}"

    def save(self, *args, **kwargs) -> None:
        is_new = self.pk is None
        previous_url = None
        existing = ShortURL.objects.filter(original_url=self.original_url).first()

        if not is_new:
            old = ShortURL.objects.filter(pk=self.pk).first()
            if old:
                previous_url = old.original_url

        if is_new and existing:
            self.pk = existing.pk
            self.short_url = existing.short_url
            super().save(update_fields=[])  # do nothing else
            return

        if previous_url != self.original_url:
            salt = settings.SHORT_URL_SALT
            self.short_url = generate_short_url(self.original_url, salt)

            for _ in range(settings.SHORT_GENERATION_RETRIES):

                if (
                    not ShortURL.objects.filter(short_url=self.short_url)
                    .exclude(pk=self.pk)
                    .exists()
                ):
                    break

                self.short_url = generate_short_url(
                    self.original_url, f"{salt}:{uuid.uuid4()}"
                )
            else:
                raise IntegrityError(
                    "Unable to generate unique short_url after several attempts"
                )

        super().save(*args, **kwargs)
