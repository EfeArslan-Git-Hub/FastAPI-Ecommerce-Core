from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True

# Order Schemas
class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemSchema]

class OrderItemResponse(OrderItemSchema):
    id: int
    
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    created_at: datetime
    status: str
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
