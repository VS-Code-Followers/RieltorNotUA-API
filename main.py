from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
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

origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key="some-random-string",)


log_level = logging.INFO
logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
)

for router in [offers.router, account.router, query.router]:
    app.include_router(router)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


@app.exception_handler(SQLAlchemyError)
async def hand_db_exceptions(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.exception_handler(ValidationError)
async def hand_validation_exceptions(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()},
    )


@app.exception_handler(RequestValidationError)
async def hand_request_validation_exceptions(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()},
    )


@app.exception_handler(Exception)
async def hand_exceptions(request: Request, exc: AttributeError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


if __name__ == "__main__":
    try:
        run(
            "main:app",
            host=config.fastapi.host,
            port=config.fastapi.port,
            reload=True,
        )
    except (KeyboardInterrupt, SystemExit):
        pass
