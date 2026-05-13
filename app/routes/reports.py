from io import BytesIO

import pandas as pd
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.routes.dependencies import template_context
from app.services import stock_service

router = APIRouter(prefix="/reports")


@router.get("/inventory")
def inventory_report(request: Request, db: Session = Depends(get_db)):
    rows = stock_service.get_inventory_report(db)
    return request.app.state.templates.TemplateResponse(
        request,
        "inventory_report.html",
        template_context(request, rows=rows),
    )


@router.get("/inventory.xlsx")
def export_inventory_report(db: Session = Depends(get_db)):
    rows = stock_service.get_inventory_report(db)
    output = BytesIO()
    df = pd.DataFrame(
        rows,
        columns=["code", "name", "unit", "opening", "stock_in", "stock_out", "closing"],
    )
    df = df.rename(
        columns={
            "code": "Mã hàng",
            "name": "Tên hàng hóa",
            "unit": "Đơn vị tính",
            "opening": "Đầu kỳ",
            "stock_in": "Nhập",
            "stock_out": "Xuất",
            "closing": "Tồn cuối",
        }
    )
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Xuat nhap ton")
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="bao-cao-xuat-nhap-ton.xlsx"'},
    )
