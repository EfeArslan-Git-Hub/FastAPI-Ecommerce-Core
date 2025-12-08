from fastapi import FastAPI
from .database import engine, Base
from .routers import products, orders

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Ecommerce Core",
    description="A simple REST API for managing products and orders with stock management.",
    version="1.0.0"
)

app.include_router(products.router)
app.include_router(orders.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Ecommerce Core API"}
