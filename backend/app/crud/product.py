from sqlmodel import Session, select
from app.models.product import Product


def createProduct(db: Session, name: str, price: int, description: str | None = None) -> Product:
    p = Product(name=name, 
                price=price, 
                description=description)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p



def listProducts(db: Session, limit: int = 100):
    q = select(Product).limit(limit)
    return db.exec(q).all()

def getProduct(db: Session, product_id: int):
    q = select(Product).where(Product.id == product_id)
    return db.exec(q).first()
