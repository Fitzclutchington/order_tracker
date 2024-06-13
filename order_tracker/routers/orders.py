from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from order_tracker.database.database import db_dependency
from order_tracker.models.orders import Orders
from order_tracker.auth.auth import user_dependency

router = APIRouter(
    prefix="/orders", tags=["orders"], responses={404: {"description": "Not found"}}
)

templates = Jinja2Templates(directory="order_tracker/templates/")


@router.get("/", response_class=HTMLResponse)
async def get_orders(request: Request, db: db_dependency, user: user_dependency):
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    orders = db.query(Orders).all()
    return templates.TemplateResponse(
        "orders.html", {"request": request, "orders": orders, "user": user}
    )
