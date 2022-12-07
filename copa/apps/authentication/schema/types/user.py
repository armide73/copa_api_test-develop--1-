import graphene
from graphene_django_extras import DjangoInputObjectType, DjangoObjectType, \
    DjangoListObjectType
from ...models import User
from django.contrib.auth.models import Permission, Group


class UserType(DjangoObjectType):
    class Meta:
        model = User
        description = " Type definition for a single user "
        filter_fields = {
            'id': ('exact', ),
            'names': ('exact', 'icontains', 'istartswith'),
            'email': ('exact', 'icontains', 'istartswith'),
            'country': ('exact', 'icontains', 'istartswith'),
            'status': ('exact', 'icontains', 'istartswith'),
            'phone_number': ('exact', 'icontains', 'istartswith'),
        }
        exclude_fields = ['password']

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset


class UserListType(DjangoListObjectType):
    class Meta:
        model = User
        description = " Type definition for a list of users "


class UserInputType(DjangoInputObjectType):
    class Meta:
        model = User
        description = " Type definition for a list of users "


class GroupType(DjangoObjectType):
    all_users = graphene.List(UserType)

    class Meta:
        model = Group
        description = " Type definition for a single group "
        filter_fields = {
            "id": ("exact", ),
        }

    def resolve_all_users(self, info, **kwargs):
        return User.objects.filter(groups__id=self.id).all()

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset


class GroupInput(DjangoInputObjectType):
    class Meta:
        description = " Group InputType definition "
        model = Group


class GroupListType(DjangoListObjectType):
    users = graphene.List(UserType)

    class Meta:
        description = " Type definition for group list "
        model = Group
        filter_fields = {
            'id': ('exact', ),
        }

    def resolve_users(self, info, **kwargs):
        return User.objects.filter(groups__id=self.id).all()


class PermissionType(DjangoObjectType):
    class Meta:
        model = Permission
        description = " Type definition for a single permission "
        filter_fields = {
            "id": ("exact", ),
        }

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset


class PermissionListType(DjangoListObjectType):
    class Meta:
        description = " Type definition for group list "
        model = Permission
        filter_fields = {
            'id': ('exact', ),
        }
