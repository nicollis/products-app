import unittest
from app.models.product import Product

class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product = Product(None, 'Test Product', 'Test Category', 999, '10', 'Test Description')

    def test_price(self):
        self.assertEqual(self.product.price, 9.99)

    def test_set_price(self):
        self.product.price = 12.34
        self.assertEqual(self.product._price, 1234)

    def test_from_request(self):
        req = {
              'name': 'Test Product',
              'category': 'Test Category',
              'price': 9.99,
              'quantity': '10',
              'description': 'Test Description'
          }
        product = Product.from_request(req)
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.category, 'Test Category')
        self.assertEqual(product.price, 9.99)
        self.assertEqual(product._price, 999)
        self.assertEqual(product.quantity, '10')
        self.assertEqual(product.description, 'Test Description')

    def test_from_mongo(self):
        data = {
            '_id': '123',
            'ProductName': 'Test Product',
            'ProductCategory': 'Test Category',
            'Price': 999,
            'AvailableQuantity': '10',
            'ProductDescription': 'Test Description'
        }
        product = Product.from_mongo(data)
        self.assertEqual(product._id, '123')
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.category, 'Test Category')
        self.assertEqual(product.price, 9.99)
        self.assertEqual(product.quantity, '10')
        self.assertEqual(product.description, 'Test Description')

    def test_to_dict(self):
        data = self.product.to_dict()
        self.assertEqual(data['name'], 'Test Product')
        self.assertEqual(data['category'], 'Test Category')
        self.assertEqual(data['price'], 9.99)
        self.assertEqual(data['quantity'], '10')
        self.assertEqual(data['description'], 'Test Description')

if __name__ == '__main__':
    unittest.main()