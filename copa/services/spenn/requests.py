from copa.services.spenn.api import SpennAPI
from copa.settings import SPENN_CALLBACK_URL


class SpennRequest(SpennAPI):
    def __init__(self, phone=None, amount=None, message=None, reference=None):
        super().__init__()

        self.callback_url = SPENN_CALLBACK_URL
        self.phone_number = phone
        self.amount = 1
        self.message = message
        self.external_reference = reference

    def create(self):
        return self.post(
            self.url.create_request_url(),
            {
                "amount": self.amount,
                "phoneNumber": self.phone_number,
                "message": self.message,
                "externalReference": self.external_reference,
                "callbackUrl": self.callback_url,
            },
        )

    def status(self, request_id):
        return self.get(self.url.request_status_url(request_id))

    def cancel(self, request_id):
        return self.post(
            self.url.cancel_request_url(),
            {
                "requestMoneyGuid": request_id,
            },
        )
