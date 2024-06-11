from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from order_tracker.database.database import Base, engine
from order_tracker.routers import orders

app = FastAPI()


@app.get("/ping")
async def ping():
    return "pong"


@app.get("/")
async def root():
    return RedirectResponse(url="/orders", status_code=status.HTTP_302_FOUND)


app.mount("/static", StaticFiles(directory="order_tracker/static"), name="static")

Base.metadata.create_all(bind=engine)

app.include_router(orders.router)
