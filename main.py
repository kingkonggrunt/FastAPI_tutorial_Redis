from fastapi import FastAPI, Response
from src import schemas
app = FastAPI()

products = [
    {"id": 1, "name": "iPad", "price": 599},
    {"id": 2, "name": "iPhone", "price": 999},
    {"id": 3, "name": "iWatch", "price": 699},
]


@app.get("/home")
def print_home():
    return {"message": "Hello World"}

@app.get("/")
def print_root():
    return {"message": "At root"}

@app.get("/products")
def product_index():
    return products

@app.post("/products")
def create_product(new_product: schemas.Product, response: Response):
    product = new_product.dict()
    product['id'] = len(products) + 1
    products.append(product)
    response.status_code = 201
    return product

@app.put("/products/{id}")
def edit_product(id: int, edited_product: schemas.Product, response: Response):
    for product in products:
        if product["id"] == id:
            product['name'] = edited_product.name
            product['price'] = edited_product.price
            response.status_code = 200
            return product
        else:
            response.status_code = 404
            return "Product Not found"

@app.delete("/products/{id}")
def destroy_product(id: int, response: Response):
    for product in products:
        if product["id"] == id:
            products.remove(product)
            response.status_code = 204
            return product

    response.status_code = 404 
    return "Product Not found"


@app.get("/products/search")
def product_search(name, response: Response):
    found = [product for product in products if name.lower() in product["name"].lower()]

    if not found:
        response.status_code = 404
        return "No products found"

    return found if len(found) > 1 else found[0]

@app.get("/products/{id}")  # place dynamic routes below specific routes
def product(id: int, response: Response):
    for product in products:
        if product["id"] == id:
            return product

    response.status_code = 404
    return "Not found"
