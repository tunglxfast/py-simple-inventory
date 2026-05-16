from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.routes.dependencies import template_context
from app.services import product_service
from app.services.exceptions import BusinessError

router = APIRouter(prefix="/products")


def render_products_page(
    request: Request,
    db: Session,
    search: str | None = None,
    include_inactive: bool = False,
    error: str | None = None,
    status_code: int = 200,
):
    products = product_service.list_products(db, include_inactive=include_inactive, search=search)
    return request.app.state.templates.TemplateResponse(
        request,
        "products.html",
        template_context(
            request,
            products=products,
            search=search or "",
            include_inactive=include_inactive,
            error=error,
        ),
        status_code=status_code,
    )


@router.get("")
def products_page(
    request: Request,
    search: str | None = None,
    include_inactive: bool = False,
    db: Session = Depends(get_db),
):
    return render_products_page(request, db, search=search, include_inactive=include_inactive)


@router.post("")
def create_product(
    request: Request,
    code: str = Form(""),
    name: str = Form(""),
    unit: str = Form(""),
    note: str = Form(""),
    db: Session = Depends(get_db),
):
    try:
        product_service.create_product(db, code, name, unit, note)
    except BusinessError as exc:
        return render_products_page(request, db, include_inactive=True, error=str(exc), status_code=400)
    return RedirectResponse("/products", status_code=303)


@router.post("/{product_id}/update")
def update_product(
    request: Request,
    product_id: int,
    code: str = Form(""),
    name: str = Form(""),
    unit: str = Form(""),
    note: str = Form(""),
    is_active: bool = Form(False),
    db: Session = Depends(get_db),
):
    try:
        product_service.update_product(db, product_id, code, name, unit, note, is_active=is_active)
    except BusinessError as exc:
        return render_products_page(request, db, include_inactive=True, error=str(exc), status_code=400)
    return RedirectResponse("/products?include_inactive=true", status_code=303)


@router.post("/{product_id}/delete")
def delete_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    try:
        product_service.delete_product(db, product_id)
    except BusinessError as exc:
        return render_products_page(request, db, error=str(exc), status_code=400)
    return RedirectResponse("/products", status_code=303)
