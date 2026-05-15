from datetime import date

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.routes.dependencies import template_context
from app.schemas.stock import StockLineData
from app.services import area_service, product_service, stock_service
from app.services.exceptions import BusinessError

router = APIRouter()


@router.get("/stock/{document_type}")
def stock_form(request: Request, document_type: str, db: Session = Depends(get_db)):
    document_type = document_type.upper()
    title = "Nhập kho" if document_type == "IN" else "Xuất kho"
    return request.app.state.templates.TemplateResponse(
        request,
        "stock_form.html",
        template_context(
            request,
            title=title,
            document_type=document_type,
            products=product_service.list_products(db),
            areas=area_service.list_areas(db),
            today=date.today().isoformat(),
            error=None,
        ),
    )


@router.post("/stock/{document_type}")
def create_stock_document(
    request: Request,
    document_type: str,
    document_date: date = Form(...),
    area_id: int = Form(...),
    description: str = Form(""),
    proposed_by: str = Form(""),
    note: str = Form(""),
    product_id: list[int] = Form([]),
    quantity: list[int] = Form([]),
    line_note: list[str] = Form([]),
    db: Session = Depends(get_db),
):
    lines = [
        StockLineData(product_id=pid, quantity=qty, note=line_note[index] if index < len(line_note) else "")
        for index, (pid, qty) in enumerate(zip(product_id, quantity, strict=False))
        if pid and qty
    ]
    try:
        stock_service.create_stock_document(
            db,
            document_type.upper(),
            lines,
            document_date,
            area_id,
            description,
            proposed_by,
            note,
        )
    except BusinessError as exc:
        title = "Nhập kho" if document_type.upper() == "IN" else "Xuất kho"
        return request.app.state.templates.TemplateResponse(
            request,
            "stock_form.html",
            template_context(
                request,
                title=title,
                document_type=document_type.upper(),
                products=product_service.list_products(db),
                areas=area_service.list_areas(db),
                today=document_date.isoformat(),
                error=str(exc),
            ),
            status_code=400,
        )
    return RedirectResponse("/documents", status_code=303)


@router.get("/documents")
def documents_page(request: Request, db: Session = Depends(get_db)):
    return request.app.state.templates.TemplateResponse(
        request,
        "documents.html",
        template_context(request, documents=stock_service.list_documents(db)),
    )


@router.get("/documents/{document_id}")
def document_detail(request: Request, document_id: int, db: Session = Depends(get_db)):
    return request.app.state.templates.TemplateResponse(
        request,
        "document_detail.html",
        template_context(request, document=stock_service.get_document(db, document_id)),
    )


@router.get("/inventory/reset")
def reset_inventory_page(request: Request, db: Session = Depends(get_db)):
    return request.app.state.templates.TemplateResponse(
        request,
        "inventory_reset.html",
        template_context(request, rows=stock_service.get_stock_table(db), error=None),
    )


@router.post("/inventory/reset")
async def reset_inventory(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    desired: dict[int, int] = {}
    for key, value in form.items():
        if key.startswith("quantity_"):
            product_id = int(key.removeprefix("quantity_"))
            desired[product_id] = int(value or 0)
    try:
        stock_service.reset_inventory(db, desired)
    except BusinessError as exc:
        return request.app.state.templates.TemplateResponse(
            request,
            "inventory_reset.html",
            template_context(request, rows=stock_service.get_stock_table(db), error=str(exc)),
            status_code=400,
        )
    return RedirectResponse("/reports/inventory", status_code=303)
