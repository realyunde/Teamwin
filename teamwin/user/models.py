import hashlib
from django.db import models


def make_token(password):
    if not isinstance(password, (bytes, str)):
        raise TypeError('Password must be a string or bytes.')
    if isinstance(password, str):
        password = password.encode('utf-8')
    return hashlib.md5(password).hexdigest()


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
            return cls.objects.get(name=name)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_by_id(cls, userid):
        try:
            return cls.objects.get(id=userid)
        except cls.DoesNotExist:
            return None

    @classmethod
    def user_exists(cls, userid):
        if cls.get_by_id(userid) is None:
            return False
        return True

    @classmethod
    def name_exists(cls, name):
        if cls.get_by_name(name) is None:
            return False
        return True

    @classmethod
    def email_exists(cls, email):
        try:
            user = cls.objects.get(email=email)
        except cls.DoesNotExist:
            user = None
        return False if user is None else True

    @classmethod
    def auth_user(cls, name, password):
        user = cls.get_by_name(name)
        if user is None:
            return False
        if user.token != make_token(password):
            return False
        return True

    @classmethod
    def create_user(cls, name, email, password):
        return cls.objects.create(
            name=name,
            email=email,
            token=make_token(password),
        )

    def set_password(self, password):
        self.password = make_token(password)
