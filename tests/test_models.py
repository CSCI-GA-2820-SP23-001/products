"""
Test cases for Product Model

"""
import os
import logging
import unittest
from datetime import date
from werkzeug.exceptions import NotFound
from service.models import Product, Color, Size, Category, DataValidationError, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  PRODUCT   M O D E L   T E S T   C A S E S
######################################################################
class TestProductModel(unittest.TestCase):
    """ Test Cases for ProductModel Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    #def test_example_replace_this(self):
    #   """ It should always be true """
    #    self.assertTrue(True)

    #def __repr__(self):
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
        # Create 5 Pets
        for _ in range(5):
            product = ProductFactory()
            product.create()
        # See if we get back 5 pets
        products = Product.all()
        self.assertEqual(len(products), 5)
        