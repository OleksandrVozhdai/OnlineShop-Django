import unittest
from decimal import Decimal
from unittest.mock import MagicMock
from main.models import *

class TechListTestCase(unittest.TestCase):
    def test_discounted_price(self):
        mock_product = TechList(price=Decimal('100.00'))
        self.assertEqual(mock_product.discounted_price, Decimal('75.00'))

    def test_str_method(self):
        mock_product = TechList(product_name="iPhone 15")
        self.assertEqual(str(mock_product), "iPhone 15")

class UserModelTestCase(unittest.TestCase):
    def test_str_method(self):
        user = User(full_name="John Doe")
        self.assertEqual(str(user), "John Doe")

class PendingUserModelTestCase(unittest.TestCase):
    def test_str_method(self):
        pending = PendingUser(email="test@example.com")
        self.assertEqual(str(pending), "test@example.com")

if __name__ == '__main__':
    unittest.main()
