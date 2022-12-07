import graphene
from graphene_django_extras import DjangoListObjectField
from ..types.stock_types import ProductivityListType, \
    ProductivityMetaListType, ProductivityFieldListType


class Query(graphene.AbstractType):
    productivity = DjangoListObjectField(
        ProductivityListType, description='All Productivity data query')
    productivity_meta = DjangoListObjectField(
        ProductivityMetaListType, description='Productivity meta list query')
    productivity_fields = DjangoListObjectField(
        ProductivityFieldListType,
        description='Productivity fields list query')
