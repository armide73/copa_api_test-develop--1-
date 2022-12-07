from graphene_django import DjangoObjectType
from copa.apps.pricing.models import Invoice, Pricing, Benefit, Subscription

class BenefitType(DjangoObjectType):
    class Meta:
        model = Benefit

class PricingType(DjangoObjectType):
    class Meta:
        model = Pricing

class SubscriptionType(DjangoObjectType):
    class Meta:
        model = Subscription
        
class InvoiceType(DjangoObjectType):
    class Meta:
        model = Invoice
