from fastapi import APIRouter, Depends, Body, Query, HTTPException
from sqlmodel import Session
from app.core.database import get_db
from app.schemas.cart import AddToCartIn
from app.crud import user as crud_user, product as crud_product, cart as crud_cart

router = APIRouter()

@router.post("/add/")
def add_to_cart(payload: AddToCartIn = Body(...), db: Session = Depends(get_db)):
    user = None
    if payload.telegram_id:
        user = crud_user.get_user_by_telegram(db, payload.telegram_id)
    if not user:
        user = crud_user.get_first_user(db)
    if not user:
        raise HTTPException(status_code=400, detail="No user in DB")

    cart = crud_cart.get_or_create_cart(db, user)
    product = crud_product.get_product(db, payload.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    crud_cart.add_to_cart(db, cart, product, payload.quantity)
    return {"ok": True}

@router.get("/me/")
def cart_me(telegram_id: int | None = Query(None), db: Session = Depends(get_db)):
    user = None
    if telegram_id:
        user = crud_user.get_user_by_telegram(db, telegram_id)
    if not user:
        user = crud_user.get_first_user(db)
    if not user:
        return {"items": []}
    cart = crud_cart.get_or_create_cart(db, user)
    items = []
    for it in crud_cart.get_cart_items(db, cart):
        prod = crud_product.get_product(db, it.product_id)
        items.append({"product": {"id": prod.id, "name": prod.name, "price": prod.price}, "quantity": it.quantity})
    return {"items": items}

@router.post("/buy/")
def buy(telegram_id: int | None = Body(None), db: Session = Depends(get_db)):
    user = None
    if telegram_id:
        user = crud_user.get_user_by_telegram(db, telegram_id)
    if not user:
        user = crud_user.get_first_user(db)
    if not user:
        raise HTTPException(status_code=400, detail="No user in DB")
    cart = crud_cart.get_or_create_cart(db, user)
    crud_cart.clear_cart(db, cart)
    return {"ok": True}
