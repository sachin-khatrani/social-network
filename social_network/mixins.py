from django.db import models
from django.utils import timezone

class TimestampMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created = timezone.now()
        self.modified = timezone.now()
        super().save(*args, **kwargs)