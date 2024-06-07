from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from order_tracker.database.database import db_dependency
from order_tracker.models.orders import Orders

router = APIRouter(
    prefix="/orders", tags=["orders"], responses={404: {"description": "Not found"}}
)

templates = Jinja2Templates(directory="order_tracker/templates/")


@router.get("/", response_class=HTMLResponse)
async def get_orders(request: Request, db: db_dependency):
    orders = db.query(Orders).all()
    return templates.TemplateResponse(
        "orders.html", {"request": request, "orders": orders}
    )
