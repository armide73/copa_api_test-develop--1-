from datetime import timedelta
from django.db import models
from copa.apps.cooperative.models import Cooperative, Member
from django.utils import timezone
from copa.models import BaseModel
from copa.utils.app_utils.sms import send_sms


class PeriodChoice(models.TextChoices):
    """Payment period choices"""

    DAILY = "daily", "Daily"
    WEEKLY = "weekly", "Weekly"
    MONTHLY = "monthly", "Monthly"
    QUARTERLY = "quarterly", "Quarterly"
    YEARLY = "yearly", "Yearly"


class SubscriptionStatus(models.TextChoices):
    """Substcription status"""

    ACTIVE = "active", "Active"
    EXPIRED = "expired", "Expired"
    CANCELLED = "cancelled", "Cancelled"


class InvoiceStatus(models.TextChoices):
    """Invoice Status"""

    PAID = "paid", "Paid"
    UNPAID = "unpaid", "Unpaid"
    PENDING_PAYMENT = "pending_payment", "Pending Payment"


# Create your models here.


class Pricing(BaseModel):
    """Pricing model"""

    title = models.CharField(max_length=255, null=False, blank=False)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )
    period = models.CharField(
        max_length=255, choices=PeriodChoice.choices, null=False, blank=False
    )
    cooperative = models.ForeignKey(
        Cooperative, on_delete=models.CASCADE, null=False, blank=False
    )
    is_active = models.BooleanField(default=True, null=False, blank=False)


class Benefit(BaseModel):
    """Pricing Benefit model"""

    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=False)
    pricing = models.ForeignKey(
        Pricing, on_delete=models.CASCADE, null=False, related_name="benefits"
    )
    cooperative = models.ForeignKey(
        Cooperative, on_delete=models.CASCADE, null=False, related_name="benefits"
    )


class Subscription(BaseModel):
    """User Subscription model"""

    cooperative = models.ForeignKey(
        Cooperative, on_delete=models.CASCADE, null=False, related_name="subscriptions"
    )
    pricing = models.ForeignKey(
        Pricing, on_delete=models.CASCADE, null=False, related_name="subscriptions"
    )
    subscription_date = models.DateTimeField(null=False, blank=False)
    expiry_date = models.DateTimeField(null=False, blank=False)
    subscription_status = models.CharField(
        max_length=255,
        choices=SubscriptionStatus.choices,
        null=False,
        default=SubscriptionStatus.ACTIVE,
    )
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, null=False, related_name="subscriptions"
    )

    @staticmethod
    def get_expiry_date(period, subscription_date):
        """Calculate expiry date based on period"""
        if period == PeriodChoice.DAILY:
            return subscription_date + timedelta(days=1)
        if period == PeriodChoice.WEEKLY:
            return subscription_date + timedelta(weeks=1)
        if period == PeriodChoice.MONTHLY:
            return subscription_date + timedelta(weeks=4)
        if period == PeriodChoice.QUARTERLY:
            return subscription_date + timedelta(weeks=13)
        if period == PeriodChoice.YEARLY:
            return subscription_date + timedelta(weeks=52)

    @property
    def is_expired(self):
        """Check if subscription is expired"""
        return self.expiry_date < timezone.now()

    @staticmethod
    def create_invoice(subscription=None):
        """Create invoice for subscription"""
        if not subscription:
            return None

        # if not subscription.is_expired:
        #     return None

        invoice = Invoice.objects.create(
            cooperative=subscription.cooperative,
            subscription=subscription,
            invoice_date=timezone.now(),
            invoice_amount=subscription.pricing.price,
            member=subscription.member,
        )

        subscription.subscription_status = SubscriptionStatus.EXPIRED
        subscription.subscription_date = subscription.expiry_date
        subscription.expiry_date = Subscription.get_expiry_date(
            subscription.pricing.period, subscription.expiry_date
        )
        subscription.save()

        send_sms(
            subscription.member.mobile,
            "We have created an invoice for you. Please pay!",
            subscription.cooperative.name,
        )
        return invoice


class Invoice(BaseModel):
    """Invoices model"""

    cooperative = models.ForeignKey(
        Cooperative, on_delete=models.CASCADE, null=False, related_name="invoices"
    )
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, null=False, related_name="invoices"
    )
    invoice_date = models.DateTimeField(null=False, blank=False)
    invoice_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )
    invoice_status = models.CharField(
        max_length=255,
        choices=InvoiceStatus.choices,
        null=False,
        default=InvoiceStatus.UNPAID,
    )
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, null=False, related_name="invoices"
    )
    payment_transferred = models.BooleanField(default=False)
    payment_transfer_id = models.CharField(max_length=255, null=True, blank=True)
    payment_method = models.CharField(max_length=255, null=True, blank=True)
