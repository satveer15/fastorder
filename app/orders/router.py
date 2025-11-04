from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Order, User
from app.schemas import OrderCreate, OrderUpdate, OrderResponse
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new order for the authenticated user"""
    new_order = Order(
        user_id=current_user.id,
        item_name=order_data.item_name,
        quantity=order_data.quantity,
        price=order_data.price,
        status="pending"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


@router.get("/", response_model=List[OrderResponse])
def get_my_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all orders for the authenticated user"""
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific order by ID"""
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    # Make sure user can only access their own orders
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this order"
        )

    return order


@router.patch("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing order"""
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this order"
        )

    # Update fields if provided
    if order_data.item_name is not None:
        order.item_name = order_data.item_name
    if order_data.quantity is not None:
        order.quantity = order_data.quantity
    if order_data.price is not None:
        order.price = order_data.price
    if order_data.status is not None:
        order.status = order_data.status

    db.commit()
    db.refresh(order)

    return order


@router.delete("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel an order - sets status to cancelled"""
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this order"
        )

    # Can only cancel pending or processing orders
    if order.status in ["completed", "cancelled"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel order with status: {order.status}"
        )

    order.status = "cancelled"
    db.commit()
    db.refresh(order)

    return order
