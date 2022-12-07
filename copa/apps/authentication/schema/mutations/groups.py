import graphene
from graphql import GraphQLError
from django.contrib.auth.models import Permission, Group

from ..types.user import GroupInput, GroupType
from .....utils.app_utils.database import SaveContextManage, \
    get_model_object


class AddGroup(graphene.Mutation):
    """
    Add Group Mutation

    Args:
        new_group (obj): new group object data
    """
    success = graphene.String()
    group = graphene.Field(GroupType)

    class Arguments:
        new_group = graphene.Argument(GroupInput)

    def mutate(self, info, **kwargs):
        success = "Group yanditswe neza"
        group = kwargs.get('new_group')

        filter_group_name = Group.objects.filter(name=group['name'].lower())

        if filter_group_name:
            raise GraphQLError("Group ifite izina: `{}` irahari".format(
                               group['name']))

        group_instance = Group(
            name=group['name'].lower()
        )

        with SaveContextManage(group_instance, model=Group) as group_instance:
            if group.permissions:
                for permission in group['permissions']:
                    permission_instance = Permission.objects.get(id=permission)
                    if permission_instance:
                        group_instance.permissions.add(permission_instance)

            return AddGroup(success=success, group=group_instance)


class UpdateGroup(graphene.Mutation):
    """
    Update Group Mutation

    Args:
        group_id (int): group primary key
        group_data (dict): group data to update
    """
    success = graphene.String()
    group = graphene.Field(GroupType)

    class Arguments:
        group_id = graphene.ID(required=True)
        group_data = graphene.Argument(GroupInput)

    def mutate(self, info, **kwargs):
        success = "Group yahinduwe neza"

        group_instance = Group.objects.get(id=kwargs.get('group_id'))

        if not group_instance:
            raise GraphQLError("Group ifite ID {} does \
                not exists".format(kwargs.get('group_id')))

        for group in kwargs.get('group_data'):
            if group == 'name':
                group_instance.name = kwargs.get('group_data')[group]
                group_instance.save()
            elif group == 'permissions':
                group_instance.permissions.clear()
                for permission in kwargs.get('group_data')[group]:
                    permission_instance = Permission.objects.get(id=permission)
                    if permission_instance:
                        group_instance.permissions.add(permission_instance)

        return UpdateGroup(success=success, group=group_instance)


class DeleteGroup(graphene.Mutation):
    """
    Delete Group Mutation

    Args:
        group_id (int): group primary key value
    """
    success = graphene.String()

    class Arguments:
        group_id = graphene.ID(required=True)

    def mutate(self, info, **kwargs):
        success = "Group yasibwe neza"

        group = get_model_object(Group, 'id', kwargs.get('group_id'))

        if not group:
            raise GraphQLError("Group ifite ID {} \
                ntabwo yabonetse".format(kwargs.get('group_id')))

        group.permissions.clear()
        group.delete()

        return DeleteGroup(success=success)
