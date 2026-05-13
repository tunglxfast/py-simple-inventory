from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.database import database_exists
from app.core.logging import configure_logging
from app.routes import areas, auth, dashboard, products, reports, setup, stock


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="Quản lý kho")
    app_root = Path(__file__).resolve().parent
    templates = Jinja2Templates(directory=str(app_root / "templates"))
    app.state.templates = templates

    app.mount("/static", StaticFiles(directory=str(app_root / "static")), name="static")
    @app.middleware("http")
    async def require_database(request: Request, call_next):
        if request.url.path.startswith(("/setup", "/static")):
            return await call_next(request)
        if not database_exists():
            return RedirectResponse("/setup", status_code=303)
        return await call_next(request)

    app.include_router(setup.router)
    app.include_router(auth.router)
    app.include_router(dashboard.router)
    app.include_router(products.router)
    app.include_router(areas.router)
    app.include_router(stock.router)
    app.include_router(reports.router)
    return app


app = create_app()
