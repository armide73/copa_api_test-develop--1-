from copa.services.kudibooks.api import KudiBooksAPI


class KudiUser(KudiBooksAPI):
    """Initialize a user on KuDiBooks API"""
    def __init__(self, **kwargs):
        super().__init__()
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.email = kwargs.get('email')


    def get_details(self):
        """Get a user's details"""
        return self.get(self.url.user_details_url())

    def create(self):
        """Create a user on KuDiBooks API"""
        return self.post(self.url.register_user_url(), {
            'firstName': self.first_name,
            'lastName': self.last_name,
            'email': self.email,
        })
