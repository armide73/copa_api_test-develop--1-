"""Kudibooks mutations."""
import graphene

from copa.apps.kudibooks.schema.mutations.company_mutations import SetupKudibooksCompany
from copa.apps.kudibooks.schema.mutations.user_mutations import SetupKudibooksAccount
from copa.apps.kudibooks.schema.mutations.vendor_mutations import SyncVendors


class Mutation(graphene.ObjectType):
    """Mutations for kudibooks"""
    setup_kudibooks_company = SetupKudibooksCompany.Field()
    set_up_kudibooks_account = SetupKudibooksAccount.Field()
    sync_vendors = SyncVendors.Field()
    