from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.routes.dependencies import template_context
from app.services import product_service, stock_service

router = APIRouter()


@router.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    products = product_service.list_products(db)
    stock_rows = stock_service.get_stock_table(db)
    documents = stock_service.list_documents(db)
    low_stock = [row for row in stock_rows if row["stock"] <= 5]
    return request.app.state.templates.TemplateResponse(
        request,
        "dashboard.html",
        template_context(
            request,
            product_count=len(products),
            document_count=len(documents),
            low_stock_count=len(low_stock),
            recent_documents=documents[:5],
            stock_rows=stock_rows[:8],
        ),
    )
