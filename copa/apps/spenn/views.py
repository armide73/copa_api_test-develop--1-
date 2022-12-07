from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.decorators import api_view

from copa.apps.pricing.models import Invoice, InvoiceStatus
from copa.apps.spenn.models import SpennRequestStatus
from copa.services.spenn.deposits import SpennDeposit


@api_view(["POST"])
def spenn_callback(request):
    """Handle POST request"""
    request_guid = request.data.get("requestGuid")
    external_refereference = request.data.get("ExternalReference")
    request_status = request.data.get("RequestStatus")

    if not request_guid or not external_refereference or not request_status:
        return HttpResponse(status=400, content="Bad Request")
    try:
        with transaction.atomic():
            status = "PENDING"
            if request_status == 2:
                status = "APPROVED"
            elif request_status == 3:
                status = "REJECTED"
            elif request_status == 4:
                status = "CANCELLED"

            spenn_request = SpennRequestStatus.objects.get(request_id=request_guid)
            spenn_request.status = status
            spenn_request.save()

            if status == "APPROVED":
                invoice = Invoice.objects.get(id=external_refereference)
                invoice.invoice_status = InvoiceStatus.PAID
                invoice.payment_method = "SPENN"
                invoice.save()
                
                try:
                    data = SpennDeposit(
                        amount=invoice.amount,
                        destination_phone=invoice.cooperative.creator.phone_number,
                        message=f"Payment from {invoice.member.mobile}",
                    ).create()
                    invoice.payment_transferred = True
                    invoice.payment_transfer_id = data.get("transactionId")
                    invoice.save()
                except Exception as e:
                    print(e)
            else:
                invoice = Invoice.objects.get(id=external_refereference)
                invoice.invoice_status = InvoiceStatus.UNPAID
                invoice.save()

            return HttpResponse(status=200, content="Payment Status Updated")
    except SpennRequestStatus.DoesNotExist:
        return HttpResponse("Request does not exist", status=400)
    except Invoice.DoesNotExist:  # type: ignore
        return HttpResponse("Invoice does not exist", status=400)
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=400)
