import graphene
from graphene_django_extras import DjangoListObjectField
from ..types.user import UserListType, GroupListType, \
    PermissionListType


class Query(graphene.AbstractType):
    users = DjangoListObjectField(
        UserListType, description='All Users query')
    groups = DjangoListObjectField(
        GroupListType, description='All Groups query')
    permissions = DjangoListObjectField(
        PermissionListType, description='All Permissions query')
