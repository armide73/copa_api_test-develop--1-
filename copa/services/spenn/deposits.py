from copa.services.spenn.api import SpennAPI


class SpennDeposit(SpennAPI):
    def __init__(self, amount, destination_phone, message="Deposit"):
        super().__init__()

        self.amount = amount
        self.destination_phone = destination_phone
        self.message = message

    def create(self):
        if not self.amount or not self.destination_phone:
            raise Exception("Amount and destination phone are required")

        return self.post(
            self.url.deposit_customer_account_url(),
            {
                "amount": self.amount,
                "destinationPhoneNumber": self.destination_phone,
                "message": self.message,
            },
        )

    def status(self, transaction_id):
        return self.get(self.url.deposit_status_url(transaction_id))
