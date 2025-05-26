from pydantic import BaseModel, Field
from typing import Optional

class Stock(BaseModel):
    """
    Stock model to handle product inventory
    """
    quantity: int = Field(default=0, ge=0, description="Available quantity of the product")
    
    def decrease(self, amount: int = 1) -> bool:
        """
        Decrease stock by given amount if possible
        
        Args:
            amount: Amount to decrease (default: 1)
            
        Returns:
            bool: True if decrease was successful, False if not enough stock
        """
        if self.quantity >= amount:
            self.quantity -= amount
            return True
        return False
    
    def increase(self, amount: int = 1) -> None:
        """
        Increase stock by given amount
        
        Args:
            amount: Amount to increase (default: 1)
        """
        self.quantity += amount

class ProductBase(BaseModel):
    """Base product model with common attributes"""
    name: str = Field(..., min_length=1, max_length=100, description="Product name")
    short_description: str = Field(..., min_length=1, max_length=200, description="Short product description")
    product_description: str = Field(..., min_length=1, description="Full product description")
    price: float = Field(..., gt=0, description="Product price")

class ProductCreate(ProductBase):
    """Model for creating a new product"""
    stock: int = Field(default=0, ge=0, description="Initial stock quantity")

class ProductUpdate(BaseModel):
    """Model for updating a product (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    short_description: Optional[str] = Field(None, min_length=1, max_length=200)
    product_description: Optional[str] = Field(None, min_length=1)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)

class Product(ProductBase):
    """Complete product model with ID and stock"""
    id: int = Field(..., description="Unique product identifier")
    stock: Stock = Field(default_factory=lambda: Stock(quantity=0))
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Smartphone X",
                "short_description": "The latest smartphone with amazing features",
                "product_description": "A detailed description of the smartphone with all its features and specifications.",
                "price": 799.99,
                "stock": {"quantity": 25}
            }
        }
