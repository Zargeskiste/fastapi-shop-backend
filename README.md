# Shop API Backend

This is a backend API for an Angular Shop Frontend, developed with Python and Flask.

## Features

- Product management endpoints (list, get, create, update, delete)
- Custom Stock class for inventory management
- CORS headers implemented for frontend access
- Simple and lightweight implementation

## Requirements

- Python 3.6+
- Flask
- Flask-CORS

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

To start the API server:

```bash
python app.py
```

The API will be available at http://localhost:8000/api/products/

## Endpoints

- `GET /api/products/` - List all products
- `GET /api/products/{product_id}/` - Get a specific product
- `POST /api/products/create/` - Create a new product
- `PUT /api/products/{product_id}/` - Update a product
- `DELETE /api/products/{product_id}/` - Delete a product
