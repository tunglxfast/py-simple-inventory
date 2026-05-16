from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import database_exists, get_db, initialize_database
from app.routes.dependencies import template_context
from app.services.auth_service import ensure_default_admin

router = APIRouter()


@router.get("/setup")
def setup_page(request: Request):
    if database_exists():
        return RedirectResponse("/", status_code=303)
    return request.app.state.templates.TemplateResponse(request, "setup.html", template_context(request))


@router.post("/setup/create")
def create_database(db: Session = Depends(get_db)):
    initialize_database()
    ensure_default_admin(db)
    return RedirectResponse("/login", status_code=303)
