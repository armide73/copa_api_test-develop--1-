import graphene
from copa.apps.pricing.models import Invoice, Pricing, Subscription
from copa.apps.pricing.schema.types.pricing_types import InvoiceType, PricingType, SubscriptionType


class Query(graphene.AbstractType):
    # Query to get all the pricing details
    pricing = graphene.List(PricingType, cooperative_id=graphene.String(required=True))
    subscriptions = graphene.List(SubscriptionType, member_id=graphene.String(required=True))
    invoices = graphene.List(InvoiceType, member_id=graphene.String(required=True))

    def resolve_pricing(self, info, cooperative_id=None):
        return Pricing.objects.filter(cooperative_id=cooperative_id)

    def resolve_subscriptions(self, info, member_id=None):
        return Subscription.objects.filter(member_id=member_id)
    
    def resolve_invoices(self, info, member_id=None):
        return Invoice.objects.filter(member_id=member_id)