import redis
import json
from fastapi import FastAPI

app = FastAPI()

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

fake_db = {
    1: {"name": "Laptop", "price": 50000},
    2: {"name": "Phone", "price": 30000}
}


@app.get("/products/{product_id}")
def get_product(product_id: int):

    # 1. Check Redis
    cached_product = r.get(f"product:{product_id}")

    if cached_product:
        return {
            "source": "Redis Cache",
            "product": json.loads(cached_product)
        }

    # 2. Cache MISS → get from database
    product = fake_db.get(product_id)

    if not product:
        return {"error": "Product not found"}

    # 3. Store in Redis
    r.set(
        f"product:{product_id}", 
        json.dumps(product), 
        ex=60)

    # 4. Return product
    return {
        "source": "Database",
        "product": product
    }

@app.put("/products/{product_id}")
def update_product(product_id: int, price: int):

    # Check if product exists
    product = fake_db.get(product_id)

    if not product:
        return {"error": "Product not found"}

    # Update database
    product["price"] = price

    # Delete old cache
    r.delete(f"product:{product_id}")

    return {
        "message": "Product updated",
        "product": product
    }