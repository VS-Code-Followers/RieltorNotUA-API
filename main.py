from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from uvicorn import run
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
import starlette.status as status
from src.api.routers import offers, account, query
from src.config import get_config
import logging

config = get_config()
app = FastAPI()
# Create session middleware
app.add_middleware(SessionMiddleware, secret_key='some-random-string')

log_level = logging.INFO
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)
# Setup logging

for router in [offers.router, account.router, query.router]:
    # include all routers
    app.include_router(router)


@app.get('/')
async def root():
    # Redirect to /docs. Will be changing in future
    return RedirectResponse(url='/docs', status_code=status.HTTP_302_FOUND)


# Exceptions hadnlers


@app.exception_handler(SQLAlchemyError)
async def hand_db_exceptions(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=400,
        content={'detail': str(exc)},
    )


@app.exception_handler(ValidationError)
async def hand_validation_exceptions(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={'detail': exc.errors()},
    )


@app.exception_handler(RequestValidationError)
async def hand_request_validation_exceptions(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content={'detail': exc.errors()},
    )


@app.exception_handler(Exception)
async def hand_exceptions(request: Request, exc: AttributeError):
    return JSONResponse(
        status_code=400,
        content={'detail': str(exc)},
    )


if __name__ == '__main__':
    try:
        # Run uvicorn app
        run(
            'main:app',
            host=config.fastapi.host,
            port=config.fastapi.port,
            reload=True,
        )
    except (KeyboardInterrupt, SystemExit):
        pass
