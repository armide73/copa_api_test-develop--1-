from copa.test_config import BaseConfiguration
from .test_data import users_query


class TestAuthentication(BaseConfiguration):

    def test_users_query(self):
        res = self.query(users_query)
        self.assertEqual(len(res['data']['users']['results']), 0)
