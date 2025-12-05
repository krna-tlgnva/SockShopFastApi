import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from app.core.config import settings
from app.core.database import SessionLocal
from app.crud import product as crud_product
from app.crud import user as crud_user
from app.crud import cart as crud_cart

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🧦 Welcome to Sock Shop Bot!\n\n"
        "/products — all products\n"
        "/add — add to cart\n"
        "/cart — view cart\n"
        "/buy — checkout\n"
    )


@dp.message(Command("products"))
async def cmd_products(message: types.Message):
    loop = asyncio.get_running_loop()

    def db_query():
        db = SessionLocal()
        try:
            return crud_product.list_products(db, 100)
        finally:
            db.close()

    products = await loop.run_in_executor(None, db_query)

    if not products:
        return await message.answer("No products found.")

    text = "*Products:*\n\n"
    for p in products:
        text += f"ID: {p.id}\n*{p.name}* — {p.price} KZT\n\n"
    await message.answer(text, parse_mode="Markdown")


@dp.message(Command("add"))
async def cmd_add(message: types.Message):
    parts = message.text.split()
    if len(parts) < 2:
        return await message.answer("Usage: /add ID")

    try:
        product_id = int(parts[1])
    except ValueError:
        return await message.answer("Product ID must be a number.")

    tg_id = message.from_user.id

    loop = asyncio.get_running_loop()

    def db_query():
        db = SessionLocal()
        try:
            user = crud_user.get_user_by_telegram(db, tg_id)
            if not user:
                user = crud_user.create_user(
                    db,
                    message.from_user.username or f"user_{tg_id}",
                    tg_id
                )

            cart = crud_cart.get_or_create_cart(db, user)
            product = crud_product.get_product(db, product_id)

            if not product:
                return {"error": "not_found"}

            crud_cart.add_to_cart(db, cart, product, 1)
            return {"ok": True}
        finally:
            db.close()

    result = await loop.run_in_executor(None, db_query)

    if result.get("error") == "not_found":
        return await message.answer("Product not found.")

    await message.answer("Added to cart!")


@dp.message(Command("cart"))
async def cmd_cart(message: types.Message):
    tg_id = message.from_user.id
    loop = asyncio.get_running_loop()

    def db_query():
        db = SessionLocal()
        try:
            user = crud_user.get_user_by_telegram(db, tg_id)
            if not user:
                return []

            cart = crud_cart.get_or_create_cart(db, user)
            items = crud_cart.get_cart_items(db, cart)

            result = []
            for it in items:
                prod = crud_product.get_product(db, it.product_id)
                result.append({
                    "name": prod.name,
                    "qty": it.quantity,
                    "price": prod.price
                })
            return result
        finally:
            db.close()

    cart_items = await loop.run_in_executor(None, db_query)

    if not cart_items:
        return await message.answer("Your cart is empty 🛒")

    text = "🛒 *Your Cart:*\n\n"
    total = 0
    for item in cart_items:
        item_total = item["qty"] * item["price"]
        total += item_total
        text += f"*{item['name']}* × {item['qty']} = {item_total} KZT\n"

    text += f"\nTotal: *{total}* KZT"
    await message.answer(text, parse_mode="Markdown")


@dp.message(Command("buy"))
async def cmd_buy(message: types.Message):
    tg_id = message.from_user.id
    loop = asyncio.get_running_loop()

    def db_query():
        db = SessionLocal()
        try:
            user = crud_user.get_user_by_telegram(db, tg_id)
            if not user:
                return False

            cart = crud_cart.get_or_create_cart(db, user)
            crud_cart.clear_cart(db, cart)
            return True
        finally:
            db.close()

    success = await loop.run_in_executor(None, db_query)

    if not success:
        return await message.answer("Nothing to buy!")

    await message.answer("🧾 Purchase completed!")


async def start_polling():
    await dp.start_polling(bot)
