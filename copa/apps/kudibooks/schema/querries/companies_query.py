import graphene

from copa.apps.kudibooks.schema.types.company_types import RequiredCompanyDataType
from copa.services.kudibooks.company import KudiCompany




class Query(graphene.AbstractType):
    """Kudibooks company querries."""
    required_company_data = graphene.Field(
        RequiredCompanyDataType,
        description="Required company data"
    )

    def resolve_required_company_data(self, info, **kwargs):
        """Resolve required company data."""
        required_data = KudiCompany().get_required()
        return required_data
