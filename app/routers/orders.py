from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

@router.post("/", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    # Create the order object first (but don't commit until we verify items)
    new_order = models.Order(status="pending")
    db.add(new_order)
    
    # We need to flush to get the new_order.id, but we can rollback if anything fails
    db.flush() 

    total_items_to_add = []
    
    try:
        for item in order.items:
            # Check if product exists and verify stock
            product = db.query(models.Product).filter(models.Product.id == item.product_id).with_for_update().first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")
            
            if product.stock_quantity < item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for product '{product.name}' (id: {product.id}). Available: {product.stock_quantity}")
            
            # Deduct stock
            product.stock_quantity -= item.quantity
            
            # Create OrderItem
            order_item = models.OrderItem(
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            total_items_to_add.append(order_item)
            
        # Add all items and commit details
        db.add_all(total_items_to_add)
        db.commit()
        db.refresh(new_order)
        return new_order
        
    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
