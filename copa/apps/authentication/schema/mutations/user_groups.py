import graphene
from graphql import GraphQLError
from ..types.user import UserType
from django.contrib.auth.models import Group
from ...models import User
from .....utils.app_utils.database import get_model_object


class UserGroup(graphene.Mutation):
    """
    Change User Group mutation

    Args:
        user_id (str): User's primary key
        group_id (str): User's chosen group
    """
    success = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        user_id = graphene.String(required=True)
        group_id = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        success = "User yashyizwe muri group neza "
        user_id = kwargs.get('user_id')
        group_id = kwargs.get('group_id')

        group = Group.objects.get(id=group_id)
        user = User.objects.get(id=user_id)

        if not group:
            raise GraphQLError("Group ifite ID: {} yabuze".format(group_id))

        if not user:
            raise GraphQLError("User ufite ID: {} yabuze".format(user_id))

        user.groups.clear()
        user.groups.add(group)

        return UserGroup(success=success, user=user)


class RemoveUserGroup(graphene.Mutation):
    """
    Remove user group mutation

    Args:
        user_id (str): user's primary key
    """
    success = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        user_id = graphene.String()

    def mutate(self, info, **kwargs):
        success = "User akuwe muri group neza"

        user = get_model_object(User, 'id', kwargs.get('user_id'))

        if not user:
            raise GraphQLError("User ufite ID: {} yabuze".format(
                kwargs.get('user_id')))

        user.groups.clear()

        return RemoveUserGroup(success=success, user=user)
