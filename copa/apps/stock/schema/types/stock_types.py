import graphene
from graphene_django_extras import DjangoInputObjectType, DjangoObjectType, \
    DjangoListObjectType
from ...models import Productivity, ProductivityField, ProductivityMeta


class ProductivityType(DjangoObjectType):
    total = graphene.Float()
    retain = graphene.Float()
    asigara = graphene.Float()
    byose = graphene.Float()

    class Meta:
        model = Productivity
        description = " Productivity single object type "
        filter_fields = {
            'id': ('exact', ),
            'cooperative__id': ('exact', ),
            'created_at': ('exact', 'gte', 'lte')
        }

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset

    def resolve_total(self, info):
        return self.total

    def resolve_retain(self, info):
        return self.retain

    def resolve_asigara(self, info):
        return self.asigara

    def resolve_byose(self, info):
        return self.byose


class ProductivityInputType(DjangoInputObjectType):
    class Meta:
        model = Productivity
        description = " Productivity single object type input "


class ProductivityListType(DjangoListObjectType):
    class Meta:
        model = Productivity
        description = " Productivity list object type "


class ProductivityMetaType(DjangoObjectType):
    class Meta:
        model = ProductivityMeta
        description = " Productivity meta single type "
        filter_fields = {
            'id': ('exact', )
        }

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset


class ProductivityMetaInputType(DjangoInputObjectType):
    class Meta:
        model = ProductivityMeta
        description = " Productivity Meta input type "
        exclude_fields = ['productivity']


class ProductivityMetaListType(DjangoListObjectType):
    class Meta:
        model = ProductivityMeta
        description = " Productivity meta list type "


class ProductivityFieldType(DjangoObjectType):
    class Meta:
        model = ProductivityField
        description = " Productivity field single type "
        filter_fields = {
            'id': ('exact', ),
            'cooperative__id': ('exact', ),
        }

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset


class ProductivityFieldInputType(DjangoInputObjectType):
    class Meta:
        model = ProductivityField
        description = " Productivity field input type "


class ProductivityFieldListType(DjangoListObjectType):
    class Meta:
        model = ProductivityField
        description = " Productivity field list type "
