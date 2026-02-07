from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models.interactions import CartItem, ProductLike, Purchase # Añadimos Purchase
from app.models.users import User
from app.models.products import Product # Necesario para validar existencia y precio
from app.core.security import get_current_user

router = APIRouter(prefix="/interactions", tags=["Interactions"])

@router.post("/like/{product_id}")
def toggle_like(product_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    # Validar que el producto existe antes de dar like
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    statement = select(ProductLike).where(ProductLike.user_id == current_user.id, ProductLike.product_id == product_id)
    like = session.exec(statement).first()

    if like:
        session.delete(like)
        msg = "Like removed"
    else:
        new_like = ProductLike(user_id=current_user.id, product_id=product_id)
        session.add(new_like)
        msg = "Like added"

    session.commit()
    return {"message": msg}

@router.post("/cart/{product_id}")
def add_to_cart(product_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    # Validar que el producto existe
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    statement = select(CartItem).where(CartItem.user_id == current_user.id, CartItem.product_id == product_id)
    item = session.exec(statement).first()

    if item:
        item.quantity += 1
        session.add(item)
    else:
        new_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        session.add(new_item)

    session.commit()
    return {"message": "Added to cart"}

# --- BLOQUE NUEVO: LA LÓGICA DE COMPRA ---

@router.post("/checkout")
def process_checkout(
    current_user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    # 1. Traer todos los items del carrito del usuario
    statement = select(CartItem).where(CartItem.user_id == current_user.id)
    cart_items = session.exec(statement).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="El carrito está vacío")

    # 2. Calcular el costo total
    total_cost = 0
    items_to_buy = []
    
    for item in cart_items:
        product = session.get(Product, item.product_id)
        if product:
            total_cost += product.price * item.quantity
            items_to_buy.append((product, item.quantity))

    # 3. Validar Saldo
    if current_user.balance < total_cost:
        raise HTTPException(
            status_code=400, 
            detail=f"Saldo insuficiente. Tienes ${current_user.balance}, necesitas ${total_cost}"
        )

    # 4. Ejecutar la compra (Transacción)
    current_user.balance -= total_cost
    session.add(current_user)

    for product, quantity in items_to_buy:
        # Registramos la compra
        new_purchase = Purchase(
            user_id=current_user.id,
            product_id=product.id,
            price_at_purchase=product.price # Importante por si el precio cambia después
        )
        session.add(new_purchase)

    # 5. Vaciar el carrito
    for item in cart_items:
        session.delete(item)

    session.commit()
    
    return {
        "message": "Compra exitosa", 
        "total_paid": total_cost, 
        "remaining_balance": current_user.balance
    }

