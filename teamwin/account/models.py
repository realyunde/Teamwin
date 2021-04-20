from django.db import models


class Account(models.Model):
    name = models.CharField(
        unique=True,
        max_length=255,
    )
    email = models.EmailField(
        null=False,
        blank=False,
        unique=True,
    )
    token = models.CharField(
        null=True,
        blank=True,
        default=None,
        max_length=200,
    )
