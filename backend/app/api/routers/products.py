from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session
from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductOut
from app.crud import product as crud_product

router = APIRouter()

@router.get("/", response_model=list[ProductOut])
def list_products(limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    return crud_product.list_products(db, limit=limit)

@router.post("/", response_model=ProductOut)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create_product(db, payload.name, payload.price, payload.description)
