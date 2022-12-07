"""SPENN Django Models"""
from django.utils import timezone
from django.db import models

from copa.models import BaseModel


# Create your models here.
class SpennSession(BaseModel):
    """Spenn Session model"""

    access_token = models.TextField(unique=True)
    refresh_token = models.TextField(null=True, blank=True)
    expires_in = models.IntegerField()

    @property
    def is_token_expired(self):
        """Check if token has expired"""
        if (
            self.created_at + timezone.timedelta(seconds=self.expires_in)
            < timezone.now()
        ):
            return True
        return False


class SpennRequestStatus(BaseModel):
    """Spenn Request model"""

    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )
    phone = models.CharField(max_length=255, null=False, blank=False)
    reference = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(
        max_length=255, null=False, blank=False, default="PENDING"
    )
    request_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.phone} - {self.amount}"


        
