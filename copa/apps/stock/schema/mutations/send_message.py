import re
import graphene
import requests
from graphql import GraphQLError
from ...models import Productivity, ProductivityField
from copa.utils.app_utils.database import get_model_object


class SendMessage(graphene.Mutation):
    """
    Send Productivity Message Mutation

    Args:
        graphene ([type]): [description]
    """
    success = graphene.String()

    class Arguments:
        id = graphene.ID()

    def mutate(self, info, **kwargs):

        id = kwargs.get('id')

        # get productivity object instance
        productivity = Productivity.objects.filter(id=id).first()

        if re.match(r'(^[0-9]{10,11}$)',
                    productivity.member.mobile) is None:
            raise GraphQLError("Telefone yanditse nabi, \
                                Urugero: \'0732990999\'")

        message = "Muraho, {first_name} {last_name}.\n" \
                  "Umusaruro mbumbe mwagemuye ni {quantity} {unit} kuri {price_per_unity} Rwf.\n" \
            .format(
            first_name=productivity.member.first_name,
            last_name=productivity.member.last_name,
            quantity=productivity.quantity,
            unit=productivity.unity,
            price_per_unity=productivity.price_per_unity
        )

        productivity_meta = productivity.productivity_meta.all()
        meta_list = []
        for meta in productivity_meta:
            productivity_field = ProductivityField.objects.filter(
                key=meta.key,
                cooperative=productivity.cooperative
            ).first()

            meta_str = "{placeholder}: {value}".format(placeholder=productivity_field.placeholder, value=meta.value)
            meta_list.append(meta_str)

        message += ", ".join(meta_list)

        message += "\nKu bundi bufasha mwahamagara 0783371338" \
                   "\nMurakoze"

        print(message)

        data = {
            'recipients': productivity.member.mobile,
            'message': message,
            'sender': productivity.cooperative.name[:10]
        }

        r = requests.post(
            'https://www.intouchsms.co.rw/api/sendsms/.json',
            data,
            auth=('frank.muhiza', 'frank.muhiza'))

        productivity.message_status = True

        if r.status_code == 404:
            productivity.message_status = False
            success = 'Message failed to be sent, try again'

        productivity.save()

        response = r.json()

        if not response:
            success = 'Message failed to be sent, try again or ask for help'

        success = 'Message sent successfully {} {}'.format(
            productivity.member.first_name,
            (productivity.member.last_name or '')
        )

        return SendMessage(success=success)
