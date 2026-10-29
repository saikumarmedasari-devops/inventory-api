
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Inventory Management API")

products = {}
next_product_id = 1


class Product(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    quantity: int = Field(ge=0)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/products", status_code=201)
def create_product(product: Product):
    global next_product_id

    product_id = next_product_id
    products[product_id] = product
    next_product_id += 1

    return {"id": product_id, **product.model_dump()}


@app.get("/products")
def list_products():
    return [
        {"id": product_id, **product.model_dump()}
        for product_id, product in products.items()
    ]


@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = products.get(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return {"id": product_id, **product.model_dump()}
