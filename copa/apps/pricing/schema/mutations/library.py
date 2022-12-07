from copa.apps.pricing.models import Subscription


def create_invoices(member=None):
    
    if member:
        subscriptions = Subscription.objecs.filter(member=member)
        
        for subscription in subscriptions:
            