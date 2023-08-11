from django.db import models
from django.utils import timezone

# Create your models here.


class TimeStampedModel(models.Model):
    """Time Stamped Model"""

    created = models.DateTimeField(
        default=timezone.now, null=True, verbose_name="생성시각")
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name="수정시각")

    class Meta:
        abstract = True
