from django.contrib.auth.models import update_last_login
from graphql_jwt.utils import jwt_encode, jwt_payload
from rest_framework.authtoken.models import Token


def generate_tokens(user):
    """
    generate tokens
    Args:
        user(Object): user's object from the database
    Returns:
        token, rest_token(tuple)
    """
    update_last_login(sender=None, user=user)

    # token to access GraphQL-based views
    user.password = None
    payload = jwt_payload(user)
    token = jwt_encode(payload)

    # token to access REST-based views
    rest_payload = Token.objects.get_or_create(user=user)
    rest_token = rest_payload[0]

    return (token, rest_token)
