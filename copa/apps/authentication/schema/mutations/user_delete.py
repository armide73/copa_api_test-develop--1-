import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from ...models import User
from .....utils.app_utils.database import get_model_object


class DeleteUser(graphene.Mutation):
    success = graphene.String()

    class Arguments:
        user_id = graphene.ID()

    @login_required
    def mutate(cls, info, **kwargs):
        success = "Umukoresha yasibwe neza"

        user = get_model_object(User, 'id', kwargs.get('user_id'))

        if info.context.user == user:
            raise GraphQLError("Ntabwo wemerewe kwisiba")

        if not user:
            raise GraphQLError("Group ifite ID {} \
                ntabwo yabonetse".format(kwargs.get('user_id')))

        user.delete()
        return DeleteUser(success=success)
