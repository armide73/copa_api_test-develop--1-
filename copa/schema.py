import graphene
import graphql_jwt
from graphene_django.debug import DjangoDebug
from graphene_django_extras import all_directives

# Schema queries and mutations imports
from copa.apps.authentication.schema.queries.user import \
    Query as UserQueries
from copa.apps.authentication.schema.mutations.mutations import \
    Mutation as UserMutations
from copa.apps.cooperative.schema.queries.cooperative import \
    Query as CooperativeQueries
from copa.apps.cooperative.schema.mutations.mutations import \
    Mutation as CooperativeMutations
from copa.apps.stock.schema.queries.stock_queries import \
    Query as StockQueries
from copa.apps.stock.schema.mutations.stock_mutations import \
    Mutation as StockMutations
from copa.apps.kudibooks.schema.mutations.mutations import \
    Mutation as KudibooksMutations

from copa.apps.kudibooks.schema.querries.companies_query import \
    Query as KudiCompanyQuerries

from copa.apps.kudibooks.schema.querries.vendor_querries import \
    Query as KudiVendorQuerries

from copa.apps.pricing.schema.querries.pricing_querries import \
    Query as PricingQuerries

from copa.apps.pricing.schema.mutations.mutations import \
    Mutation as PricingMutations
from copa.apps.spenn.schema.mutations.mutations import \
    Mutation as SpennMutations  


class Query(
    graphene.ObjectType,
    UserQueries,
    CooperativeQueries,
    StockQueries,
    KudiCompanyQuerries,
    KudiVendorQuerries,
    PricingQuerries
):
    debug = graphene.Field(DjangoDebug, name='_debug')
    pass


class Mutation(
    UserMutations,
    CooperativeMutations,
    StockMutations,
    KudibooksMutations,
    PricingMutations,
    SpennMutations,
):
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(
    mutation=Mutation, query=Query, directives=all_directives)
