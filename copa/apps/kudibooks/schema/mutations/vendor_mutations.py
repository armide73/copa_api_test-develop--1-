"""Kudibooks Vendors mutation"""
from unicodedata import name
import graphene
from graphql_jwt.decorators import login_required

from copa.services.kudibooks.vendor import KudiVendor


class SyncVendors(graphene.Mutation):
    """Class to Synchronize cooperative vendors with kudibooks"""
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    message = graphene.String()

    @login_required
    def mutate(self, info, **kwargs):
        """Sync cooperative vendors"""
        user = info.context.user
        cooperative = user.cooperatives
        kudi_company_id = cooperative.kudibooks_company_id

        for member in cooperative.members.all():
            if member.kudi_books_id:
                continue

            vendor = KudiVendor(
                user_code=user.kudibooks_user_code,
                company_id=kudi_company_id,
                name=member.first_name + " " + member.last_name,
                phone=member.mobile
            ).create()

            member.kudi_books_id = vendor.get("vendorID")
            member.save()

            return SyncVendors(success="Vendors synced successfully")
        