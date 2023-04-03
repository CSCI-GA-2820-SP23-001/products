"""
Test cases for Product Model

"""
import os
import logging
import unittest
from datetime import date
from werkzeug.exceptions import NotFound
from service.models import Product, DataValidationError, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  PRODUCT   M O D E L   T E S T   C A S E S
######################################################################


# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for ProductModel Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    # def test_example_replace_this(self):
    #   """ It should always be true """
    #    self.assertTrue(True)

    # def __repr__(self):
    #    return f"<Product {self.name} id=[{self.id}]>"

    def test_create_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(name="WATCH", category="ACCESSORIES", size="L", color="GREEN")
        self.assertEqual(str(product), "<Product WATCH id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "WATCH")
        self.assertEqual(product.category, "ACCESSORIES")
        self.assertEqual(product.size, "L")

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = Product(name="WATCH", category="ACCESSORIES", size="L", color="GREEN")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)

    def test_list_all_products(self):
        """It should List all Products in the database"""
        products = Product.all()
        self.assertEqual(products, [])
        # Create 5 Products
        for _ in range(5):
            product = ProductFactory()
            product.create()
        # See if we get back 5 products
        products = Product.all()
        self.assertEqual(len(products), 5)

    def test_serialize_a_product(self):
        """It should serialize a Product"""
        product = ProductFactory()
        data = product.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], product.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], product.name)
        self.assertIn("available", data)
        self.assertEqual(data["available"], product.available)
        self.assertIn("color", data)
        self.assertEqual(data["color"], product.color.name)
        self.assertIn("category", data)
        self.assertEqual(data["category"], product.category.name)
        self.assertIn("size", data)
        self.assertEqual(data["size"], product.size.name)
        self.assertIn("create_date", data)
        self.assertEqual(date.fromisoformat(data["create_date"]), product.create_date)
        self.assertIn("last_modify_date", data)
        self.assertEqual(
            date.fromisoformat(data["last_modify_date"]), product.last_modify_date
        )

    def test_deserialize_a_product(self):
        """It should de-serialize a Product"""
        data = ProductFactory().serialize()
        product = Product()
        product.deserialize(data)
        self.assertNotEqual(product, None)
        self.assertEqual(product.name, data["name"])
        self.assertEqual(product.available, data["available"])
        self.assertEqual(product.color.name, data["color"])
        self.assertEqual(product.category.name, data["category"])
        self.assertEqual(product.size.name, data["size"])
        self.assertEqual(product.create_date, date.fromisoformat(data["create_date"]))
        self.assertEqual(
            product.last_modify_date, date.fromisoformat(data["last_modify_date"])
        )

    def test_deserialize_missing_data(self):
        """It should not deserialize a Product with missing data"""
        data = {"id": 1, "name": "cheese", "category": "GROCERIES"}
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_available(self):
        """It should not deserialize a bad available attribute"""
        test_product = ProductFactory()
        data = test_product.serialize()
        data["available"] = "true"
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_size(self):
        """It should not deserialize a bad size attribute"""
        test_product = ProductFactory()
        data = test_product.serialize()
        data["color"] = "red"  # wrong case
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_invalid_attribute(self):
        """It should not deserialize invalid attribute"""
        data = {
            "id": 1,
            "name": "shoes",
            "available": "true",
            "category": "FASHION",
            "color": "BLACK",
            "size": "L",
        }
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_find_product(self):
        """It should Find a Product by ID"""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        logging.debug(products)
        # make sure they got saved
        self.assertEqual(len(Product.all()), 5)
        # find the 2nd product in the list
        product = Product.find(products[1].id)
        self.assertIsNot(product, None)
        self.assertEqual(product.id, products[1].id)
        self.assertEqual(product.name, products[1].name)
        self.assertEqual(product.available, products[1].available)
        self.assertEqual(product.color.name, products[1].color.name)
        self.assertEqual(product.category.name, products[1].category.name)
        self.assertEqual(product.size.name, products[1].size.name)
        self.assertEqual(product.create_date, products[1].create_date)
        self.assertEqual(product.last_modify_date, products[1].last_modify_date)

    def test_find_by_name(self):
        """It should Find a Product by Name"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        name = products[0].name
        count = len([product for product in products if product.name == name])
        found = Product.find_by_name(name)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.name, name)

    def test_find_by_availability(self):
        """It should Find Products by Availability"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        available = products[0].available
        count = len([product for product in products if product.available == available])
        found = Product.find_by_availability(available)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.available, available)

    def test_find_by_color(self):
        """It should Find Products by Color"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        color = products[0].color
        count = len([product for product in products if product.color == color])
        found = Product.find_by_color(color)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.color, color)

    def test_find_by_category(self):
        """It should Find Products by Category"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        category = products[0].category
        count = len([product for product in products if product.category == category])
        found = Product.find_by_category(category)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.category, category)

    def test_find_by_size(self):
        """It should Find Products by Size"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        size = products[0].size
        count = len([product for product in products if product.size == size])
        found = Product.find_by_size(size)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.size, size)

    def test_find_by_create_date(self):
        """It should Find Products by Create Date"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        create_date = products[0].create_date
        count = len(
            [product for product in products if product.create_date == create_date]
        )
        found = Product.find_by_create_date(create_date.isoformat())
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.create_date, create_date)

    def test_find_by_last_modify_date(self):
        """It should Find Products by Last Modify Date"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        last_modify_date = products[0].last_modify_date
        count = len(
            [
                product
                for product in products
                if product.last_modify_date == last_modify_date
            ]
        )
        found = Product.find_by_last_modify_date(last_modify_date.isoformat())
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.last_modify_date, last_modify_date)

    def test_find_or_404_not_found(self):
        """It should return 404 not found"""
        self.assertRaises(NotFound, Product.find_or_404, 0)
