from fastapi import FastAPI
from app.core.database import init_db
from app.api.routers import products, users, cart
from app.core import bot as bot_module
import asyncio

app = FastAPI(title="Sock Shop FastAPI")

app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(cart.router, prefix="/api/cart", tags=["cart"])

@app.on_event("startup")
async def startup_event():
    init_db()
    if bot_module.bot.token and bot_module.bot.token != "":
        loop = asyncio.get_running_loop()
        loop.create_task(bot_module.start_polling())

@app.get("/healthz")
def healthz():
    return {"status":"ok"}
