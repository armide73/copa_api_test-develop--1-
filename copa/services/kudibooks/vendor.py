"""Kudibooks vendor module"""
from copa.services.kudibooks.api import KudiBooksAPI


class KudiVendor(KudiBooksAPI):
    """Kudibooks API vendor class
    """
    def __init__(self, **kwargs):
        """Initialize a vendor on KuDiBooks API"""
        super().__init__()
        self.headers['Company-Code'] = kwargs.get('company_id')
        self.headers['User-Code'] = kwargs.get('user_code')

        self.vendor_id = kwargs.get('vendor_id')
        self.name = kwargs.get('name')
        self.tin = kwargs.get('tin')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.email = kwargs.get('email')
        self.phone = kwargs.get('phone')
        self.address = kwargs.get('address')
        self.note = kwargs.get('note')

    def get_all(self):
        """Get all vendors"""
        url = self.url.vendors_url()
        return self.get(url)

    def get_details(self):
        """Get a vendor's details"""
        return self.get(self.url.vendor_details_url().format(vendor_id=self.vendor_id))

    def create(self):
        """Create a vendor on KuDiBooks API"""
        return self.post(self.url.vendors_url(), {
            'vendorName': self.name,
            'vendorTIN': self.tin,
            'contactPersonF': self.first_name,
            'contactPersonL': self.last_name,
            'email': self.email,
            'phoneNumber': self.phone,
            'physicalAddress': self.address,
            'note': self.note
        })

    def update(self):
        """Update a vendor on KuDiBooks API"""
        return self.put(
            self.url.vendors_url().format(vendor_id=self.vendor_id),
            {
                'vendorName': self.name,
                'vendorTIN': self.tin,
                'contactPersonF': self.first_name,
                'contactPersonL': self.last_name,
                'email': self.email,
                'phoneNumber': self.phone,
                'physicalAddress': self.address,
                'note': self.note
            }
        )

    def remove(self):
        """Delete a vendor on KudiBooks API"""
        return self.delete(self.url.delete_vendor_url().format(vendor_id=self.vendor_id))
