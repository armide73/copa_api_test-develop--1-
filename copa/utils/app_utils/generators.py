import uuid

from django.utils.http import int_to_base36
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

ID_LENGTH = 9


def id_generater() -> str:
    """Generates random string whose length is of `ID_LENGTH`"""
    return int_to_base36(uuid.uuid4().int)[:ID_LENGTH]


class Token(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.pk) + text_type(timestamp) +
                text_type(user.is_active))
