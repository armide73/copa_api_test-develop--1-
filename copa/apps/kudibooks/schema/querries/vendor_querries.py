"""Kudibooks Vendor Types"""
import graphene
from graphql_jwt.decorators import login_required
from copa.apps.kudibooks.schema.types.vendor_types import KudiBooksVendorType
from copa.services.kudibooks.vendor import KudiVendor


class Query(graphene.AbstractType):
    """Kudibooks vendor querries."""
    kudibooks_vendors = graphene.List(KudiBooksVendorType, description="Kudibooks vendors")

    @login_required
    def resolve_kudibooks_vendors(self, info, **kwargs):
        """KudiBooks vendors resolver."""
        user = info.context.user
        kudibooks_company_id = user.cooperatives.kudibooks_company_id

        response = KudiVendor(
            company_id=kudibooks_company_id,
            user_code=user.kudibooks_user_code
        ).get_all()

        return response["vendors"]
    