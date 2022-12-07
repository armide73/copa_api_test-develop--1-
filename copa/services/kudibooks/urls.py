"""Kudibboks URL Configuration
"""
from copa.settings import KUDIBOOKS_API_URL


class URLs:
    """Kudibooks API urls class"""
    def __init__(self):
        self.api_url = KUDIBOOKS_API_URL

        # Company
        self.companies = 'company'
        self.required_data = 'company/required'
        self.users = 'user'

        # Vendor
        self.vendors = 'vendor'
        self.update_vendor = 'vendor/update/{vendor_id}'.format(vendor_id="{vendor_id}")
        self.delete_vendor = 'vendor/delete/{vendor_id}'.format(vendor_id="{vendor_id}")
        self.vendor_details = 'vendor/edit/{vendor_id}'.format(vendor_id="{vendor_id}")
        
        # User
        self.user_register = 'user/register'

    def base_url(self):
        return self.api_url

    def companies_url(self):
        return f'{self.api_url}/{self.companies}'

    def company_required_data_url(self):
        return f'{self.api_url}/{self.required_data}'

    def vendors_url(self):
        return f'{self.api_url}/{self.vendors}'

    def vendor_update_url(self):
        return f'{self.api_url}/{self.update_vendor}'

    def vendor_delete_url(self):
        return f'{self.api_url}/{self.delete_vendor}'

    def vendor_details_url(self):
        return f'{self.api_url}/{self.vendor_details}'
    
    def register_user_url(self):
        return f'{self.api_url}/{self.user_register}'
    
    def user_details_url(self):
        return f'{self.api_url}/{self.users}'
