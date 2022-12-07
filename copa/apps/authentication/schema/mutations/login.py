import graphene
from ...models import User
from graphql import GraphQLError
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from .....utils.responses.common import ERROR_RESPONSES, \
    SUCCESS_RESPONSES
from .....utils.auth_utils.token import generate_tokens
from ..types.user import UserType


class Login(graphene.Mutation):
    """
    Login a user mutation

    Args:
        email (str): User's email
        password (str): User's password
    """
    success = graphene.String()
    user = graphene.Field(UserType)
    token = graphene.String()
    rest_token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        message = ERROR_RESPONSES['invalid_credentials']

        user = User.objects.filter(email=email).first()
        if not user:
            raise GraphQLError(_(message))

        token, rest_token, success = None, None, None

        if user.is_active:
            user_auth = authenticate(email=email, password=password)

            if not user_auth:
                raise GraphQLError(_(message))

            token, rest_token = generate_tokens(user_auth)

            success = SUCCESS_RESPONSES['login_success']

        return Login(success=success, user=user,
                     token=token, rest_token=rest_token)
