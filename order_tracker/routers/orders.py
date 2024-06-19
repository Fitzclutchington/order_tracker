from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from order_tracker.auth.auth import user_dependency
from order_tracker.database.database import db_dependency
from order_tracker.models.orders import Orders

router = APIRouter(
    prefix="/orders", tags=["orders"], responses={404: {"description": "Not found"}}
)

templates = Jinja2Templates(directory="order_tracker/templates/")


# TODO: figure out how to render username instead
# of user id of the sales owner
@router.get("/", response_class=HTMLResponse)
async def get_orders(request: Request, db: db_dependency, user: user_dependency):
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    orders = db.query(Orders).all()
    return templates.TemplateResponse(
        "orders.html", {"request": request, "orders": orders, "user": user}
    )


@router.get("/create", response_class=HTMLResponse)
async def create_order_page(request: Request, user: user_dependency):
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        "add-order.html", {"request": request, "user": user}
    )


@router.post("/create", response_class=HTMLResponse)
async def create_order(
    request: Request, db: db_dependency, user: user_dependency, name: str = Form(...)
):

    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    orders_model = Orders()
    orders_model.name = name
    orders_model.sales_user_id = user.id

    db.add(orders_model)
    db.commit()
    return RedirectResponse(url="/orders", status_code=status.HTTP_302_FOUND)
