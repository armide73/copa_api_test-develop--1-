"""Kudibooks company types."""
import graphene

class KudiCurrencyType(graphene.ObjectType):
    """Kudi currency type."""
    id = graphene.Int()
    name = graphene.String()

class KudiIndustryType(graphene.ObjectType):
    """Kudi industry type."""
    id = graphene.Int()
    name = graphene.String()

class KudiPlanType(graphene.ObjectType):
    """Kudi plan type."""
    id = graphene.Int()
    name = graphene.String()
    description = graphene.String() 

class KudiCountryType(graphene.ObjectType):
    """Kudi books country type."""
    id = graphene.Int()
    name = graphene.String()


class RequiredCompanyDataType(graphene.ObjectType):
    """Kudi books required company data type."""
    countries = graphene.List(KudiCountryType)
    currencies = graphene.List(KudiCurrencyType)
    industries = graphene.List(KudiCurrencyType)
    plans = graphene.List(KudiPlanType)
