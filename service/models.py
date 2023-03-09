"""
Models for YourResourceModel

All of the models are stored in this module
"""
import logging
from enum import Enum
from datetime import date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


# Function to initialize the database
def init_db(app):
    """ Initializes the SQLAlchemy app """
    Product.init_db(app)


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

class Color(Enum):
    """Enumeration of valid Product Colors"""
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"
    BLACK = "black"
    WHITE = "white"
    PINK = "pink"
    UNKNOWN = "unknown"
    OTHER = "other"

class Size(Enum):
    """Enumeration of valid Product Sizes"""
    XS = "xs"
    S = "s"
    M = "m"
    L = "l"
    XL = "xl"
    OTHER = "other"
    UNKNOWN = "unknown"

class Category(Enum):
    """Enumeration of valid Product Categories"""
    FASHION = "fashion"
    ACCESSORIES = "accessories"
    GROCERIES = "groceries"
    DRUGS = "drugs"
    PETS = "pets"
    BEAUTY = "beauty"
    HOME = "home"
    DEVICE = "device"
    GAMING = "gaming"
    BOOK = "book"
    OTHER = "other"
    UNKNOWN = "unknown"

class Product(db.Model):
    """
    Class that represents a YourResourceModel
    """

    ##################################################
    # Table Schema
    ##################################################
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=False)
    category = db.Column(
        db.Enum(Category), nullable=False, server_default=(Category.UNKNOWN.name)
    )
    color = db.Column(
        db.Enum(Color), nullable=False, server_default=(Color.UNKNOWN.name)
    )
    size = db.Column(
        db.Enum(Size), nullable=False, server_default=(Size.UNKNOWN.name)
    )
    create_date = db.Column(db.Date(), nullable=False, default=date.today())
    last_modify_date = db.Column(db.Date(), nullable=False, default=date.today())


    def __repr__(self):
        return f"<Product {self.name} id=[{self.id}]>"

    def create(self):
        """ Creates a Product to the database """
        logger.info("Creating %s", self.name)
        # id must be none to generate next primary key
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Product to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a Product from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self) -> dict:
        """ Serializes a Product into a dictionary """
        return {
            "id": self.id,
            "name": self.name,
            "available": self.available,
            "category": self.category.name,
            "color": self.color.name,  # convert enum to string
            "size": self.size.name,
            "create_date": self.create_date.isoformat(),
            "last_modify_date": self.last_modify_date.isoformat()
        }

    def deserialize(self, data: dict):
        """
        Deserializes a Product from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.category = data["category"]
            if isinstance(data["available"], bool):
                self.available = data["available"]
            else:
                raise DataValidationError(
                    "Invalid type for boolean [available]: "
                    + str(type(data["available"]))
                )
            self.color = getattr(Color, data["color"])  # create enum from string
            self.size = getattr(Size, data["size"])
            self.category = getattr(Category, data["category"])
            self.create_date = date.fromisoformat(data["create_date"])
            self.last_modify_date = date.fromisoformat(data["last_modify_date"])
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError("Invalid product: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid product: body of request contained bad or no data " + str(error)
            ) from error
        return self

    
    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def init_db(cls, app: Flask):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls) -> list:
        """ Returns all of the Products in the database """
        logger.info("Processing all Products")
        return cls.query.all()

    @classmethod
    def find(cls, product_id: int):
        """ Finds a Product by it's ID """
        logger.info("Processing lookup for id %s ...", product_id)
        return cls.query.get(product_id)


    @classmethod
    def find_or_404(cls, product_id: int):
        """Find a Product by it's id

        :param product_id: the id of the Product to find
        :type product_id: int

        :return: an instance with the product_id, or 404_NOT_FOUND if not found
        :rtype: Product

        """
        logger.info("Processing lookup or 404 for id %s ...", product_id)
        return cls.query.get_or_404(product_id)


    @classmethod
    def find_by_name(cls, name: str) -> list:
        """Returns all Products with the given name

        Args:
            name (string): the name of the Products you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)


    @classmethod
    def find_by_availability(cls, available: bool = True) -> list:
        """Returns all Products by their availability

        :param available: True for products that are available
        :type available: str

        :return: a collection of Products that are available
        :rtype: list

        """
        logger.info("Processing available query for %s ...", available)
        return cls.query.filter(cls.available == available)

    
    @classmethod
    def find_by_create_date(cls, create_date: str) -> list:
        """Returns all Products by their create date

        Args:
            name (string): the create date of the Products you want to match
        """
        
        logger.info("Processing create_date query for %s ...", create_date)
        return cls.query.filter(cls.create_date == date.fromisoformat(create_date))

    
    @classmethod
    def find_by_last_modify_date(cls, last_modify_date: str) -> list:
        """Returns all Products by their last modify date

        Args:
            name (string): the last modify date of the Products you want to match
        """
        
        logger.info("Processing last_modify_date query for %s ...", last_modify_date)
        return cls.query.filter(cls.last_modify_date == date.fromisoformat(last_modify_date))


    @classmethod
    def find_by_color(cls, color: Color = Color.UNKNOWN) -> list:
        """Returns all Products by their Color

        :param color: values are ['red', 'yello', 'green', ...]
        :type available: enum

        :return: a collection of Products that are available
        :rtype: list

        """
        logger.info("Processing color query for %s ...", color.name)
        return cls.query.filter(cls.color == color)


    @classmethod
    def find_by_size(cls, size: Size = Size.UNKNOWN) -> list:
        """Returns all Products by their Size

        :param size: values are ['xs', 's', 'm', ...]
        :type available: enum

        :return: a collection of Products that are available
        :rtype: list

        """
        logger.info("Processing size query for %s ...", size.name)
        return cls.query.filter(cls.size == size)


    @classmethod
    def find_by_category(cls, category: Category = Category.UNKNOWN) -> list:
        """Returns all Products by their Category

        :param color: values are ['groceries', 'device', 'beauty', ...]
        :type available: enum

        :return: a collection of Products that are available
        :rtype: list

        """
        logger.info("Processing category query for %s ...", category.name)
        return cls.query.filter(cls.category == category)



