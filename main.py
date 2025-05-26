from fastapi import FastAPI, HTTPException, Path, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn

from models import Product, ProductCreate, ProductUpdate
from database import get_products_db, ProductDB

app = FastAPI(
    title="Shop API Backend",
    description="API for Angular Shop Frontend",
    version="1.0.0"
)

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Angular app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database
def get_db():
    return get_products_db()

@app.get("/api/products/", response_model=List[Product])
async def get_products(db: ProductDB = Depends(get_db)):
    """
    Get a list of all products.
    
    Returns:
        List[Product]: A list of product objects with their details
    """
    return list(db.values())

@app.get("/api/products/{product_id}/", response_model=Product)
async def get_product(
    product_id: int = Path(..., description="The ID of the product to get"),
    db: ProductDB = Depends(get_db)
):
    """
    Get a specific product by ID.
    
    Args:
        product_id (int): The ID of the product to retrieve
        
    Returns:
        Product: The product data
        
    Raises:
        HTTPException: If the product is not found
    """
    if product_id not in db:
        raise HTTPException(status_code=404, detail="Product not found")
    return db[product_id]

@app.post("/api/products/create/", response_model=Product)
async def create_product(
    product: ProductCreate,
    db: ProductDB = Depends(get_db)
):
    """
    Create a new product.
    
    Args:
        product (ProductCreate): The product data to create
        
    Returns:
        Product: The created product data including its ID
    """
    # Find the next available ID
    new_id = max(db.keys(), default=0) + 1
    
    # Create new product with the generated ID
    new_product = Product(
        id=new_id,
        name=product.name,
        short_description=product.short_description,
        product_description=product.product_description,
        stock=product.stock,
        price=product.price
    )
    
    # Add to database
    db[new_id] = new_product
    return new_product

@app.put("/api/products/{product_id}/", response_model=Product)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: ProductDB = Depends(get_db)
):
    """
    Update an existing product.
    
    Args:
        product_id (int): The ID of the product to update
        product_update (ProductUpdate): The updated product data
        
    Returns:
        Product: The updated product
        
    Raises:
        HTTPException: If the product is not found
    """
    if product_id not in db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get current product
    current_product = db[product_id]
    
    # Update the product with new values, keeping old values where no new ones provided
    update_data = product_update.dict(exclude_unset=True)
    updated_product = current_product.copy(update=update_data)
    
    # Save back to database
    db[product_id] = updated_product
    return updated_product

@app.delete("/api/products/{product_id}/")
async def delete_product(
    product_id: int,
    db: ProductDB = Depends(get_db)
):
    """
    Delete a product.
    
    Args:
        product_id (int): The ID of the product to delete
        
    Returns:
        dict: A confirmation message
        
    Raises:
        HTTPException: If the product is not found
    """
    if product_id not in db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Remove from database
    del db[product_id]
    return {"message": f"Product {product_id} deleted successfully"}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
