import re
from graphql import GraphQLError


class Validate:
    """
    Validate class
    """

    def strip_value(self, value):
        """
        Strip values of methods before validations
        Arguments:
            value: {String} any string
        """
        if value:
            self.value = value.strip()
            return self.value
        else:
            return None

    def validate_register(self, user):
        for key, value in user.items():
            if key == 'names':
                names = self.strip_value(value)
                if re.match(r'[a-zA-Z]', names) is None:
                    raise GraphQLError("Amazina yanditse nabi, \
                                        Urugero: \'Kamari Veda\'")
            elif key == 'phone_number':
                phone_number = self.strip_value(value)
                if re.match(r'(^[0-9]{10,11}$)',
                            phone_number) is None:
                    raise GraphQLError("Telefone yanditse nabi, \
                                        Urugero: \'0732990999\'")
            elif key == 'email':
                email = self.strip_value(value)
                if re.match(
                    r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]{2,5}$',
                        email) is None:
                    raise GraphQLError("Email yanditse nabi, \
                                        Urugero: \'kamari@mail.com\'")

        return user


validate = Validate()
