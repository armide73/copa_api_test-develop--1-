from copa.settings import SPENN_PARTNER_API_URL


class URLs:
    """Spenn API urls class"""

    def __init__(self):
        self.partner_api_url = SPENN_PARTNER_API_URL

    def partner_url(self):
        return self.partner_api_url

    def create_request_url(self):
        return f"{self.partner_api_url}/transaction/request"

    def request_status_url(self, request_id):
        return f"{self.partner_api_url}/transaction/request/{request_id}/status"

    def cancel_request_url(self):
        return f"{self.partner_api_url}/transaction/request/cancel"

    def deposit_customer_account_url(self):
        return f"{self.partner_api_url}/transaction/deposit"

    def deposit_status_url(self, transaction_id):
        return f"{self.partner_api_url}/transaction/{transaction_id}/status"
