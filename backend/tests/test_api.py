import unittest
import json

from ..api import app


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_delivery_fee_free(self):
        payload = json.dumps({
            'cart_value': 10000,
            'delivery_distance': 2235,
            'number_of_items': 4,
            'time': '2022-01-21T15:00:00Z'
        })
    
        response = self.app.post('/api/fee', headers={'Content-Type': 'application/json'}, data=payload)

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, response.json['delivery_fee'])
    
    def test_delivery_fee_rush_hour(self):
        payload = json.dumps({
            'cart_value': 790,
            'delivery_distance': 2235,
            'number_of_items': 4,
            'time': '2022-01-21T16:32:00Z'
        })
    
        response = self.app.post('/api/fee', headers={'Content-Type': 'application/json'}, data=payload)

        self.assertEqual(200, response.status_code)
        self.assertAlmostEqual(781, response.json['delivery_fee'])
    
    def test_delivery_fee_more_than_4_items(self):
        payload = json.dumps({
            'cart_value': 790,
            'delivery_distance': 2235,
            'number_of_items': 5,
            'time': '2022-01-20T16:32:00Z'
        })
    
        response = self.app.post('/api/fee', headers={'Content-Type': 'application/json'}, data=payload)

        self.assertEqual(200, response.status_code)
        self.assertAlmostEqual(760, response.json['delivery_fee'])
    
    def test_delivery_fee_distance_less_than_1km(self):
        payload = json.dumps({
            'cart_value': 790,
            'delivery_distance': 935,
            'number_of_items': 4,
            'time': '2022-01-20T16:32:00Z'
        })
    
        response = self.app.post('/api/fee', headers={'Content-Type': 'application/json'}, data=payload)

        self.assertEqual(200, response.status_code)
        self.assertAlmostEqual(410, response.json['delivery_fee'])
    
    def test_delivery_fee_cart_value_over_minimum(self):
        payload = json.dumps({
            'cart_value': 1500,
            'delivery_distance': 1253,
            'number_of_items': 4,
            'time': '2022-01-20T16:32:00Z'
        })
    
        response = self.app.post('/api/fee', headers={'Content-Type': 'application/json'}, data=payload)

        self.assertEqual(200, response.status_code)
        self.assertAlmostEqual(300, response.json['delivery_fee'])
    
    def test_delivery_fee_capped_at_15(self):
        payload = json.dumps({
            'cart_value': 250,
            'delivery_distance': 5253,
            'number_of_items': 4,
            'time': '2022-01-20T16:32:00Z'
        })
    
        response = self.app.post('/api/fee', headers={'Content-Type': 'application/json'}, data=payload)

        self.assertEqual(200, response.status_code)
        self.assertEqual(1500, response.json['delivery_fee'])