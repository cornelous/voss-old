import unittest
import json

from app import app


class CurrencyTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_successful_signup(self):
        # Given

        base =  "EUR"
        target = "EUR"

        # When
        response = self.app.get('/currency?base=' + base + '&target=' + target)

        # Then
        self.assertEqual(str, '')
        self.assertEqual(200, response.status_code)

    # def tearDown(self):
    #     # Delete Database collections after the test is complete
