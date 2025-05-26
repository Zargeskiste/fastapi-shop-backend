from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import re

# Stock class for inventory management
class Stock:
    def __init__(self, quantity=0):
        self.quantity = quantity

    def decrease(self, amount=1):
        if self.quantity >= amount:
            self.quantity -= amount
            return True
        return False

    def increase(self, amount=1):
        self.quantity += amount
        return True

    def to_dict(self):
        return {"quantity": self.quantity}

# Product class
class Product:
    def __init__(self, id, name, short_description, product_description, price, stock=None):
        self.id = id
        self.name = name
        self.short_description = short_description
        self.product_description = product_description
        self.price = price
        self.stock = stock if stock else Stock(0)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "short_description": self.short_description,
            "product_description": self.product_description,
            "price": self.price,
            "stock": self.stock.to_dict()
        }

# In-memory product database
products = {
    1: Product(
        id=1,
        name="Smartphone X",
        short_description="The latest smartphone with amazing features",
        product_description="A detailed description of the smartphone with all its features and specifications. This smartphone comes with a high-resolution display, powerful processor, and long-lasting battery.",
        price=799.99,
        stock=Stock(25)
    ),
    2: Product(
        id=2,
        name="Laptop Pro",
        short_description="Professional laptop for developers",
        product_description="A high-performance laptop designed for developers and professionals. Features a fast CPU, plenty of RAM, and a solid-state drive for quick boot times and application loading.",
        price=1299.99,
        stock=Stock(15)
    ),
    3: Product(
        id=3,
        name="Wireless Headphones",
        short_description="Premium noise-cancelling headphones",
        product_description="Experience superior sound quality with these wireless noise-cancelling headphones. Perfect for commuting, traveling, or just enjoying your favorite music without distractions.",
        price=249.99,
        stock=Stock(50)
    ),
    4: Product(
        id=4,
        name="Smart Watch",
        short_description="Track your fitness and stay connected",
        product_description="This smart watch helps you stay on top of your fitness goals while keeping you connected. Features include heart rate monitoring, step counting, and notification alerts.",
        price=199.99,
        stock=Stock(30)
    ),
    5: Product(
        id=5,
        name="Bluetooth Speaker",
        short_description="Portable speaker with amazing sound",
        product_description="Take your music anywhere with this portable Bluetooth speaker. Despite its compact size, it delivers rich, room-filling sound and has a battery that lasts all day.",
        price=89.99,
        stock=Stock(40)
    ),
}

class ShopAPIHandler(BaseHTTPRequestHandler):
    # CORS headers
    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    # Helper to set JSON response
    def _set_json_response(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self._set_cors_headers()
        self.end_headers()
    
    # Parse request body as JSON
    def _get_request_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            return json.loads(body.decode('utf-8'))
        return {}
    
    # Handle OPTIONS method for CORS preflight
    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    # GET method to retrieve products
    def do_GET(self):
        # GET all products
        if self.path == '/api/products/' or self.path == '/api/products':
            self._set_json_response()
            self.wfile.write(json.dumps([product.to_dict() for product in products.values()]).encode('utf-8'))
            return
        
        # GET specific product
        product_match = re.match(r'/api/products/([0-9]+)/?', self.path)
        if product_match:
            product_id = int(product_match.group(1))
            if product_id in products:
                self._set_json_response()
                self.wfile.write(json.dumps(products[product_id].to_dict()).encode('utf-8'))
            else:
                self._set_json_response(404)
                self.wfile.write(json.dumps({"error": "Product not found"}).encode('utf-8'))
            return
        
        # Route not found
        self._set_json_response(404)
        self.wfile.write(json.dumps({"error": "Route not found"}).encode('utf-8'))
    
    # POST method to create products
    def do_POST(self):
        # Create a new product
        if self.path == '/api/products/create/' or self.path == '/api/products/create':
            try:
                data = self._get_request_body()
                
                # Validate required fields
                required_fields = ['name', 'short_description', 'product_description', 'price']
                for field in required_fields:
                    if field not in data:
                        self._set_json_response(400)
                        self.wfile.write(json.dumps({"error": f"Missing required field: {field}"}).encode('utf-8'))
                        return
                
                # Find the next available ID
                new_id = max(products.keys(), default=0) + 1
                
                # Create new product
                stock_qty = data.get('stock', 0)
                stock = Stock(stock_qty)
                
                new_product = Product(
                    id=new_id,
                    name=data['name'],
                    short_description=data['short_description'],
                    product_description=data['product_description'],
                    price=float(data['price']),
                    stock=stock
                )
                
                # Add to database
                products[new_id] = new_product
                
                self._set_json_response(201)
                self.wfile.write(json.dumps(new_product.to_dict()).encode('utf-8'))
                return
            except json.JSONDecodeError:
                self._set_json_response(400)
                self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode('utf-8'))
                return
        
        # Route not found
        self._set_json_response(404)
        self.wfile.write(json.dumps({"error": "Route not found"}).encode('utf-8'))
    
    # PUT method to update products
    def do_PUT(self):
        product_match = re.match(r'/api/products/([0-9]+)/?', self.path)
        if product_match:
            product_id = int(product_match.group(1))
            if product_id in products:
                try:
                    data = self._get_request_body()
                    product = products[product_id]
                    
                    # Update fields if provided
                    if 'name' in data:
                        product.name = data['name']
                    if 'short_description' in data:
                        product.short_description = data['short_description']
                    if 'product_description' in data:
                        product.product_description = data['product_description']
                    if 'price' in data:
                        product.price = float(data['price'])
                    if 'stock' in data:
                        product.stock.quantity = int(data['stock'])
                    
                    self._set_json_response()
                    self.wfile.write(json.dumps(product.to_dict()).encode('utf-8'))
                except json.JSONDecodeError:
                    self._set_json_response(400)
                    self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode('utf-8'))
            else:
                self._set_json_response(404)
                self.wfile.write(json.dumps({"error": "Product not found"}).encode('utf-8'))
            return
        
        # Route not found
        self._set_json_response(404)
        self.wfile.write(json.dumps({"error": "Route not found"}).encode('utf-8'))
    
    # DELETE method to remove products
    def do_DELETE(self):
        product_match = re.match(r'/api/products/([0-9]+)/?', self.path)
        if product_match:
            product_id = int(product_match.group(1))
            if product_id in products:
                del products[product_id]
                self._set_json_response()
                self.wfile.write(json.dumps({"message": f"Product {product_id} deleted successfully"}).encode('utf-8'))
            else:
                self._set_json_response(404)
                self.wfile.write(json.dumps({"error": "Product not found"}).encode('utf-8'))
            return
        
        # Route not found
        self._set_json_response(404)
        self.wfile.write(json.dumps({"error": "Route not found"}).encode('utf-8'))

if __name__ == '__main__':
    # Create HTTP server
    server = HTTPServer(('0.0.0.0', 8000), ShopAPIHandler)
    print("Server started at http://localhost:8000/api/products/")
    
    try:
        # Start the server
        server.serve_forever()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("Server stopped.")
        server.server_close()
