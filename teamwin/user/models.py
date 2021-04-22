import hashlib
from django.db import models


def make_password(password):
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
        return False if user is None else True

    @classmethod
    def create_user(cls, name, email, password):
        token = make_password(password)
        try:
            user = cls(
                name=name,
                email=email,
                token=token
            )
            user.save()
        except:
            user = None
        return user

    @classmethod
    def auth_user(cls, name, password):
        user = cls.get_by_name(name)
        if user is None:
            return False
        if user.token != make_password(password):
            return False
        return True

    def set_password(self, password):
        self.password = make_password(password)
