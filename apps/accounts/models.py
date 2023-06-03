from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from apps.accounts.choice import UserType
from apps.accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    User Model Class
    """
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)

    user_type = models.CharField(max_length=20, default=UserType.STUDENT.value,
                                 help_text="can be 'super-admin', 'teacher', 'student'",
                                 db_index=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    # here username_field is django defined field in account model, used for account identification.
    USERNAME_FIELD = 'email'

    # list of the field names that will be prompted for when creating a account via the
    # createsuperuser management command.
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return str(self.email)

