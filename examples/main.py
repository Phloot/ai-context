from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .domains.marketplace import MarketplaceError
from .routers.marketplace import router as marketplace_router
from .services.marketplace import MarketplaceService

BASE_DIR = Path(__file__).resolve().parent


def create_app() -> FastAPI:
    """Application factory keeps tests isolated and startup wiring explicit."""
    app = FastAPI(title="Flightplan Marketplace Example")
    app.state.marketplace_service = MarketplaceService.example()

    @app.exception_handler(MarketplaceError)
    async def marketplace_error_handler(
        _request: Request, error: MarketplaceError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=error.status_code,
            content={
                "error": {
                    "code": error.code,
                    "message": error.message,
                    "details": error.details,
                }
            },
        )

    app.include_router(marketplace_router)
    app.mount(
        "/static/marketplace",
        StaticFiles(directory=BASE_DIR / "static"),
        name="marketplace-static",
    )
    return app


app = create_app()
