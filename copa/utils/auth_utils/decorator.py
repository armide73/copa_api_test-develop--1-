from functools import wraps
from graphql import GraphQLError
from graphql.execution.base import ResolveInfo
from daca.apps.profiles.models import Role
from django.utils.translation import gettext as _
from daca.utils.messages.auth_messages import AUTH_ERROR_RESPONSES


def user_permission(*param):
    """
    Check user's permission based on their role
    """

    # allowed default : super_admin
    allowed_roles = ['super_admin']
    for arg in param:
        allowed_roles.append(arg)

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            info = [arg for arg in args if isinstance(arg, ResolveInfo)]

            user = info[0].context.user
            # get roles
            roles = Role.objects.filter(name__in=allowed_roles)

            # check if one of user's role is in the roles
            if user.verified_profiles.filter(role__in=roles,):
                return f(*args, **kwargs)
            raise GraphQLError(
                _(AUTH_ERROR_RESPONSES["permission_denied"])
            )

        return wrapper
    return decorator


def super_user_permission():
    """
    Check if a user is an admin.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            info = [arg for arg in args if isinstance(arg, ResolveInfo)]

            user = info[0].context.user
            if user.is_admin:
                return f(*args, **kwargs)
            raise GraphQLError(
                _(AUTH_ERROR_RESPONSES["permission_denied"])
            )

        return wrapper
    return decorator


def check_authorization(app, action, model):
    """
    Check user's permission based on their role

    Args:
        app: django app name
        action: model action such as (add, change, delete, view)
        model: database model in lowecase
    """

    allowed_app = app  # django app name
    allowed_action = action  # action (add, change, delete, view)
    allowed_model = model  # the model name in lowercase letters

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            info = [arg for arg in args if isinstance(arg, ResolveInfo)]

            user = info[0].context.user

            if user.has_perm('{}.{}_{}'.format(
                    allowed_app,
                    allowed_action,
                    allowed_model)):
                return f(*args, **kwargs)
            raise GraphQLError(
                _(AUTH_ERROR_RESPONSES["permission_denied"])
            )

        return wrapper
    return decorator
