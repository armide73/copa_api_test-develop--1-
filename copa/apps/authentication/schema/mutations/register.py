import graphene
from django.contrib.auth import get_user_model
from ...models import User
from ..types.user import UserInputType, UserType
from .....utils.auth_utils.validations import validate
from .....utils.app_utils.database import SaveContextManage
from .....utils.responses.common import SUCCESS_RESPONSES
from django.utils.translation import gettext as _
from .....utils.auth_utils.token import generate_tokens


class Register(graphene.Mutation):
    """
    Register mutation

    Args:
        new_user (obj): obj of user's data
    """
    success = graphene.String()
    user = graphene.Field(UserType)
    token = graphene.String()
    rest_token = graphene.String()

    class Arguments:
        new_user = graphene.Argument(UserInputType)

    def mutate(self, info, **kwargs):
        new_user = kwargs.get('new_user')
        valid_user = validate.validate_register(new_user)

        # register user functionality
        user = get_user_model().objects.create_user(**valid_user)

        with SaveContextManage(user, model=User) as user:
            success = _(
                SUCCESS_RESPONSES['register_success'].format(user.email))

            token, rest_token = None, None

            token, rest_token = generate_tokens(user)

            return Register(success=success,
                            user=user,
                            token=token,
                            rest_token=rest_token)
