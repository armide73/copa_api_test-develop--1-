from datetime import timedelta
import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField
import nanoid
from django.utils import timezone

from copa.settings import FRONTEND_URL
from copa.utils.app_utils.sms import send_sms

from ...models import BaseModel
from ...apps.authentication.models import User


class Cooperative(BaseModel):
    code = models.CharField(
        max_length=50, unique=True, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    province = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    sector = models.CharField(max_length=100, null=True, blank=True)
    creator = models.OneToOneField(
        User, on_delete=models.CASCADE,
        null=True, blank=True, related_name="cooperatives")
    kudibooks_company_id = models.CharField(
        max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Cooperatives"

    def __str__(self):
        return self.name

    def get_service(self, service):
        return self.enabled_services.filter(service=service).first()
    
    def is_service_enabled(self, service):
        return self.enabled_services.filter(service=service).exists()


class CooperativeField(BaseModel):
    cooperative = models.ForeignKey(
        Cooperative,
        on_delete=models.CASCADE,
        null=False, related_name="cooperative_fields")
    key = models.CharField(max_length=255, unique=True)
    placeholder = models.CharField(max_length=255, null=True, blank=True)
    field_type = models.CharField(max_length=255, null=True, blank=True)
    select_options = ArrayField(models.CharField(
        max_length=255,
        null=False,
        blank=False),
        null=True,
        blank=True)
    is_required = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        verbose_name_plural = "CooperativeFields"

    def __str__(self):
        return self.key


class CooperativeMeta(BaseModel):
    cooperative = models.ForeignKey(
        Cooperative,
        on_delete=models.CASCADE,
        null=False, related_name="cooperative_meta")
    key = models.CharField(max_length=200, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "CooperativeMeta"

    def __str__(self):
        return self.key


def nameFile(instance, filename):
    return '/'.join(['images', str(instance.name), filename])


class Member(BaseModel):
    cooperative = models.ForeignKey(
        Cooperative,
        on_delete=models.CASCADE,
        null=False, related_name="members")
    full_name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(
        max_length=50,
        default=None,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Gabo', 'Gabo'),
            ('Gore', 'Gore'),
            ('', '')],
        null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    identity_card = models.CharField(max_length=100, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    keywords = models.CharField(max_length=255, null=True, blank=True)
    kudi_books_id = models.CharField(max_length=100, null=True, blank=True)
    verification_token = models.CharField(max_length=255, null=True, blank=True)
    verification_token_expires_in = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Members"

    def __str__(self):
        """String representation of the model"""
        return self.full_name

    @property
    def amazina(self):
        """Display member's name"""
        return self.full_name

    def save(self, *args, **kwargs):
        self.keywords = '{} {} {}'.format(
            self.full_name,
            self.identity_card,
            self.mobile).lower()
        super().save(*args, **kwargs)

    def generate_verification_token(self):
        """Generate a verification token"""
        token = nanoid.generate(size=10)
        expires_in = timezone.now() + timedelta(minutes=30)
        self.verification_token = str(token)
        self.verification_token_expires_in = expires_in
        self.save()
        return token

    def send_verification_link_sms(self):
        """Send verification link to member"""
        token = self.generate_verification_token()
        message = f'Hi {self.full_name}, please click here {FRONTEND_URL}/members/{self.id}/verification/{token} to confirm {self.cooperative.name} membership'
        send_sms(self.mobile, message, 'COPA')

    def verify_membership(self, token):
        """Verify membership"""
        # check if token expired
        now = timezone.now()

        if not self.verification_token_expires_in:
            raise Exception('Verification link expired')

        if self.verification_token_expires_in < now:
            raise Exception('Verification link expired')

        if self.verification_token == token:
            self.verification_token = None
            self.is_verified = True
            self.save()
            return True
        else:
            raise Exception('Invalid verification link')


class MemberField(BaseModel):
    cooperative = models.ForeignKey(
        Cooperative, on_delete=models.CASCADE, null=True, blank=True)
    key = models.CharField(max_length=255)
    placeholder = models.CharField(max_length=255, null=True, blank=True)
    field_type = models.CharField(
        max_length=255,
        choices=[
            ('text', 'text'),
            ('checkbox', 'checkbox'),
            ('radio', 'radio'),
            ('number', 'number'),
            ('email', 'email'),
            ('date', 'date')
        ],
        null=True, blank=True)
    select_options = ArrayField(models.CharField(
        max_length=255,
        null=False,
        blank=False),
        null=True,
        blank=True)
    is_required = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        verbose_name_plural = "MemberFields"

    def __str__(self):
        return '{}'.format(self.cooperative)


class MemberMeta(BaseModel):
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        null=False, related_name="member_meta"
    )
    key = models.CharField(max_length=200, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "MemberMeta"
        unique_together = ['member', 'key']

    def __str__(self):
        return self.key


class EnabledServices(BaseModel):
    cooperative = models.ForeignKey(
        Cooperative,
        on_delete=models.CASCADE,
        null=False, related_name="enabled_services")
    service = models.CharField(max_length=255, null=True, blank=True)
    is_enabled = models.BooleanField(default=True, null=False, blank=False)
    subscription_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    subscription_status = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=[
            ('active', 'active'),
            ('inactive', 'inactive'),
            ('expired', 'expired'),
            ('', '')], default="active")

    class Meta:
        verbose_name_plural = "EnabledServices"

    def __str__(self):
        return self.service

class CooperativeEmployee(models.Model):
    cooperative=models.ForeignKey(Cooperative,on_delete=models.CASCADE,null=True)
    names=models.CharField(max_length=100, blank=False)
    employee_id=models.CharField(max_length=100, unique=True, blank=False)
    address=models.TextField(blank=True)
    phone_number=models.CharField(max_length=70,blank=False)

    def __str__(self):
        return self.names
    

