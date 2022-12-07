from django.test import Client, TestCase
import json


class BaseConfiguration(TestCase):
    """
    Base configuration for all test in daca project
    """

    @classmethod
    def setUpClass(cls):

        # We have first to run setUpClass function that
        # we inherited from TestCase
        super(BaseConfiguration, cls).setUpClass()
        cls.client = Client()

    @classmethod
    def query(cls, query: str = None):
        """
        Method to use wen runing all queries and mutations
        for tests
        args:
            query: query of the request to be made
        """
        body = dict()
        body['query'] = query
        response = cls.client.get(
            '/copa/v1/graphql/',
            json.dumps(body),
            content_type='application/json'
        )
        json_response = json.loads(response.content.decode())
        return json_response
