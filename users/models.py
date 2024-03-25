from django.db import models, IntegrityError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, firstname, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, firstname, password, **other_fields)

    def create_user(self, email, username, firstname='', password=None, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, firstname=firstname, **other_fields)
        user.set_password(password)

        try:
            user.save()
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e):
                # Handle unique constraint violation error
                if 'email' in str(e):
                    raise ValueError(_('This email address is already in use.'))
                elif 'username' in str(e):
                    raise ValueError(_('This username is already taken.'))
            else:
                raise  # Re-raise the exception if it's not a unique constraint violation error

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    firstname = models.CharField(max_length=150, blank=True)
    lastname = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'firstname']

    def __str__(self):
        return f"{self.email} | {self.username}"
