"""Kudibooks Vendor Types"""
import graphene


class KudiBooksVendorType(graphene.ObjectType):
    """Kudibooks vendor type."""
    id = graphene.Int()
    name = graphene.String()
