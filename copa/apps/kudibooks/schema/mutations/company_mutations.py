"""Kudibooks Company mutations"""
import graphene
from graphql_jwt.decorators import login_required

from copa.apps.cooperative.models import Cooperative
from copa.apps.cooperative.schema.types.cooperative import CooperativeType
from copa.services.kudibooks.company import KudiCompany

class SetupKudibooksCompany(graphene.Mutation):
    """Set up kudibooks company
    """
    success = graphene.String()
    cooperative = graphene.Field(CooperativeType)

    class Arguments:
        """Arguments for the mutation"""
        cooperative_id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, kwargs):
        """Mutation to set up kudibooks company"""
        user = info.context.user
        cooperative_id = kwargs.get("cooperative_id")

        cooperative = Cooperative.objects.filter(pk=cooperative_id)

        company_data = KudiCompany(
            company_name=cooperative.name,
            industry=23,
            country=12,
            currency=186,
            plan=2
        ).create()

        cooperative.kudibooks_company_id = company_data.get("companyID")
        cooperative.save()
        return SetupKudibooksCompany(success="Company created", cooperative=cooperative)
