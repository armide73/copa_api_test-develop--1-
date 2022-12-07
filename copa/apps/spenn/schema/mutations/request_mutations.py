import graphene
import requests
from django.db import transaction

from copa.apps.pricing.models import Invoice, InvoiceStatus
from copa.apps.spenn.models import SpennRequestStatus
from copa.services.spenn.requests import SpennRequest


class PaymentMethod(graphene.Enum):
    """Payment channel enum"""

    MOBILE_MONEY = "MOBILE_MONEY"
    SPENN = "SPENN"


class RequestInvoicePayment(graphene.Mutation):
    message = graphene.String()
    success = graphene.Boolean()

    class Arguments:
        payment_method = graphene.Argument(PaymentMethod, required=True)
        invoice_id = graphene.String(required=True)

    def mutate(self, info, payment_method=None, invoice_id=None):
        try:
            with transaction.atomic():
                invoice = Invoice.objects.get(id=invoice_id)

                if invoice.invoice_status == "PAID":
                    return RequestInvoicePayment(
                        success=False, message="Invoice has already been paid"
                    )

                if (
                    payment_method == "SPENN"
                    and invoice.invoice_status == InvoiceStatus.UNPAID
                ):
                    request = SpennRequest(
                        amount=invoice.invoice_amount,
                        phone=invoice.member.mobile,
                        message=f"Payment for {invoice.cooperative.name} invoice",
                        reference=invoice.id,
                    ).create()

                    request_id = request.get("requestId")

                    SpennRequestStatus.objects.create(
                        amount=invoice.invoice_amount,
                        phone=invoice.member.mobile,
                        reference=invoice.id,
                        request_id=request_id,
                    )
                    invoice.invoice_status = InvoiceStatus.PENDING_PAYMENT
                    invoice.save()
                    return RequestInvoicePayment(
                        success=True, message="Invoice payment request successful"
                    )
        except Invoice.DoesNotExist as e:
            print(e)
            return RequestInvoicePayment(
                success=False, message="Invoice does not exist"
            )
        except requests.exceptions.HTTPError as e:
            print(e)
            print(e.response.text)
            return RequestInvoicePayment(
                success=False, message="Error requesting payment"
            )
        except Exception as e:
            print(e)
            return RequestInvoicePayment(
                success=False, message="Error requesting payment"
            )


class CancelSpennRequest(graphene.Mutation):
    message = graphene.String()
    success = graphene.Boolean()

    class Arguments:
        invoice_id = graphene.String(required=True)

    def mutate(self, info, invoice_id=None):
        try:
            with transaction.atomic():
                invoice = Invoice.objects.get(id=invoice_id)

                if invoice.status == InvoiceStatus.PAID:
                    return CancelSpennRequest(
                        success=False, message="Invoice has already been paid"
                    )

                if invoice.invoice_status == InvoiceStatus.PENDING_PAYMENT:
                    request = SpennRequestStatus.objects.get(
                        reference=invoice.id, status="PENDING"
                    )

                    SpennRequest().cancel(request.request_id)
                    invoice.status = InvoiceStatus.UNPAID
                    invoice.save()
        except Invoice.DoesNotExist as e:
            print(e)
            return CancelSpennRequest(success=False, message="Invoice does not exist")
        except requests.exceptions.HTTPError as e:
            print(e)
            print(e.response.text)
            return CancelSpennRequest(success=False, message="Error cancelling payment")
        except Exception as e:
            print(e)
            return CancelSpennRequest(success=False, message="Error cancelling payment")
