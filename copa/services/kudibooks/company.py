"""Kudibooks compny Service."""
from copa.services.kudibooks.api import KudiBooksAPI


class KudiCompany(KudiBooksAPI):
    """A class kuDiBooks company service."""
    def __init__(self, **kwargs):
        """Initialize a company on KuDiBooks API"""
        super().__init__()

        self.headers['User-Code'] = kwargs.get('user_code')
        self.company_name = kwargs.get('company_name')
        self.industry = kwargs.get('industry')
        self.country = kwargs.get('country')
        self.currency = kwargs.get('currency')
        self.plan = kwargs.get('plan')

    def get_all(self):
        """Get all companies"""
        url = self.url.companies_url()
        return self.get(url)

    def create(self):
        """Create a company on KuDiBooks API"""
        return self.post(self.url.companies_url(), {
            'companyName': self.company_name,
            'industry': self.industry,
            'country': self.country,
            'currency': self.currency,
            'plan': self.plan
        })

    def get_required(self):
        """Get required data for company creation"""
        return self.get(self.url.company_required_data_url())
