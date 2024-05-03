from fastapi import FastAPI
from api import top

app = FastAPI()

app.include_router(top.router)