from django.db import models
from ...models import BaseModel
from copa.apps.cooperative.models import Cooperative, Member
# from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Productivity(BaseModel):
    cooperative = models.ForeignKey(
        Cooperative, on_delete=models.CASCADE,
        null=False, blank=False, related_name="productivity")
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE,
        null=False, blank=False, related_name="member_productivity")
    quantity = models.FloatField()
    unity = models.CharField(
        max_length=50, default='kg', null=True, blank=True)
    message_status = models.BooleanField(default=False)
    price_per_unity = models.FloatField(
        null=True, default=0, blank=False)

    class Meta:
        verbose_name_plural = "Productivity"
        ordering = ['-created_at']

    def __str__(self):
        return '{}'.format(self.id)

    @property
    def total(self):
        return self.quantity * self.price_per_unity

    @property
    def retain(self):
        retain = 0
        productivity_meta = ProductivityMeta.objects.filter(
            productivity=self.id)

        for meta in productivity_meta:
            field = ProductivityField.objects.filter(
                key=meta.key, cooperative=self.cooperative.id).first()

            if field.field_choice == 'percentage':
                retain += float(meta.value)
        return retain

    @property
    def asigara(self):
        asigara = 0

        productivity_meta = ProductivityMeta.objects.filter(
            productivity=self.id)

        for meta in productivity_meta:
            field = ProductivityField.objects.filter(
                key=meta.key, cooperative=self.cooperative.id).first()
            if field.field_choice == 'percentage':
                asigara += (float(meta.value) * self.price_per_unity)
            elif field.field_choice == 'francsremove':
                asigara += float(meta.value)
            elif field.field_choice == 'francsadd':
                asigara -= float(meta.value)

        if asigara >= 100:
            asigara += 100

        return asigara

    @property
    def byose(self):
        return self.total - self.asigara


class ProductivityField(BaseModel):
    cooperative = models.ForeignKey(
        Cooperative,
        on_delete=models.CASCADE,
        null=True, blank=True)
    key = models.CharField(max_length=255, null=False, blank=False)
    placeholder = models.CharField(max_length=255, null=True, blank=True)
    field_choice = models.CharField(
        max_length=255,
        choices=[
            ('percentage', 'percentage'),
            ('francs', 'francs'),
            ('francsadd', 'francsadd'),
            ('francsremove', 'francsremove'),
            ('none', 'none'),
            ('', ''),
        ],
        default='none', null=True, blank=True)
    default_value = models.FloatField(default=0)
    field_type = models.CharField(
        max_length=255,
        choices=[
            ('number', 'number'),
        ],
        null=True, blank=True)
    is_required = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        verbose_name_plural = "ProductivityFields"

    def __str__(self):
        return '{} {}'.format(self.cooperative, self.key)

    def delete(self):
        super().hard_delete()


class ProductivityMeta(BaseModel):
    productivity = models.ForeignKey(
        Productivity,
        on_delete=models.CASCADE,
        null=False, related_name="productivity_meta"
    )
    key = models.CharField(max_length=200, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "ProductivityMeta"
        unique_together = ['productivity', 'key']

    def __str__(self):
        return self.key
