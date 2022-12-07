import graphene
from graphql import GraphQLError
from copa.apps.pricing.models import Benefit, Pricing, Subscription
from copa.apps.pricing.schema.types.pricing_types import InvoiceType, PricingType
from graphql_jwt.decorators import login_required


class AddPricing(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        price = graphene.Float(required=True)
        period = graphene.String(required=True)
        benefits = graphene.List(graphene.String)

    pricing = graphene.Field(PricingType)
    success = graphene.Boolean()

    @login_required
    def mutate(self, info, title, price, period, benefits=None):
        user = info.context.user
        cooperative = user.cooperatives
        pricing = Pricing.objects.create(
            title=title, price=price, period=period, cooperative=cooperative)

        if benefits:
            for benefit in benefits:
                benefit = Benefit.objects.create(
                    pricing=pricing,
                    cooperative=cooperative,
                    title=benefit
                )

        return AddPricing(pricing=pricing, success=True)


class UpdatePricing(graphene.Mutation):
    class Arguments:
        pricing_id = graphene.Int(required=True)
        title = graphene.String()
        price = graphene.Float()
        period = graphene.String()
        description = graphene.String()

    pricing = graphene.Field(PricingType)

    def mutate(self, info, pricing_id, title=None, price=None, description=None):
        pricing = Pricing.objects.filter(id=pricing_id).first()

        if not pricing:
            return GraphQLError('Pricing does not exist')

        pricing.title = title
        pricing.price = price
        pricing.description = description
        pricing.save()

        return UpdatePricing(pricing=pricing)


class DeactivatePricing(graphene.Mutation):
    class Arguments:
        pricing_id = graphene.Int(required=True)

    pricing = graphene.Field(PricingType)

    def mutate(self, info, pricing_id=None):
        pricing = Pricing.objects.filter(id=pricing_id).first()

        if pricing:
            pricing.is_active = False
            pricing.save()
        else:
            return GraphQLError('Pricing does not exist')

        return DeactivatePricing(pricing=pricing)


class CreateInvoices(graphene.Mutation):
    """Create invoice mutation"""
    class Arguments:
        """Arguments for the mutation"""
        subscription_id = graphene.String(required=True)

    success = graphene.Boolean()
    invoice = graphene.Field(InvoiceType)

    def mutate(self, info, subscription_id):
        """Mutation to create invoice"""
        subscription = Subscription.objects.filter(id=subscription_id).first()

        if not subscription:
            return GraphQLError('Subscription does not exist')

        invoice = Subscription.create_invoice(subscription)

        return CreateInvoices(success=True, invoice=invoice)
