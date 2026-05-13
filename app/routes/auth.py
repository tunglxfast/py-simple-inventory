from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.security import create_auth_token
from app.core.database import get_db
from app.routes.dependencies import template_context
from app.services import auth_service
from app.services.exceptions import BusinessError

router = APIRouter()


@router.get("/login")
def login_page(request: Request):
    return request.app.state.templates.TemplateResponse(request, "login.html", template_context(request))


@router.post("/login")
def login(
    request: Request,
    username: str = Form(""),
    password: str = Form(""),
    db: Session = Depends(get_db),
):
    try:
        auth_service.require_valid_login(username, password)
        if not auth_service.authenticate(db, username, password):
            raise BusinessError("Tài khoản hoặc mật khẩu không đúng.")
    except BusinessError as exc:
        return request.app.state.templates.TemplateResponse(
            request,
            "login.html",
            template_context(request, error=str(exc), username=username),
            status_code=400,
        )
    response = RedirectResponse("/", status_code=303)
    response.set_cookie("auth_token", create_auth_token(username), httponly=True, samesite="lax")
    return response


@router.post("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("auth_token")
    return response
