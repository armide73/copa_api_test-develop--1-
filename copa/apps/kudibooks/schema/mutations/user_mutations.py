"""Kudibooks user mutations."""
from datetime import datetime
from email import message
import graphene
from graphql_jwt.decorators import login_required
from requests import HTTPError
from copa.apps.authentication.schema.types.user import UserType
from copa.apps.cooperative.models import EnabledServices
from copa.services.kudibooks.company import KudiCompany
from copa.services.kudibooks.users import KudiUser

class ErrorType(graphene.ObjectType):
    """Error type."""
    message = graphene.String()
    field = graphene.String()

class SetupKudibooksAccount(graphene.Mutation):
    """Set up kudibooks account
    """
    message = graphene.String()
    success = graphene.Boolean()
    user = graphene.Field(UserType)
    errors = graphene.List(ErrorType)

    class Arguments:
        """Arguments for the mutation"""
        industry = graphene.Int(required=True)
        country = graphene.Int(required=True)
        currency = graphene.Int(required=True)
        plan = graphene.Int(required=True)

    @login_required
    def mutate(self, info, **kwargs):
        """Mutate the data"""
        user = info.context.user
        industry = kwargs.get("industry")
        country = kwargs.get("country")
        currency = kwargs.get("currency")
        plan = kwargs.get("plan")

        errors = []

        if not industry:
            errors.append(ErrorType(message="Industry is required", field="industry"))

        if not country:
            errors.append(ErrorType(message="Country is required", field="country"))

        if not currency:
            errors.append(ErrorType(message="Currency is required", field="currency"))

        if not plan:
            errors.append(ErrorType(message="Plan is required", field="plan"))

        if len(errors) > 0:
            return SetupKudibooksAccount(success=False, errors=errors)

        kudibooks_user = None
        if not user.kudibooks_user_code:
            try:
                kudibooks_user = KudiUser(
                    first_name=user.names,
                    last_name=user.names,
                    email=user.email,
                ).create()
            except (HTTPError, Exception):
                return SetupKudibooksAccount(
                    success=False,
                    message="Something went wrong, try again later"
                )

            user.kudibooks_user_code = kudibooks_user.get("remote_uuid")
            user.save()

        cooperative = user.cooperatives
        if cooperative.kudibooks_company_id:
            return SetupKudibooksAccount(success="Company already created", user=user)

        kudibooks_company = None

        try:
            kudibooks_company = KudiCompany(
                user_code=user.kudibooks_user_code,
                company_name=cooperative.name,
                industry=industry,
                country=country,
                currency=currency,
                plan=plan
            ).create()
        except (HTTPError, Exception):
            return SetupKudibooksAccount(
                success=False, 
                message="Something went wrong, try again later"
            )

        kudibooks_company_data = kudibooks_company.get("original")
        cooperative.kudibooks_company_id = kudibooks_company_data.get("remote_uuid")
        cooperative.save()

        EnabledServices.objects.create(
            cooperative=cooperative,
            service="KUDIBOOKS",
            is_enabled=True,
            subscription_date=datetime.now()
        )

        return SetupKudibooksAccount(success="User created", user=user)
