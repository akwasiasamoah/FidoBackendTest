from fastapi import FastAPI
from src.schemas import entities
from src.controllers.user_controller import user_router
from src.controllers.transaction_controller import transaction_router
from src.database import create_tables
from os import environ as env

app = FastAPI()

create_tables()

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(transaction_router, prefix="/transactions", tags=["transactions"])

@app.get('/')
def index():
    return {
        "details": f"Hello, World! Secret = {env['MY_VARIABLE']}"
    }