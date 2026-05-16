from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.routes.dependencies import template_context
from app.services import area_service
from app.services.exceptions import BusinessError

router = APIRouter(prefix="/areas")


@router.get("")
def areas_page(request: Request, include_inactive: bool = False, db: Session = Depends(get_db)):
    areas = area_service.list_areas(db, include_inactive=include_inactive)
    return request.app.state.templates.TemplateResponse(
        request,
        "areas.html",
        template_context(request, areas=areas, include_inactive=include_inactive, error=None),
    )


@router.post("")
def create_area(
    request: Request,
    name: str = Form(""),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    try:
        area_service.create_area(db, name, description)
    except BusinessError as exc:
        areas = area_service.list_areas(db, include_inactive=True)
        return request.app.state.templates.TemplateResponse(
            request,
            "areas.html",
            template_context(request, areas=areas, include_inactive=True, error=str(exc)),
            status_code=400,
        )
    return RedirectResponse("/areas", status_code=303)


@router.post("/{area_id}/update")
def update_area(
    request: Request,
    area_id: int,
    name: str = Form(""),
    description: str = Form(""),
    is_active: bool = Form(False),
    db: Session = Depends(get_db),
):
    try:
        area_service.update_area(db, area_id, name, description, is_active)
    except BusinessError as exc:
        areas = area_service.list_areas(db, include_inactive=True)
        return request.app.state.templates.TemplateResponse(
            request,
            "areas.html",
            template_context(request, areas=areas, include_inactive=True, error=str(exc)),
            status_code=400,
        )
    return RedirectResponse("/areas?include_inactive=true", status_code=303)
