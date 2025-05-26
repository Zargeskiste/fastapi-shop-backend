from typing import Dict, Optional
from models import Product, Stock

# Type definition for our product database
ProductDB = Dict[int, Product]

# In-memory database to store products
_PRODUCTS_DB: ProductDB = {}

# Initialize with some sample products
def init_db():
    """Initialize the database with sample products"""
    global _PRODUCTS_DB
    
    # Only initialize if empty
    if not _PRODUCTS_DB:
        _PRODUCTS_DB = {
            1: Product(
                id=1,
                name="Smartphone X",
                short_description="The latest smartphone with amazing features",
                product_description="A detailed description of the smartphone with all its features and specifications. "
                                  "This smartphone comes with a high-resolution display, powerful processor, and long-lasting battery.",
                price=799.99,
                stock=Stock(quantity=25)
            ),
            2: Product(
                id=2,
                name="Laptop Pro",
                short_description="Professional laptop for developers",
                product_description="A high-performance laptop designed for developers and professionals. "
                                  "Features a fast CPU, plenty of RAM, and a solid-state drive for quick boot times and application loading.",
                price=1299.99,
                stock=Stock(quantity=15)
            ),
            3: Product(
                id=3,
                name="Wireless Headphones",
                short_description="Premium noise-cancelling headphones",
                product_description="Experience superior sound quality with these wireless noise-cancelling headphones. "
                                  "Perfect for commuting, traveling, or just enjoying your favorite music without distractions.",
                price=249.99,
                stock=Stock(quantity=50)
            ),
            4: Product(
                id=4,
                name="Smart Watch",
                short_description="Track your fitness and stay connected",
                product_description="This smart watch helps you stay on top of your fitness goals while keeping you connected. "
                                  "Features include heart rate monitoring, step counting, and notification alerts.",
                price=199.99,
                stock=Stock(quantity=30)
            ),
            5: Product(
                id=5,
                name="Bluetooth Speaker",
                short_description="Portable speaker with amazing sound",
                product_description="Take your music anywhere with this portable Bluetooth speaker. "
                                  "Despite its compact size, it delivers rich, room-filling sound and has a battery that lasts all day.",
                price=89.99,
                stock=Stock(quantity=40)
            ),
        }

def get_products_db() -> ProductDB:
    """
    Get the products database.
    
    Returns:
        ProductDB: The products database dictionary
    """
    # Initialize database if it's the first call
    init_db()
    return _PRODUCTS_DB
