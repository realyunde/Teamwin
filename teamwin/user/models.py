from django.db import models


class User(models.Model):
    name = models.CharField(
        null=False,
        unique=True,
        blank=False,
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

    @classmethod
    def get_by_name(cls, name):
        try:
            account = cls.objects.get(name=name)
        except cls.DoesNotExist:
            account = None
        return account

    @classmethod
    def get_by_id(cls, userid):
        try:
            user = cls.objects.get(id=userid)
        except cls.DoesNotExist:
            user = None
        return user

    @classmethod
    def user_exists(cls, userid):
        if cls.get_by_id(userid) is None:
            return False
        return True

    @classmethod
    def email_exists(cls, email):
        try:
            user = cls.objects.get(email=email)
        except cls.DoesNotExist:
            user = None
        return user
