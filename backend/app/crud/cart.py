from sqlmodel import Session, select
from app.models.cart import Cart, CartItem
from app.models.user import User
from app.models.product import Product

def createCart(db: Session, user: User) -> Cart:
    
    q = select(Cart).where(Cart.user_id == user.id)
    cart = db.exec(q).first()
    
    if cart:
        return cart
    
    new_cart = Cart(user_id=user.id)
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_cart




def addItem(db: Session, cart: Cart, product: Product, quantity: int = 1):
    q = select(CartItem).where(
        CartItem.cart_id == cart.id, 
        CartItem.product_id == product.id)
    
    item = db.exec(q).first()
    
    if item:
        item.quantity += quantity
    else:
        item = CartItem(cart_id=cart.id, 
                        product_id=product.id, 
                        quantity=quantity)
        db.add(item)
    db.commit()
    db.refresh(item)
    return item


def getItems(db: Session, cart: Cart):
    q = select(CartItem).where(CartItem.cart_id == cart.id)
    return db.exec(q).all()




def clearCart(db: Session, cart: Cart):
    items = getItems(db, cart)
    
    for it in items:
        db.delete(it)
        
    db.commit()
    
    return True
