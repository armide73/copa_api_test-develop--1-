from graphene_django_extras import DjangoInputObjectType, DjangoObjectType, \
    DjangoListObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination
from ...models import Cooperative, Member, MemberMeta, MemberField,CooperativeEmployee


class CooperativeType(DjangoObjectType):
    class Meta:
        model = Cooperative
        description = " Type definition for a single cooperative "
        filter_fields = {
            'id': ('exact', ),
            'name': ('exact', 'icontains', 'istartswith'),
            'district': ('exact', 'icontains', 'istartswith'),
            'province': ('exact', 'icontains', 'istartswith'),
            'sector': ('exact', 'icontains', 'istartswith'),
        }

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset


class CooperativeInputType(DjangoInputObjectType):
    class Meta:
        model = Cooperative
        description = " Type definition for a single cooperative "
        exclude_fields = [
            'created_at',
            'updated_at',
            'deleted_at',
            'deleted_by']


class CooperativeListType(DjangoListObjectType):
    class Meta:
        model = Cooperative
        description = " Type definition for a list of cooperative "


# Member types
class MemberType(DjangoObjectType):
    class Meta:
        model = Member
        description = " Type definition for a single member "
        filter_fields = {
            'id': ('exact', ),
            'gender': ('exact', 'icontains', 'istartswith'),
            'cooperative__id': ('exact', ),
            'created_at': ('exact', 'gte', 'lte'),
            'keywords': ('exact', 'icontains', 'istartswith'),
        }

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset


class MemberInputType(DjangoInputObjectType):
    class Meta:
        model = Member
        description = " Type definition for a single member "
        exclude_fields = [
            'created_at',
            'updated_at',
            'deleted_at',
            'deleted_by']


class MemberListType(DjangoListObjectType):
    class Meta:
        model = Member
        description = " Type definition for a list of member "
        pagination = LimitOffsetGraphqlPagination(
            default_limit=100, ordering="-created_at")


class MemberMetaType(DjangoObjectType):
    class Meta:
        model = MemberMeta
        description = " Type definition for a single member "
        filter_fields = {
            'id': ('exact', ),
            'key': ('exact', 'icontains', 'istartswith'),
            'member__id': ('exact',)
        }

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset


class MemberMetaInputType(DjangoInputObjectType):
    class Meta:
        model = MemberMeta
        description = " Input type definition for member meta data "
        exclude_fields = ['member']


class MemberMetaListType(DjangoListObjectType):
    class Meta:
        model = MemberMeta
        description = " Type for a list of members "


class MemberFieldType(DjangoObjectType):
    class Meta:
        model = MemberField
        description = " Type of a single member field "
        filter_fields = {
            'id': ('exact', ),
            'key': ('exact', 'icontains', 'istartswith'),
            'cooperative__id': ('exact', ),
        }

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset


class MemberFieldInputType(DjangoInputObjectType):
    class Meta:
        model = MemberField
        description = " Type of a single member field "


class MemberFieldListType(DjangoListObjectType):
    class Meta:
        model = MemberField
        description = " Type of a list of member fields "

class EmployeeType(DjangoObjectType):
    class Meta:
        model=CooperativeEmployee
        description="Type of employees"
        fields=('names','employee_id','address','phone_number')      
