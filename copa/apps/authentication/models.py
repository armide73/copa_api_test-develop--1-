from django.db import models

# Create your models here.
from django.db import migrations
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.utils import timezone
from django.db.models import F
from django.utils.translation import gettext as _

from copa.manager import BaseManager
from copa.utils.app_utils.generators import id_generater, ID_LENGTH
from django.contrib.postgres.operations import CreateExtension
from copa.models import BaseModel
from django.contrib.postgres.fields import ArrayField


class Migration(migrations.Migration):

    operations = [
        CreateExtension('postgis'),
        ...
    ]


class UserManager(BaseUserManager, BaseManager):
    """
    User Manager class
    """

    def create_user(self, **kwargs):
        """
        Create a user method
        """
        names = kwargs.get("names")
        phone_number = kwargs.get("phone_number")
        email = kwargs.get("email")
        password = kwargs.get("password")

        check_email = self.model.objects.filter(email=email).first()
        check_phone_number = self.model.objects.filter(
            phone_number=phone_number,
        ).first()
        if check_email:
            raise ValueError(
                _("User ufite email {} arahari".format(email))
            )

        if phone_number and check_phone_number:
            raise ValueError(
                _("User ufite phone number {} arahari".format(phone_number))
            )

        user = self.model(
            names=names,
            phone_number=phone_number,
            email=self.normalize_email(email),
            country=kwargs.get("country"),
        )
        user.set_password(password)
        user.keywords = \
            "phone_number{} names{} email{} country{}"\
            .format(
                user.phone_number,
                user.names,
                user.email,
                user.country)
        user.is_active = True
        return user

    def create_superuser(self, email, password):
        """
        Create super user method to your default database
        """
        user = self.create_user(email=email, password=password)
        user.is_superuser = user.is_staff = True
        user.is_active = user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model
    """
    id = models.CharField(
        max_length=ID_LENGTH,
        primary_key=True,
        default=id_generater,
        editable=False,
    )
    phone_number = models.CharField(max_length=100, null=True, unique=True)
    email = models.EmailField(max_length=100, unique=True, null=True)
    password = models.CharField(max_length=100)
    names = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(auto_now_add=True, null=True)
    image = models.CharField(
        max_length=150, null=True, blank=True,
        default="https://res.cloudinary.com/julien/image/upload/"
        "v1594986765/user-avatar_nch70m.png")
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    keywords = models.CharField(max_length=255, null=True, blank=True)
    kudibooks_user_code = models.CharField(max_length=100, null=True, blank=True)

    objects = UserManager()
    all_objects = UserManager(alive_only=False)

    USERNAME_FIELD = "email"

    class Meta:
        """
        User's Meta data
        """
        verbose_name_plural = "Users"
        ordering = [F('email').asc(nulls_last=True)]

    def __str__(self):
        return self.email

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()

    def get_full_name(self):
        return '{}'.format(self.names)


class UserOtherField(BaseModel):
    id = models.CharField(
        max_length=ID_LENGTH,
        primary_key=True,
        default=id_generater,
        editable=False,
    )
    key = models.CharField(max_length=255, unique=True)
    placeholder = models.CharField(max_length=255)
    field_type = models.CharField(max_length=255)
    select_options = ArrayField(models.CharField(
        max_length=255,
        null=False,
        blank=False),
        null=True,
        blank=True)
    is_required = models.BooleanField(default=False, null=False, blank=False)
