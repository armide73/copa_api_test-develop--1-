import graphene

from copa.apps.pricing.schema.mutations.pricing_mutations import AddPricing, CreateInvoices


class Mutation(graphene.ObjectType):
   add_pricing = AddPricing.Field()
   create_invoice = CreateInvoices.Field()
