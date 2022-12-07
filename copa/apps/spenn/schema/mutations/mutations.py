import graphene

from copa.apps.spenn.schema.mutations.request_mutations import CancelSpennRequest, RequestInvoicePayment


class Mutation(graphene.ObjectType):
    request_invoice_payment = RequestInvoicePayment.Field()
    cancel_spenn_request = CancelSpennRequest.Field()
    