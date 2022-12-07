import graphene
from .register import Register
from .login import Login
from .groups import AddGroup, UpdateGroup, \
    DeleteGroup
from .user_groups import UserGroup, RemoveUserGroup
from .user_delete import DeleteUser


class Mutation(graphene.ObjectType):
    register = Register.Field()
    login = Login.Field()
    add_group = AddGroup.Field()
    update_group = UpdateGroup.Field()
    delete_group = DeleteGroup.Field()
    user_group = UserGroup.Field()
    remove_user_group = RemoveUserGroup.Field()
    delete_user = DeleteUser.Field()
