import graphene
from graphql_jwt.decorators import login_required
from ..types.cooperative import CooperativeInputType, \
    CooperativeType
from ...models import Cooperative
from .....services.kudibooks.company import KudiCompany
from .....utils.app_utils.database import SaveContextManage
from .....utils.responses.common import SUCCESS_RESPONSES


class AddCooperative(graphene.Mutation):
    """
    Add Cooperative Mutation

    Args:
        new_coop (obj): new cooperative data
    """
    success = graphene.String()
    cooperative = graphene.Field(CooperativeType)

    class Arguments:
        new_coop = graphene.Argument(CooperativeInputType)

    @login_required
    def mutate(self, info, **kwargs):
        success = SUCCESS_RESPONSES['created'].format('Cooperative')
        new_coop = kwargs.get('new_coop')

        user = info.context.user

        cooperative = Cooperative(
            name=new_coop['name'],
            code=new_coop['code'],
            province=new_coop['province'],
            district=new_coop['district'],
            sector=new_coop['sector'],
            creator=user
        )

        with SaveContextManage(cooperative, model=Cooperative) as coop:
            kudibooks = cooperative.get_service("KUDIBOOKS")
            if kudibooks and kudibooks.is_enabled:
                KudiCompany(
                    company_name=coop.name,
                    industry="Cooperative",
                    country="Rwanda",
                    currency="RWF",
                    plan="Basic"
                ).create()

            return AddCooperative(success=success, cooperative=coop)
