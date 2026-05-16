from fastapi import Request

from app.core.security import verify_auth_token


def current_username(request: Request) -> str | None:
    return verify_auth_token(request.cookies.get("auth_token"))


def template_context(request: Request, **kwargs):
    context = {"request": request, "current_username": current_username(request)}
    context.update(kwargs)
    return context

